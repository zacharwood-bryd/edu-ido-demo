"""Insert the seed data into the org, step by step.

Build order (each step needs Ids from the ones before it):
 1. University and department accounts
 2. Academic terms
 3. Learning programs (degree programmes) and learning courses (modules)
 4. People as Person Accounts: students, faculty, marketing staff
 5. Faculty and staff linked to their department (AccountContactRelation)
 6. A Contact Profile per person (Student / Faculty / Staff)
 7. Course offerings for each course and term, taught by faculty
 8. Students enrolled on a programme (LearnerProgram)
 9. Students enrolled on course offerings (CourseOfferingParticipant)

Every Id we create is saved to the manifest so teardown deletes exactly those.
"""

import json
import logging
import os
import random

from seed import config, generate
from seed.schema import Schema

log = logging.getLogger(__name__)

BATCH_SIZE = 200  # the limit for one sObject Collections request


class Manifest:
    """A JSON file listing every record created, in creation order."""

    def __init__(self, path: str):
        self.path = path
        self.steps: list[dict] = []
        if os.path.exists(path):
            with open(path) as f:
                self.steps = json.load(f).get("created", [])

    def add(self, sobject: str, ids: list[str]) -> None:
        ids = [i for i in ids if i]
        if ids:
            self.steps.append({"sobject": sobject, "ids": ids})
            self.save()

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump({"created": self.steps}, f, indent=2)

    def is_empty(self) -> bool:
        return not any(step["ids"] for step in self.steps)


