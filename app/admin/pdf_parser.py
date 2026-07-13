"""
PDF Parser — extracts questions from uploaded PDFs.
Supports two formats:
1. Structured: Q. <text> (A) opt (B) opt (C) opt (D) opt Ans: X
2. Plain text extraction with heuristic detection
"""
import re
import pdfplumber
from typing import List, Dict
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from PDF bytes."""
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def parse_questions_from_text(text: str, subject: str = "General Knowledge",
                               exam: str = "cds", year: int = 2024,
                               paper: str = "I") -> List[Dict]:
    """
    Heuristic parser for MCQ questions from extracted PDF text.
    Looks for patterns like:
      1. Question text
      (a) Option A  (b) Option B  (c) Option C  (d) Option D
      Ans: (b) or Answer: b
    """
    questions = []
    lines = text.replace('\r', '').split('\n')
    cleaned = [l.strip() for l in lines if l.strip()]
    full_text = '\n'.join(cleaned)

    # Pattern 1: numbered questions with (a)(b)(c)(d) options
    pattern = re.compile(
        r'(\d+)[.)]\s+(.+?)\n'
        r'(?:\(a\)|a[.)]\s*)(.+?)\n'
        r'(?:\(b\)|b[.)]\s*)(.+?)\n'
        r'(?:\(c\)|c[.)]\s*)(.+?)\n'
        r'(?:\(d\)|d[.)]\s*)(.+?)\n'
        r'(?:ans(?:wer)?[:\s]*(?:\()?([a-dA-D])(?:\))?)',
        re.IGNORECASE | re.DOTALL
    )

    matches = pattern.findall(full_text)
    base_id = 90000

    for i, m in enumerate(matches):
        num, qtext, a, b, c, d, ans = m
        ans = ans.strip().lower()
        options = [a.strip(), b.strip(), c.strip(), d.strip()]
        ans_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        answer = options[ans_map.get(ans, 0)] if ans in ans_map else options[0]

        # Detect topic from question content
        topic = detect_topic(qtext, subject)

        questions.append({
            "id": base_id + i,
            "exam": exam,
            "year": year,
            "paper": paper,
            "subject": subject,
            "topic": topic,
            "question": qtext.strip(),
            "options": options,
            "answer": answer,
            "explanation": f"From uploaded PDF. Answer: ({ans.upper()}) {answer}",
            "source": "pdf_upload",
        })

    # Pattern 2: simpler format without answer markers — just extract Q+options
    if not questions:
        questions = parse_simple_format(cleaned, subject, exam, year, paper, base_id)

    return questions


def parse_simple_format(lines: List[str], subject: str, exam: str,
                         year: int, paper: str, base_id: int) -> List[Dict]:
    """Fallback: detect question blocks heuristically."""
    questions = []
    i = 0
    q_count = 0

    while i < len(lines):
        line = lines[i]
        # Detect question start: starts with number or "Q."
        q_match = re.match(r'^(?:Q\.?\s*)?(\d+)[.)]\s*(.+)', line)
        if q_match:
            qtext = q_match.group(2)
            options = []
            i += 1
            # Collect up to 4 options
            while i < len(lines) and len(options) < 4:
                opt = lines[i]
                opt_match = re.match(r'^\(?([a-dA-D])[.)]\s*(.+)', opt)
                if opt_match:
                    options.append(opt_match.group(2).strip())
                    i += 1
                elif re.match(r'^\d+[.)]', opt):
                    break
                else:
                    if options:
                        break
                    i += 1

            if len(options) >= 2:
                topic = detect_topic(qtext, subject)
                questions.append({
                    "id": base_id + q_count,
                    "exam": exam, "year": year, "paper": paper,
                    "subject": subject, "topic": topic,
                    "question": qtext.strip(),
                    "options": options if len(options) == 4 else options + [""] * (4 - len(options)),
                    "answer": options[0],
                    "explanation": "From uploaded PDF.",
                    "source": "pdf_upload",
                })
                q_count += 1
        else:
            i += 1

    return questions


def detect_topic(text: str, subject: str) -> str:
    """Guess topic from question text."""
    text_lower = text.lower()
    if subject == "English":
        if any(w in text_lower for w in ["synonym", "similar meaning", "means the same"]):
            return "Synonyms"
        if any(w in text_lower for w in ["antonym", "opposite"]):
            return "Antonyms"
        if any(w in text_lower for w in ["error", "incorrect", "correct the"]):
            return "Spotting Errors"
        if any(w in text_lower for w in ["idiom", "phrase", "means"]):
            return "Idioms & Phrases"
        if any(w in text_lower for w in ["blank", "fill in"]):
            return "Fill in the Blanks"
        return "Comprehension"
    elif subject == "Elementary Mathematics":
        if any(w in text_lower for w in ["profit", "loss", "cost price", "selling"]):
            return "Profit & Loss"
        if any(w in text_lower for w in ["interest", "principal", "rate"]):
            return "Simple & Compound Interest"
        if any(w in text_lower for w in ["speed", "distance", "train", "time"]):
            return "Speed, Time & Distance"
        if any(w in text_lower for w in ["triangle", "circle", "angle", "polygon"]):
            return "Geometry"
        if any(w in text_lower for w in ["sin", "cos", "tan", "trigon"]):
            return "Trigonometry"
        if any(w in text_lower for w in ["area", "volume", "perimeter", "surface"]):
            return "Mensuration"
        if any(w in text_lower for w in ["percent", "%"]):
            return "Percentage"
        return "Arithmetic"
    else:  # GK
        if any(w in text_lower for w in ["battle", "war", "revolt", "mughal", "british", "independence"]):
            return "History"
        if any(w in text_lower for w in ["river", "mountain", "state", "capital", "ocean", "pass"]):
            return "Geography"
        if any(w in text_lower for w in ["article", "constitution", "parliament", "president", "lok sabha"]):
            return "Polity"
        if any(w in text_lower for w in ["missile", "drdo", "navy", "army", "air force", "ins ", "operation"]):
            return "Defence Current Affairs"
        if any(w in text_lower for w in ["gdp", "inflation", "rbi", "tax", "economy"]):
            return "Economy"
        if any(w in text_lower for w in ["element", "atom", "force", "energy", "cell", "dna", "planet"]):
            return "Science & Technology"
        return "General Knowledge"
