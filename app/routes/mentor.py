from fastapi import APIRouter, Body
from typing import List, Dict
from app.data.cds_pyq import CDS_PYQ

router = APIRouter()

# ── Topic difficulty map ──────────────────────────────────────
TOPIC_DIFFICULTY = {
    "Synonyms": "Easy", "Antonyms": "Easy", "Fill in the Blanks": "Easy",
    "Idioms & Phrases": "Medium", "One-Word Substitution": "Medium",
    "Spotting Errors": "Medium", "Sentence Improvement": "Medium",
    "Ordering of Sentences": "Hard", "Comprehension": "Hard",
    "Number System": "Easy", "Arithmetic": "Medium", "Percentage": "Medium",
    "Ratio & Proportion": "Medium", "Simple & Compound Interest": "Medium",
    "Profit & Loss": "Medium", "Time & Work": "Medium",
    "Speed, Time & Distance": "Medium", "Algebra": "Hard",
    "Geometry": "Hard", "Trigonometry": "Hard", "Mensuration": "Hard",
    "Statistics": "Medium",
    "History": "Medium", "Geography": "Medium", "Polity": "Medium",
    "Economy": "Medium", "Science & Technology": "Medium",
    "Defence Current Affairs": "Easy", "Sports": "Easy",
    "Books & Authors": "Easy", "Environment": "Medium",
    "International Affairs": "Medium",
}

# ── Smart mentor tips per topic ───────────────────────────────
MENTOR_TIPS = {
    "Synonyms": [
        "Read 10 new words daily from 'Word Power Made Easy' by Norman Lewis.",
        "Make flashcards — write the word on front, synonym + sentence on back.",
        "CDS repeats words like Valiant, Diligent, Frugal — focus on these.",
        "Use the word in a sentence to remember it better than just memorising.",
    ],
    "Antonyms": [
        "Learn words in antonym pairs — e.g., Verbose ↔ Terse, Benevolent ↔ Malevolent.",
        "Prefix tricks: un-, in-, im-, dis-, non- often form antonyms.",
        "Revise 5 antonym pairs every night before sleeping.",
    ],
    "Fill in the Blanks": [
        "Read the full sentence before choosing — context matters most.",
        "Eliminate clearly wrong options first to narrow down choices.",
        "Focus on collocations — words that naturally go together.",
    ],
    "Spotting Errors": [
        "Focus on Subject-Verb Agreement — it's the most tested rule.",
        "Remember: 'Neither/Either' takes singular verb. 'As well as' doesn't change subject.",
        "Present perfect clashes with past time words (yesterday, ago) — common trap.",
        "Practice 10 error spotting questions daily for 30 days.",
    ],
    "Sentence Improvement": [
        "Know the 'Too...to' and 'So...that' constructions thoroughly.",
        "Double negatives are always wrong — 'cannot help but not' is incorrect.",
        "Brush up on preposition usage: insist on, look forward to, afraid of.",
    ],
    "Idioms & Phrases": [
        "Learn 5 idioms daily with their exact meaning and an example sentence.",
        "Military idioms appear frequently — bite the bullet, hold the fort.",
        "Group idioms by theme: body parts, animals, colours — easier to remember.",
    ],
    "One-Word Substitution": [
        "Focus on phobias, -cide words, -ology words — CDS loves these.",
        "Make a dedicated notebook: word → meaning → sentence.",
        "Revise government/political terms: Plutocracy, Theocracy, Autocracy.",
    ],
    "Algebra": [
        "Master identities: (a+b)², (a-b)², a³+b³ — appear every exam.",
        "Practice solving simultaneous equations by elimination and substitution.",
        "For quadratic equations, memorise the factorisation method.",
    ],
    "Arithmetic": [
        "Practice percentage, ratio and average questions daily — they form 40% of paper.",
        "Speed: learn shortcut tables up to 30 and squares up to 30.",
        "For series problems, find the difference pattern first.",
    ],
    "Geometry": [
        "Memorise all circle theorems — tangent-radius angle, inscribed angle theorem.",
        "Triangle properties are tested heavily — medians, altitudes, angle bisectors.",
        "Practice coordinate geometry alongside — it overlaps with algebra.",
    ],
    "Trigonometry": [
        "Memorise the table: sin/cos/tan for 0°, 30°, 45°, 60°, 90°.",
        "Identities: sin²+cos²=1, 1+tan²=sec², 1+cot²=cosec² — must know.",
        "Height and distance problems always appear — practice shadow problems.",
    ],
    "History": [
        "Focus on Modern Indian History (1757–1947) — most questions come from here.",
        "Make a timeline: Battles → Revolts → Freedom Movement → Independence.",
        "Military history: Battles of Panipat, Kargil, 1971 war are high-frequency.",
    ],
    "Geography": [
        "Study India's physical features: rivers, passes, coasts, islands.",
        "Memorise important straits, gulfs, and their strategic significance.",
        "World geography: continents, oceans, longest rivers, highest peaks.",
    ],
    "Polity": [
        "The Constitution's structure: Parts, Schedules, Fundamental Rights (Part III).",
        "Emergency provisions (Articles 352, 356, 360) are frequently tested.",
        "Focus on constitutional amendments: 42nd, 44th, 73rd, 74th, 86th.",
    ],
    "Science & Technology": [
        "Physics: Newton's laws, optics, electricity — basics are enough.",
        "Chemistry: chemical symbols, pH scale, common compounds.",
        "Defence technology: missiles (Prithvi, Agni, BrahMos), satellites, indigenisation.",
    ],
    "Defence Current Affairs": [
        "Follow PIB (Press Information Bureau) for defence news.",
        "Know all military exercises India participates in — with which country.",
        "Memorise mottos of Army, Navy, Air Force and their HQ locations.",
    ],
}

