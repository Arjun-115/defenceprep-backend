from fastapi import APIRouter, Query
from typing import Optional
import random

router = APIRouter()

def _shuffle_q(q: dict) -> dict:
    if not q.get("options") or not q.get("answer"):
        return q
    opts = list(q["options"])
    correct = q["answer"]
    rng = random.Random(q.get("id", 0) * 7 + 13)
    rng.shuffle(opts)
    return {**q, "options": opts, "answer": correct}

PYQ_DATA = [
    {
        "id": 1, "exam": "cds", "year": 2023, "subject": "General Knowledge",
        "question": "Which battle is considered the first major battle of the Indian Rebellion of 1857?",
        "options": ["Battle of Plassey", "Battle of Meerut", "Battle of Delhi", "Battle of Lucknow"],
        "answer": "Battle of Meerut",
        "explanation": "The Indian Rebellion of 1857 began at Meerut on May 10, 1857."
    },
    {
        "id": 2, "exam": "cds", "year": 2023, "subject": "Elementary Mathematics",
        "question": "If the sum of two numbers is 20 and their product is 96, find the numbers.",
        "options": ["8 and 12", "6 and 14", "10 and 10", "4 and 16"],
        "answer": "8 and 12",
        "explanation": "x+y=20, xy=96 → x²-20x+96=0 → (x-8)(x-12)=0 → x=8,12"
    },
    {
        "id": 3, "exam": "nda", "year": 2023, "subject": "Mathematics",
        "question": "The value of sin 30° + cos 60° is:",
        "options": ["0", "1", "√3/2", "1/2"],
        "answer": "1",
        "explanation": "sin 30° = 0.5 and cos 60° = 0.5, so sum = 1"
    },
    {
        "id": 4, "exam": "afcat", "year": 2022, "subject": "General Awareness",
        "question": "Which is the highest gallantry award in India?",
        "options": ["Param Vir Chakra", "Vir Chakra", "Ashoka Chakra", "Kirti Chakra"],
        "answer": "Param Vir Chakra",
        "explanation": "Param Vir Chakra is India's highest wartime military decoration."
    },
    {
        "id": 5, "exam": "nda", "year": 2022, "subject": "General Ability",
        "question": "Who was the first Chief of Defence Staff (CDS) of India?",
        "options": ["General Bipin Rawat", "General MM Naravane", "Admiral Karambir Singh", "Air Marshal RKS Bhadauria"],
        "answer": "General Bipin Rawat",
        "explanation": "Gen Bipin Rawat became India's first CDS on January 1, 2020."
    },
    {
        "id": 6, "exam": "cds", "year": 2022, "subject": "English",
        "question": "Choose the correct synonym for 'Valiant':",
        "options": ["Cowardly", "Brave", "Weak", "Timid"],
        "answer": "Brave",
        "explanation": "Valiant means showing courage and determination, synonym is Brave."
    },
    {
        "id": 7, "exam": "afcat", "year": 2023, "subject": "Numerical Ability",
        "question": "A train 150m long passes a pole in 15 seconds. Find the speed of the train.",
        "options": ["10 m/s", "36 km/h", "Both A and B", "None"],
        "answer": "Both A and B",
        "explanation": "Speed = 150/15 = 10 m/s = 10×3.6 = 36 km/h"
    },
    {
        "id": 8, "exam": "na", "year": 2023, "subject": "Science",
        "question": "What is the SI unit of electric current?",
        "options": ["Volt", "Watt", "Ampere", "Ohm"],
        "answer": "Ampere",
        "explanation": "The SI unit of electric current is Ampere (A)."
    }
]

@router.get("/")
def get_pyq(
    exam: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    subject: Optional[str] = Query(None)
):
    results = PYQ_DATA
    if exam:
        results = [q for q in results if q["exam"] == exam.lower()]
    if year:
        results = [q for q in results if q["year"] == year]
    if subject:
        results = [q for q in results if subject.lower() in q["subject"].lower()]
    return {"total": len(results), "questions": [_shuffle_q(q) for q in results]}

@router.get("/exams")
def get_pyq_exams():
    exams = list(set(q["exam"] for q in PYQ_DATA))
    years = sorted(list(set(q["year"] for q in PYQ_DATA)), reverse=True)
    return {"exams": exams, "years": years}
