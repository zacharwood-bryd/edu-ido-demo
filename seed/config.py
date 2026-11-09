"""Settings for the seed run. Change the numbers here, not in the loader."""

# How many people of each persona to create.
STUDENT_COUNT = 100
FACULTY_COUNT = 20
MARKETING_STAFF_COUNT = 5

# The fictional UK university the demo is built around.
UNIVERSITY_NAME = "Northfield University"
EMAIL_DOMAIN = "northfield.example.ac.uk"

# Faculty and staff are Contacts under these department (business) accounts.
DEPARTMENTS = [
    "School of Computer Science",
    "School of Business and Management",
    "School of Psychology",
    "School of Engineering",
    "Marketing and Student Recruitment",
]

# Degree programmes. Each student is enrolled on one.
# "school" must match a name in DEPARTMENTS.
PROGRAMMES = [
    {"name": "BSc Computer Science", "school": "School of Computer Science"},
    {"name": "BSc Data Science", "school": "School of Computer Science"},
    {"name": "BA Business Management", "school": "School of Business and Management"},
    {"name": "BSc Psychology", "school": "School of Psychology"},
    {"name": "MEng Mechanical Engineering", "school": "School of Engineering"},
    # The marketing persona's scene builds a campaign for this short course.
    {"name": "AI Leadership (Short Course)", "school": "School of Business and Management"},
]

# Courses (modules). Each is offered once per term in ACADEMIC_TERMS.
COURSES = [
    {"name": "Introduction to Programming", "code": "CS101", "school": "School of Computer Science"},
    {"name": "Machine Learning Foundations", "code": "CS210", "school": "School of Computer Science"},
    {"name": "Principles of Marketing", "code": "BM110", "school": "School of Business and Management"},
    {"name": "Leading with AI", "code": "BM305", "school": "School of Business and Management"},
    {"name": "Cognitive Psychology", "code": "PS120", "school": "School of Psychology"},
    {"name": "Thermodynamics", "code": "EN201", "school": "School of Engineering"},
]

# UK academic year 2026/27.
ACADEMIC_TERMS = [
    {"name": "Autumn Term 2026", "start": "2026-09-28", "end": "2026-12-11"},
    {"name": "Spring Term 2027", "start": "2027-01-11", "end": "2027-03-26"},
]

# Each student takes this many course offerings in the current term.
COURSES_PER_STUDENT = 3

# A fixed seed makes Faker produce the same people on every run.
RANDOM_SEED = 2026

# Records the seed creates are written here so teardown can delete exactly them.
MANIFEST_PATH = "seed_manifest.json"