def get_weak_topics(answers: List[Dict]) -> Dict:
    """Analyse answers and return topic-wise performance."""
    topic_stats = {}
    for a in answers:
        topic = a.get("topic", "Unknown")
        correct = a.get("correct", False)
        if topic not in topic_stats:
            topic_stats[topic] = {"attempted": 0, "correct": 0, "wrong": 0}
        topic_stats[topic]["attempted"] += 1
        if correct:
            topic_stats[topic]["correct"] += 1
        else:
            topic_stats[topic]["wrong"] += 1

    for t in topic_stats:
        s = topic_stats[t]
        s["accuracy"] = round(s["correct"] / s["attempted"] * 100) if s["attempted"] > 0 else 0
        s["difficulty"] = TOPIC_DIFFICULTY.get(t, "Medium")

    return topic_stats


@router.post("/analyse")
def analyse_performance(payload: dict = Body(...)):
    """
    Accepts quiz answers and returns full analysis + mentor advice.
    payload: { answers: [{topic, subject, correct, year, question_id}] }
    """
    answers = payload.get("answers", [])
    if not answers:
        return {"error": "No answers provided"}

    topic_stats = get_weak_topics(answers)
    total = len(answers)
    correct_total = sum(1 for a in answers if a.get("correct"))
    score_pct = round(correct_total / total * 100) if total else 0

    # Categorise topics
    weak   = [t for t, s in topic_stats.items() if s["accuracy"] < 50]
    medium = [t for t, s in topic_stats.items() if 50 <= s["accuracy"] < 75]
    strong = [t for t, s in topic_stats.items() if s["accuracy"] >= 75]

    # Overall level
    if score_pct >= 80:
        level = "Excellent"
        overall_msg = "Outstanding! You are well-prepared. Focus on maintaining accuracy under time pressure."
    elif score_pct >= 60:
        level = "Good"
        overall_msg = "Good performance. Strengthen weak topics and you're on track to clear CDS."
    elif score_pct >= 40:
        level = "Average"
        overall_msg = "Room for improvement. Focus on the weak topics below and revise daily."
    else:
        level = "Needs Work"
        overall_msg = "Don't be discouraged. Break your preparation into daily targets and be consistent."

    # Build mentor advice for each weak topic
    mentor_advice = {}
    for topic in (weak + medium):
        tips = MENTOR_TIPS.get(topic, [
            f"Practice more {topic} questions from PYQs.",
            f"Revise {topic} basics from standard textbooks.",
            f"Attempt at least 10 {topic} questions daily.",
        ])
        mentor_advice[topic] = {
            "accuracy": topic_stats[topic]["accuracy"],
            "difficulty": TOPIC_DIFFICULTY.get(topic, "Medium"),
            "tips": tips,
        }

    # Priority study plan
    study_plan = []
    for topic in weak:
        study_plan.append({"topic": topic, "priority": "High", "daily_target": "15 questions/day", "timeframe": "1 week"})
    for topic in medium:
        study_plan.append({"topic": topic, "priority": "Medium", "daily_target": "10 questions/day", "timeframe": "2 weeks"})
    for topic in strong:
        study_plan.append({"topic": topic, "priority": "Maintain", "daily_target": "5 questions/day", "timeframe": "Ongoing"})

    # Recommended next questions (from weak topics)
    recommended_qids = []
    for topic in weak[:3]:
        qs = [q for q in CDS_PYQ if q["topic"] == topic][:5]
        recommended_qids.extend([q["id"] for q in qs])

    return {
        "summary": {
            "total": total,
            "correct": correct_total,
            "wrong": total - correct_total,
            "score_percent": score_pct,
            "level": level,
            "message": overall_msg,
        },
        "topic_performance": topic_stats,
        "categories": {
            "weak": weak,
            "medium": medium,
            "strong": strong,
        },
        "mentor_advice": mentor_advice,
        "study_plan": study_plan,
        "recommended_question_ids": recommended_qids[:15],
    }


