"""Offline tests: a fake org stands in for Salesforce, so no login is needed."""

import itertools

from seed import config, generate
from seed.loader import Loader, Manifest, teardown
from seed.schema import Schema


def field(name, ftype="string", nillable=True, picklist=None):
    return {
        "name": name,
        "type": ftype,
        "createable": True,
        "nillable": nillable,
        "defaultedOnCreate": False,
        "picklistValues": [{"value": v, "active": True} for v in (picklist or [])],
    }


FAKE_SCHEMA = {
    "Account": [field(n) for n in [
        "Name", "ParentId", "RecordTypeId", "FirstName", "LastName", "PersonEmail", "Phone",
        "PersonTitle", "PersonBirthdate", "AccountNumber", "PersonMailingStreet",
        "PersonMailingCity", "PersonMailingPostalCode", "PersonMailingCountry",
    ]],
    "AcademicTerm": [field("Name"), field("StartDate"), field("EndDate"),
                     field("TermType", "picklist", picklist=["Semester", "Quarter"])],
    "LearningProgram": [field("Name"), field("ProviderId")],
    "LearningCourse": [field("Name"), field("CourseNumber"), field("ProviderId")],
    "CourseOffering": [field(n) for n in ["Name", "LearningCourseId", "AcademicTermId", "StartDate", "EndDate", "PrimaryFacultyId"]],
    "ContactProfile": [field("ContactId"), field("Type", "picklist", picklist=["Student", "Faculty", "Staff"])],
    "LearnerProgram": [field(n) for n in ["Name", "LearnerContactId", "LearningProgramId", "AcademicTermId", "Status"]],
    "CourseOfferingParticipant": [field(n) for n in ["ParticipantContactId", "CourseOfferingId", "ParticipationStatus"]],
    "AccountContactRelation": [field(n) for n in ["AccountId", "ContactId", "IsActive"]],
}


class FakeObject:
    def __init__(self, name):
        self.name = name

    def describe(self):
        if self.name not in FAKE_SCHEMA:
            raise Exception("NOT_FOUND")
        return {"fields": FAKE_SCHEMA[self.name]}


class FakeSF:
    def __init__(self):
        self.counter = itertools.count(1)
        self.inserted = {}
        self.deleted = []

    def __getattr__(self, name):
        return FakeObject(name)

    def restful(self, path, method="GET", json=None, params=None):
        if method == "POST":
            out = []
            for rec in json["records"]:
                obj = rec["attributes"]["type"]
                self.inserted.setdefault(obj, []).append(rec)
                out.append({"success": True, "id": f"{obj[:3]}{next(self.counter):012d}"})
            return out
        ids = params["ids"].split(",")
        self.deleted.extend(ids)
        return [{"success": True} for _ in ids]

    def query(self, soql):
        return {"records": [{"Id": "012PERSON"}]}

    def query_all(self, soql):
        ids = soql.split("IN (")[1].rstrip(")").replace("'", "").split(",")
        return {"records": [{"Id": i, "PersonContactId": "003" + i} for i in ids]}


def test_generated_counts_and_unique_emails():
    fake = generate.make_faker()
    students = generate.students(fake, 100)
    faculty = generate.faculty(fake, 20)
    assert len(students) == 100 and len(faculty) == 20
    emails = [p["email"] for p in students + faculty]
    assert len(set(emails)) == len(emails)
    assert all(e.endswith(config.EMAIL_DOMAIN) for e in emails)


def test_clean_drops_unknown_fields_and_fixes_picklists():
    schema = Schema(FakeSF())
    cleaned = schema.clean("AcademicTerm", {"Name": "T1", "TermType": "Term", "Bogus__c": 1})
    assert cleaned == {"Name": "T1", "TermType": "Semester"}


def test_full_seed_and_teardown(tmp_path):
    sf = FakeSF()
    manifest = Manifest(str(tmp_path / "m.json"))
    loader = Loader(sf, manifest)
    loader.run()

    people = config.STUDENT_COUNT + config.FACULTY_COUNT + config.MARKETING_STAFF_COUNT
    accounts = 1 + len(config.DEPARTMENTS) + people
    assert len(sf.inserted["Account"]) == accounts
    assert len(sf.inserted["ContactProfile"]) == people
    assert len(sf.inserted["LearnerProgram"]) == config.STUDENT_COUNT
    assert len(sf.inserted["CourseOffering"]) == len(config.COURSES) * len(config.ACADEMIC_TERMS)
    assert len(sf.inserted["CourseOfferingParticipant"]) == config.STUDENT_COUNT * config.COURSES_PER_STUDENT
    assert len(sf.inserted["AccountContactRelation"]) == config.FACULTY_COUNT + config.MARKETING_STAFF_COUNT
    assert loader.failures == 0

    created = sum(len(s["ids"]) for s in manifest.steps)
    teardown(sf, manifest)
    assert len(sf.deleted) == created
    assert manifest.is_empty()
