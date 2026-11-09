"""Seed the EDU IDO with demo data.

Usage:
    python seed_org.py preview                      # no org needed: shows the generated people
    python seed_org.py describe --target-org edu-ido  # saves the org's Education Cloud fields to describe_output.json
    python seed_org.py seed     --target-org edu-ido
    python seed_org.py teardown --target-org edu-ido

Leave out --target-org to log in with the username and password in .env instead.
"""

import argparse
import json
import logging
import sys

from seed import config, generate

EDU_OBJECTS = [
    "AcademicTerm",
    "LearningProgram",
    "LearningCourse",
    "CourseOffering",
    "ContactProfile",
    "LearnerProgram",
    "CourseOfferingParticipant",
    "AccountContactRelation",
]


def preview() -> None:
    fake = generate.make_faker()
    groups = {
        "students": generate.students(fake, config.STUDENT_COUNT),
        "faculty": generate.faculty(fake, config.FACULTY_COUNT),
        "marketing_staff": generate.marketing_staff(fake, config.MARKETING_STAFF_COUNT),
    }
    for name, people in groups.items():
        print(f"{name}: {len(people)}")
        for p in people[:3]:
            print("   ", json.dumps(p))


def describe(sf) -> None:
    from seed.schema import Schema

    schema = Schema(sf)
    out = {}
    for obj in EDU_OBJECTS:
        if not schema.has_object(obj):
            out[obj] = "NOT AVAILABLE IN THIS ORG"
            continue
        out[obj] = {
            name: {
                "type": f["type"],
                "required": f["createable"] and not f["nillable"] and not f["defaultedOnCreate"],
                "picklist": [v["value"] for v in f.get("picklistValues", []) if v.get("active")] or None,
            }
            for name, f in schema.fields(obj).items()
            if f["createable"]
        }
    with open("describe_output.json", "w") as f:
        json.dump(out, f, indent=2)
    print("Wrote describe_output.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["preview", "describe", "seed", "teardown"])
    parser.add_argument("--target-org", help="Salesforce CLI alias or username")
    parser.add_argument("--force", action="store_true", help="seed even if a manifest already exists")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")

    if args.command == "preview":
        preview()
        return 0

    from seed.connect import connect
    from seed.loader import Loader, Manifest, teardown

    sf = connect(args.target_org)
    manifest = Manifest(config.MANIFEST_PATH)

    if args.command == "describe":
        describe(sf)
    elif args.command == "seed":
        if not manifest.is_empty() and not args.force:
            print(f"{config.MANIFEST_PATH} already lists seeded records. Run teardown first, or pass --force.")
            return 1
        Loader(sf, manifest).run()
    elif args.command == "teardown":
        teardown(sf, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