@router.get("/tips/{topic}")
def get_topic_tips(topic: str):
    """Get mentor tips for a specific topic."""
    tips = MENTOR_TIPS.get(topic, [
        f"Practice more {topic} questions from PYQs.",
        f"Revise {topic} basics from standard textbooks.",
    ])
    return {
        "topic": topic,
        "difficulty": TOPIC_DIFFICULTY.get(topic, "Medium"),
        "tips": tips,
    }


@router.get("/chat")
def mentor_chat(q: str = ""):
    """Simple rule-based AI mentor chat."""
    q_lower = q.lower()

    if any(w in q_lower for w in ["synonym", "antonym", "vocabulary", "word"]):
        reply = "📚 For vocabulary, read 'Word Power Made Easy' by Norman Lewis daily. Practice 10 synonyms + antonyms every morning. CDS English paper repeats many words — focus on: Valiant, Frugal, Diligent, Belligerent, Magnanimous."
    elif any(w in q_lower for w in ["math", "maths", "algebra", "trigon", "geometry"]):
        reply = "📐 For Mathematics: (1) Master identities first — (a+b)², sin²+cos²=1. (2) Solve 20 questions daily. (3) Focus on Arithmetic (40% of paper), then Geometry & Trigonometry. Use R.S. Aggarwal for practice."
    elif any(w in q_lower for w in ["gk", "general knowledge", "history", "geography", "polity"]):
        reply = "🌍 For GK: (1) Read Lucent's GK cover to cover. (2) For History — focus on Modern India (1857–1947). (3) For Defence GK — follow PIB daily. (4) For Geography — study India's rivers, passes, coasts thoroughly."
    elif any(w in q_lower for w in ["ssb", "interview", "personality"]):
        reply = "🎖️ For SSB: (1) Be consistent in all 5 stages — assessors look for the same personality everywhere. (2) Show OLQs naturally — don't fake. (3) Read newspapers daily. (4) Fill PIQ form very carefully — the IO will question everything you write."
    elif any(w in q_lower for w in ["weak", "improve", "score", "fail", "low"]):
        reply = "💪 To improve your weak areas: (1) Take the Assessment Test to identify exact weak topics. (2) Focus on 2 weak topics at a time. (3) Solve 15 PYQs per weak topic daily. (4) Review explanations of wrong answers — don't skip this step."
    elif any(w in q_lower for w in ["time", "schedule", "plan", "study plan"]):
        reply = "📅 Ideal CDS daily schedule: Morning (6-8 AM) — Maths practice. Forenoon (10 AM-12 PM) — GK reading. Evening (4-6 PM) — English practice. Night (8-9 PM) — PYQ quiz + review. Take Sundays as full mock test day."
    elif any(w in q_lower for w in ["book", "reference", "material", "resource"]):
        reply = "📖 Best books for CDS: (1) English — Word Power Made Easy (Norman Lewis). (2) Maths — Elementary Mathematics by RS Aggarwal. (3) GK — Lucent's GK + Arihant CDS guide. (4) PYQs — Pathfinder CDS by Arihant. Study NCERTs (9th-12th) for Science."
    elif any(w in q_lower for w in ["cds", "exam", "pattern", "syllabus"]):
        reply = "⚔️ CDS Exam Pattern: 3 papers — English (100 marks), GK (100 marks), Maths (100 marks — only for IMA/INA/AFA). Each paper is 2 hours. Negative marking: -0.33 per wrong answer. Cutoff is usually 60-70% combined. Focus on accuracy over speed."
    elif any(w in q_lower for w in ["hello", "hi", "hey", "help"]):
        reply = "👋 Hello! I'm your DefencePrep AI Mentor. I can help you with: study tips, weak topic advice, exam strategy, SSB preparation, and more. Ask me anything like 'How to improve in Maths?' or 'Tips for SSB interview'."
    else:
        reply = f"🤔 Good question! For '{q}' — I suggest: (1) Search PYQs on this topic using the filter above. (2) Take a topic quiz to assess your level. (3) Review explanations carefully after each attempt. Keep going — consistency beats intensity! 💪"

    return {"question": q, "reply": reply}
