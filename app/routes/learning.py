from fastapi import APIRouter, Body
from typing import List

router = APIRouter()

STUDY_PLANS = {
    "cds": {
        "exam": "CDS",
        "duration_weeks": 12,
        "weekly_plan": [
            {"week": "1-2", "focus": "English Grammar & Vocabulary", "hours_per_day": 3},
            {"week": "3-4", "focus": "Elementary Mathematics - Arithmetic", "hours_per_day": 4},
            {"week": "5-6", "focus": "General Knowledge - History & Geography", "hours_per_day": 3},
            {"week": "7-8", "focus": "Mathematics - Algebra & Geometry", "hours_per_day": 4},
            {"week": "9-10", "focus": "GK - Polity, Economy, Science", "hours_per_day": 3},
            {"week": "11-12", "focus": "Full Mock Tests & PYQ Practice", "hours_per_day": 5}
        ]
    },
    "nda": {
        "exam": "NDA",
        "duration_weeks": 16,
        "weekly_plan": [
            {"week": "1-3", "focus": "Mathematics - Algebra & Calculus", "hours_per_day": 4},
            {"week": "4-6", "focus": "Mathematics - Trigonometry & Vectors", "hours_per_day": 4},
            {"week": "7-9", "focus": "General Ability - English", "hours_per_day": 3},
            {"week": "10-12", "focus": "General Ability - GK (Science, History)", "hours_per_day": 3},
            {"week": "13-14", "focus": "Current Affairs & Defence GK", "hours_per_day": 2},
            {"week": "15-16", "focus": "Mock Tests & Revision", "hours_per_day": 5}
        ]
    },
    "afcat": {
        "exam": "AFCAT",
        "duration_weeks": 10,
        "weekly_plan": [
            {"week": "1-2", "focus": "Verbal Ability & English", "hours_per_day": 3},
            {"week": "3-4", "focus": "Numerical Ability & Maths", "hours_per_day": 3},
            {"week": "5-6", "focus": "Reasoning & Military Aptitude", "hours_per_day": 3},
            {"week": "7-8", "focus": "General Awareness & Current Affairs", "hours_per_day": 3},
            {"week": "9-10", "focus": "Mock Tests & PYQ Revision", "hours_per_day": 5}
        ]
    }
}

RESOURCES = [
    {"title": "Pathfinder CDS Entrance Examination", "type": "Book", "exam": "cds", "author": "Arihant Experts"},
    {"title": "NDA/NA Mathematics", "type": "Book", "exam": "nda", "author": "R.S. Aggarwal"},
    {"title": "AFCAT Guide", "type": "Book", "exam": "afcat", "author": "Arihant Experts"},
    {"title": "Lucent's General Knowledge", "type": "Book", "exam": "all", "author": "Lucent Publications"},
    {"title": "Word Power Made Easy", "type": "Book", "exam": "all", "author": "Norman Lewis"},
    {"title": "UPSC Official Website", "type": "Website", "exam": "cds,nda", "url": "https://upsc.gov.in"},
    {"title": "IAF Official Website", "type": "Website", "exam": "afcat", "url": "https://afcat.cdac.in"},
    {"title": "SSBCrack", "type": "Website", "exam": "ssb", "url": "https://ssbcrack.com"}
]

@router.get("/study-plan/{exam_id}")
def get_study_plan(exam_id: str):
    plan = STUDY_PLANS.get(exam_id.lower())
    if not plan:
        return {"error": "Study plan not found for this exam"}
    return plan

@router.get("/resources")
def get_resources(exam: str = None):
    if exam:
        filtered = [r for r in RESOURCES if exam.lower() in r["exam"]]
        return {"resources": filtered}
    return {"resources": RESOURCES}

@router.post("/quiz/submit")
def submit_quiz(answers: dict = Body(...)):
    """Simple quiz scoring endpoint"""
    correct = answers.get("correct", 0)
    total = answers.get("total", 0)
    score = (correct / total * 100) if total > 0 else 0
    
    if score >= 80:
        level = "Excellent"
        message = "Outstanding performance! You're well prepared."
    elif score >= 60:
        level = "Good"
        message = "Good work! Focus on weak areas to improve further."
    elif score >= 40:
        level = "Average"
        message = "Keep practicing. Review the topics you got wrong."
    else:
        level = "Needs Improvement"
        message = "Don't give up! Revise basics and attempt more PYQs."
    
    return {
        "score": round(score, 2),
        "correct": correct,
        "total": total,
        "level": level,
        "message": message
    }

@router.get("/daily-challenge")
def daily_challenge():
    return {
        "question": "Which organisation conducts the CDS examination?",
        "options": ["Ministry of Defence", "UPSC", "CDAC", "NDA Board"],
        "answer": "UPSC",
        "explanation": "The Union Public Service Commission (UPSC) conducts the CDS exam twice a year.",
        "topic": "Defence GK",
        "difficulty": "Easy"
    }
