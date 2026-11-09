"""Make up realistic UK people with Faker. No Salesforce calls happen here."""

import random

from faker import Faker

from seed import config

FACULTY_TITLES = ["Lecturer", "Senior Lecturer", "Associate Professor", "Professor"]
UK_CITIES = [
    "Leeds", "York", "Manchester", "Sheffield", "Birmingham", "Bristol", "Nottingham",
    "Newcastle upon Tyne", "Liverpool", "London", "Glasgow", "Cardiff", "Hull", "Durham",
]
MARKETING_TITLES = [
    "Head of Marketing",
    "Campaign Manager",
    "Digital Marketing Officer",
    "Student Recruitment Officer",
    "Marketing Data Analyst",
]


def make_faker() -> Faker:
    fake = Faker("en_GB")
    Faker.seed(config.RANDOM_SEED)
    random.seed(config.RANDOM_SEED)
    return fake


def _email(first: str, last: str, n: int) -> str:
    local = f"{first}.{last}{n}".lower().replace(" ", "").replace("'", "")
    return f"{local}@{config.EMAIL_DOMAIN}"


def students(fake: Faker, count: int) -> list[dict]:
    people = []
    for n in range(1, count + 1):
        first, last = fake.first_name(), fake.last_name()
        people.append(
            {
                "persona": "Student",
                "first_name": first,
                "last_name": last,
                "email": _email(first, last, n),
                "phone": fake.phone_number(),
                # Undergraduates, roughly 18 to 24.
                "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=24).isoformat(),
                "student_id": f"NU{2026000 + n}",
                "street": fake.street_address(),
                "city": random.choice(UK_CITIES),
                "postcode": fake.postcode(),
                "programme": random.choice(config.PROGRAMMES)["name"],
            }
        )
    return people


def faculty(fake: Faker, count: int) -> list[dict]:
    schools = sorted({p["school"] for p in config.PROGRAMMES})
    people = []
    for n in range(1, count + 1):
        first, last = fake.first_name(), fake.last_name()
        people.append(
            {
                "persona": "Faculty",
                "first_name": first,
                "last_name": last,
                "email": _email(first, last, n),
                "phone": fake.phone_number(),
                "title": random.choice(FACULTY_TITLES),
                # Cycle through schools so every school has some faculty.
                "department": schools[n % len(schools)],
            }
        )
    return people


def marketing_staff(fake: Faker, count: int) -> list[dict]:
    people = []
    for n in range(1, count + 1):
        first, last = fake.first_name(), fake.last_name()
        people.append(
            {
                "persona": "Staff",
                "first_name": first,
                "last_name": last,
                "email": _email(first, last, n),
                "phone": fake.phone_number(),
                "title": MARKETING_TITLES[(n - 1) % len(MARKETING_TITLES)],
                "department": "Marketing and Student Recruitment",
            }
        )
    return people