class Loader:
    def __init__(self, sf, manifest: Manifest):
        self.sf = sf
        self.schema = Schema(sf)
        self.manifest = manifest
        self.failures = 0

    # ---------- low-level helpers ----------

    def insert(self, sobject: str, records: list[dict]) -> list[str | None]:
        """Insert records in batches of 200. Returns one Id (or None) per record."""
        if not self.schema.has_object(sobject):
            log.warning("%s is not available in this org, skipping %d records", sobject, len(records))
            return [None] * len(records)

        ids: list[str | None] = []
        for start in range(0, len(records), BATCH_SIZE):
            batch = [self.schema.clean(sobject, r) for r in records[start : start + BATCH_SIZE]]
            body = {
                "allOrNone": False,
                "records": [{"attributes": {"type": sobject}, **r} for r in batch],
            }
            results = self.sf.restful("composite/sobjects", method="POST", json=body)
            for result in results:
                if result.get("success"):
                    ids.append(result["id"])
                else:
                    self.failures += 1
                    errors = "; ".join(e.get("message", "") for e in result.get("errors", []))
                    log.error("%s insert failed: %s", sobject, errors)
                    ids.append(None)

        self.manifest.add(sobject, ids)
        log.info("%s: created %d of %d", sobject, sum(1 for i in ids if i), len(records))
        return ids

    def query_one(self, soql: str) -> dict | None:
        records = self.sf.query(soql)["records"]
        return records[0] if records else None

    # ---------- steps ----------

    def accounts(self) -> tuple[str, dict[str, str]]:
        [university_id] = self.insert("Account", [{"Name": config.UNIVERSITY_NAME}])
        depts = [{"Name": name, "ParentId": university_id} for name in config.DEPARTMENTS]
        dept_ids = self.insert("Account", depts)
        return university_id, dict(zip(config.DEPARTMENTS, dept_ids))

    def academic_terms(self) -> list[str | None]:
        records = [
            {"Name": t["name"], "StartDate": t["start"], "EndDate": t["end"], "TermType": "Term"}
            for t in config.ACADEMIC_TERMS
        ]
        return self.insert("AcademicTerm", records)

    def learning_programs(self, dept_ids: dict) -> dict[str, str]:
        provider = self.schema.first_field("LearningProgram", "ProviderId", "AccountId") if self.schema.has_object("LearningProgram") else None
        records = []
        for p in config.PROGRAMMES:
            record = {"Name": p["name"]}
            if provider:
                record[provider] = dept_ids.get(p["school"])
            records.append(record)
        ids = self.insert("LearningProgram", records)
        return {p["name"]: i for p, i in zip(config.PROGRAMMES, ids)}

    def learning_courses(self, dept_ids: dict) -> list[str | None]:
        provider = self.schema.first_field("LearningCourse", "ProviderId", "AccountId") if self.schema.has_object("LearningCourse") else None
        code = self.schema.first_field("LearningCourse", "CourseNumber", "Code") if self.schema.has_object("LearningCourse") else None
        records = []
        for c in config.COURSES:
            record = {"Name": f"{c['code']} {c['name']}"}
            if code:
                record[code] = c["code"]
            if provider:
                record[provider] = dept_ids.get(c["school"])
            records.append(record)
        return self.insert("LearningCourse", records)

    def person_accounts(self, people: list[dict]) -> list[str | None]:
        rt = self.query_one(
            "SELECT Id FROM RecordType WHERE SobjectType = 'Account' "
            "AND IsPersonType = true AND IsActive = true LIMIT 1"
        )
        if rt is None:
            raise RuntimeError("No active Person Account record type found. Is Person Accounts enabled?")

        records = []
        for p in people:
            record = {
                "RecordTypeId": rt["Id"],
                "FirstName": p["first_name"],
                "LastName": p["last_name"],
                "PersonEmail": p["email"],
                "Phone": p["phone"],
                "PersonTitle": p.get("title"),
            }
            if p["persona"] == "Student":
                record.update(
                    {
                        "PersonBirthdate": p["birthdate"],
                        "AccountNumber": p["student_id"],
                        "PersonMailingStreet": p["street"],
                        "PersonMailingCity": p["city"],
                        "PersonMailingPostalCode": p["postcode"],
                        "PersonMailingCountry": "United Kingdom",
                    }
                )
            records.append({k: v for k, v in record.items() if v is not None})
        return self.insert("Account", records)

    def person_contact_ids(self, account_ids: list[str | None]) -> list[str | None]:
        """Each Person Account has a hidden Contact. Return those Contact Ids, same order."""
        found: dict[str, str] = {}
        real_ids = [i for i in account_ids if i]
        for start in range(0, len(real_ids), BATCH_SIZE):
            chunk = ",".join(f"'{i}'" for i in real_ids[start : start + BATCH_SIZE])
            for row in self.sf.query_all(f"SELECT Id, PersonContactId FROM Account WHERE Id IN ({chunk})")["records"]:
                found[row["Id"]] = row["PersonContactId"]
        return [found.get(i) if i else None for i in account_ids]

    def department_links(self, people: list[dict], contact_ids: list, dept_ids: dict) -> None:
        records = [
            {"AccountId": dept_ids[p["department"]], "ContactId": cid, "IsActive": True}
            for p, cid in zip(people, contact_ids)
            if cid and dept_ids.get(p["department"])
        ]
        self.insert("AccountContactRelation", records)

    def contact_profiles(self, people: list[dict], contact_ids: list) -> None:
        if not self.schema.has_object("ContactProfile"):
            log.warning("ContactProfile not in org, skipping profiles")
            return
        type_field = self.schema.first_field("ContactProfile", "Type", "ProfileType")
        records = []
        for p, cid in zip(people, contact_ids):
            if not cid:
                continue
            record = {"ContactId": cid}
            if type_field:
                record[type_field] = p["persona"]
            records.append(record)
        self.insert("ContactProfile", records)

    def course_offerings(self, course_ids: list, term_ids: list, faculty_contacts: list) -> list[dict]:
        """One offering per course per term. Returns [{id, term_index}]."""
        teachers = [c for c in faculty_contacts if c]
        faculty_field = (
            self.schema.first_field("CourseOffering", "PrimaryFacultyId", "InstructorId")
            if self.schema.has_object("CourseOffering")
            else None
        )
        records, index = [], []
        for ti, (term, term_id) in enumerate(zip(config.ACADEMIC_TERMS, term_ids)):
            for ci, (course, course_id) in enumerate(zip(config.COURSES, course_ids)):
                if not course_id:
                    continue
                record = {
                    "Name": f"{course['code']} {course['name']} ({term['name']})",
                    "LearningCourseId": course_id,
                    "AcademicTermId": term_id,
                    "StartDate": term["start"],
                    "EndDate": term["end"],
                }
                if faculty_field and teachers:
                    record[faculty_field] = teachers[ci % len(teachers)]
                records.append({k: v for k, v in record.items() if v is not None})
                index.append(ti)
        ids = self.insert("CourseOffering", records)
        return [{"id": i, "term_index": t} for i, t in zip(ids, index) if i]

    def learner_programs(self, students: list[dict], contact_ids: list, program_ids: dict, term_ids: list) -> None:
        if not self.schema.has_object("LearnerProgram"):
            log.warning("LearnerProgram not in org, skipping programme enrolments")
            return
        learner = self.schema.first_field("LearnerProgram", "LearnerContactId", "ContactId")
        records = []
        for s, cid in zip(students, contact_ids):
            program_id = program_ids.get(s["programme"])
            if not (cid and program_id and learner):
                continue
            records.append(
                {
                    "Name": f"{s['first_name']} {s['last_name']} - {s['programme']}",
                    learner: cid,
                    "LearningProgramId": program_id,
                    "AcademicTermId": term_ids[0],
                    "Status": "Active",
                }
            )
        self.insert("LearnerProgram", records)

    def course_participants(self, contact_ids: list, offerings: list[dict]) -> None:
        current = [o["id"] for o in offerings if o["term_index"] == 0]
        if not current:
            log.warning("No course offerings for the current term, skipping course enrolments")
            return
        if not self.schema.has_object("CourseOfferingParticipant"):
            log.warning("CourseOfferingParticipant not in org, skipping course enrolments")
            return
        participant = self.schema.first_field(
            "CourseOfferingParticipant", "ParticipantContactId", "ContactId"
        )
        records = []
        for cid in contact_ids:
            if not (cid and participant):
                continue
            for offering_id in random.sample(current, min(config.COURSES_PER_STUDENT, len(current))):
                records.append(
                    {participant: cid, "CourseOfferingId": offering_id, "ParticipationStatus": "Enrolled"}
                )
        self.insert("CourseOfferingParticipant", records)

    # ---------- the whole run ----------

    def run(self) -> None:
        fake = generate.make_faker()
        students = generate.students(fake, config.STUDENT_COUNT)
        faculty = generate.faculty(fake, config.FACULTY_COUNT)
        staff = generate.marketing_staff(fake, config.MARKETING_STAFF_COUNT)

        _, dept_ids = self.accounts()
        term_ids = self.academic_terms()
        program_ids = self.learning_programs(dept_ids)
        course_ids = self.learning_courses(dept_ids)

        student_contacts = self.person_contact_ids(self.person_accounts(students))
        faculty_contacts = self.person_contact_ids(self.person_accounts(faculty))
        staff_contacts = self.person_contact_ids(self.person_accounts(staff))

        self.department_links(faculty + staff, faculty_contacts + staff_contacts, dept_ids)
        self.contact_profiles(
            students + faculty + staff, student_contacts + faculty_contacts + staff_contacts
        )

        offerings = self.course_offerings(course_ids, term_ids, faculty_contacts)
        self.learner_programs(students, student_contacts, program_ids, term_ids)
        self.course_participants(student_contacts, offerings)

        log.info("Done. %d record(s) failed; see errors above.", self.failures)


def teardown(sf, manifest: Manifest) -> None:
    """Delete everything in the manifest, newest first, then clear it."""
    # Deleting a Person Account also deletes its hidden Contact, ContactProfile etc.,
    # so some later deletes may report "entity is deleted". That's fine.
    for step in reversed(manifest.steps):
        ids = step["ids"]
        for start in range(0, len(ids), BATCH_SIZE):
            chunk = ",".join(ids[start : start + BATCH_SIZE])
            results = sf.restful(
                "composite/sobjects", method="DELETE", params={"ids": chunk, "allOrNone": "false"}
            )
            ok = sum(1 for r in results if r.get("success"))
            log.info("%s: deleted %d of %d", step["sobject"], ok, len(results))
    manifest.steps = []
    manifest.save()
