# EDU IDO demo seed

Python scripts (simple-salesforce + Faker) that seed an Education Cloud demo org with a fictional UK university, built around the three webinar personas: students, professors (faculty) and marketing staff.

## What it creates

| Step | Object | Records |
| --- | --- | --- |
| 1 | Account (business) | Northfield University + 5 department accounts |
| 2 | AcademicTerm | Autumn 2026, Spring 2027 |
| 3 | LearningProgram | 6 programmes, incl. the AI Leadership short course for the marketing scene |
| 3 | LearningCourse | 6 modules |
| 4 | Account (Person) | 100 students, 20 faculty, 5 marketing staff |
| 5 | AccountContactRelation | Faculty and staff linked to their department |
| 6 | ContactProfile | One per person: Student, Faculty or Staff |
| 7 | CourseOffering | Each module in each term, with a faculty member as primary faculty |
| 8 | LearnerProgram | Each student on one programme |
| 9 | CourseOfferingParticipant | Each student on 3 modules this term |

All counts and names live in `seed/config.py`.

## Schema safety

Education Cloud field names and picklist values move between releases, so the loader describes each object first and:
- skips fields the org doesn't have,
- swaps a picklist value the org rejects for a valid one, and logs it,
- warns about required fields it isn't filling,
- skips an object entirely if it isn't in the org.

Run `describe` first and check `describe_output.json` against what the loader sends.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sf org login web --alias edu-ido
```

## Run

```bash
python seed_org.py preview                          # no org: shows sample generated people
python seed_org.py describe --target-org edu-ido    # dumps the org's EDU fields to describe_output.json
python seed_org.py seed     --target-org edu-ido    # creates everything
python seed_org.py teardown --target-org edu-ido    # deletes exactly what seed created
```

`seed` records every Id it creates in `seed_manifest.json` (git-ignored). `teardown` deletes from that file, newest first, which makes it a reset between demo runs. `seed` refuses to run again while the manifest has records, unless you pass `--force`.

No `sf` CLI? Copy `.env.example` to `.env`, fill it in, and leave out `--target-org`.

## Tests

```bash
python -m pytest -q
```

The tests run against a fake org, so they check the build order and record counts but not the real org's validation rules.

## Not yet covered

- Marketing staff are Person Accounts, not Salesforce Users (Users need licences).
- No applications (IndividualApplication), cases, advisors or engagement data yet.
- Not yet run against the real EDU IDO.
