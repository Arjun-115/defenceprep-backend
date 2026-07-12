from fastapi import APIRouter

router = APIRouter()

EXAMS = [
    {
        "id": "cds",
        "name": "CDS",
        "full_name": "Combined Defence Services",
        "description": "Written exam for IMA, INA, AFA, and OTA conducted by UPSC.",
        "eligibility": "Graduate degree, Age 19-25",
        "syllabus": ["English", "General Knowledge", "Elementary Mathematics"],
        "icon": "⚔️"
    },
    {
        "id": "afcat",
        "name": "AFCAT",
        "full_name": "Air Force Common Admission Test",
        "description": "Entry to Indian Air Force as Flying and Ground Duty Officer.",
        "eligibility": "Graduate/Engineering, Age 20-26",
        "syllabus": ["General Awareness", "Verbal Ability", "Numerical Ability", "Reasoning"],
        "icon": "✈️"
    },
    {
        "id": "nda",
        "name": "NDA",
        "full_name": "National Defence Academy",
        "description": "Entry to Army, Navy and Air Force wings of NDA.",
        "eligibility": "Class 12 pass, Age 16.5-19.5",
        "syllabus": ["Mathematics", "General Ability Test"],
        "icon": "🛡️"
    },
    {
        "id": "na",
        "name": "Navy",
        "full_name": "Indian Navy Exam",
        "description": "Various entries into Indian Navy as officer and sailor.",
        "eligibility": "Graduate/Engineering, Age 19-25",
        "syllabus": ["Mathematics", "Science", "General Knowledge", "English"],
        "icon": "⚓"
    },
    {
        "id": "territorial",
        "name": "TA",
        "full_name": "Territorial Army",
        "description": "Part-time soldiering for employed civilians.",
        "eligibility": "Graduate, Age 18-42, Employed",
        "syllabus": ["Reasoning", "Elementary Mathematics", "GK", "English"],
        "icon": "🎖️"
    }
]

@router.get("/")
def get_exams():
    return {"exams": EXAMS}

@router.get("/{exam_id}")
def get_exam(exam_id: str):
    exam = next((e for e in EXAMS if e["id"] == exam_id), None)
    if not exam:
        return {"error": "Exam not found"}
    return exam
