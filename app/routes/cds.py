from fastapi import APIRouter, Query
from typing import Optional
import random
from app.data.cds_pyq import CDS_PYQ, CDS_SUBJECTS
from app.admin.database import get_custom_questions

router = APIRouter()


def shuffle_options(q: dict) -> dict:
    """
    Shuffle the options of a question using its ID as seed so:
    - Same question always shows same shuffled order (deterministic)
    - But answer is NOT always at position B/C — spread across A/B/C/D
    """
    if not q.get("options") or not q.get("answer"):
        return q

    opts = list(q["options"])
    correct = q["answer"]

    # Use question ID as seed — deterministic but unique per question
    rng = random.Random(q.get("id", 0) * 7 + 13)
    rng.shuffle(opts)

    return {**q, "options": opts, "answer": correct}


@router.get("/subjects")
def get_cds_subjects():
    """Return all CDS subjects with metadata."""
    return {"subjects": CDS_SUBJECTS}


@router.get("/subjects/{subject_name}/topics")
def get_subject_topics(subject_name: str):
    """Return topics for a given CDS subject."""
    subject = next(
        (v for k, v in CDS_SUBJECTS.items() if k.lower().replace(" ", "-") == subject_name.lower()),
        None
    )
    if not subject:
        return {"error": "Subject not found"}
    return {"subject": subject_name, **subject}


@router.get("/pyq")
def get_cds_pyq(
    subject: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    paper: Optional[str] = Query(None),
):
    results = CDS_PYQ + get_custom_questions()

    if subject:
        results = [q for q in results if subject.lower() in q["subject"].lower()]
    if topic:
        results = [q for q in results if topic.lower() in q["topic"].lower()]
    if year:
        results = [q for q in results if q["year"] == year]
    if paper:
        results = [q for q in results if q.get("paper", "").upper() == paper.upper()]

    return {
        "total": len(results),
        "filters": {"subject": subject, "topic": topic, "year": year, "paper": paper},
        "questions": [shuffle_options(q) for q in results]
    }


@router.get("/pyq/stats")
def get_cds_pyq_stats():
    """Return stats: years available, subjects, topics with counts."""
    years = sorted(list(set(q["year"] for q in CDS_PYQ)), reverse=True)
    subjects = {}
    for q in CDS_PYQ:
        s = q["subject"]
        t = q["topic"]
        if s not in subjects:
            subjects[s] = {"total": 0, "topics": {}}
        subjects[s]["total"] += 1
        subjects[s]["topics"][t] = subjects[s]["topics"].get(t, 0) + 1

    return {
        "total_questions": len(CDS_PYQ),
        "years": years,
        "year_range": f"{min(years)}–{max(years)}",
        "subjects": subjects
    }


@router.get("/pyq/topic-wise")
def get_topic_wise_breakdown():
    """Return all questions grouped by subject → topic."""
    grouped = {}
    for q in CDS_PYQ:
        s = q["subject"]
        t = q["topic"]
        if s not in grouped:
            grouped[s] = {}
        if t not in grouped[s]:
            grouped[s][t] = []
        grouped[s][t].append(shuffle_options(q))
    return {"data": grouped}
