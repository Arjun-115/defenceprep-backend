"""
Simple JSON file-based database for admin-managed content.
Stores: custom questions, study materials, current affairs, site settings.
"""
import json, os
from typing import List, Dict, Any
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "db")
os.makedirs(DB_DIR, exist_ok=True)

def _path(name: str) -> str:
    return os.path.join(DB_DIR, f"{name}.json")

def _read(name: str, default=None) -> Any:
    path = _path(name)
    if not os.path.exists(path):
        return default if default is not None else []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(name: str, data: Any):
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Questions ──────────────────────────────────────────────
def get_custom_questions() -> List[Dict]:
    return _read("custom_questions", [])

def save_question(q: Dict) -> Dict:
    questions = get_custom_questions()
    if "id" not in q or not q["id"]:
        max_id = max((x.get("id", 0) for x in questions), default=9000)
        q["id"] = max_id + 1
    q["created_at"] = datetime.utcnow().isoformat()
    q["source"] = q.get("source", "admin")
    existing = next((i for i, x in enumerate(questions) if x["id"] == q["id"]), None)
    if existing is not None:
        questions[existing] = q
    else:
        questions.append(q)
    _write("custom_questions", questions)
    return q

def delete_question(qid: int) -> bool:
    questions = get_custom_questions()
    new_q = [x for x in questions if x["id"] != qid]
    if len(new_q) == len(questions):
        return False
    _write("custom_questions", new_q)
    return True

def get_all_questions_combined():
    from app.data.cds_pyq import CDS_PYQ
    custom = get_custom_questions()
    return CDS_PYQ + custom

# ── Study Materials ────────────────────────────────────────
def get_materials() -> List[Dict]:
    return _read("materials", [])

def save_material(m: Dict) -> Dict:
    materials = get_materials()
    if "id" not in m or not m["id"]:
        max_id = max((x.get("id", 0) for x in materials), default=0)
        m["id"] = max_id + 1
    m["created_at"] = datetime.utcnow().isoformat()
    existing = next((i for i, x in enumerate(materials) if x["id"] == m["id"]), None)
    if existing is not None:
        materials[existing] = m
    else:
        materials.append(m)
    _write("materials", materials)
    return m

def delete_material(mid: int) -> bool:
    materials = get_materials()
    new_m = [x for x in materials if x["id"] != mid]
    if len(new_m) == len(materials):
        return False
    _write("materials", new_m)
    return True

# ── Current Affairs ────────────────────────────────────────
def get_custom_ca() -> List[Dict]:
    return _read("current_affairs_custom", [])

def save_ca(ca: Dict) -> Dict:
    items = get_custom_ca()
    if "id" not in ca or not ca["id"]:
        max_id = max((x.get("id", 0) for x in items), default=200)
        ca["id"] = max_id + 1
    ca["created_at"] = datetime.utcnow().isoformat()
    items.append(ca)
    _write("current_affairs_custom", items)
    return ca

# ── Site Settings ──────────────────────────────────────────
def get_settings() -> Dict:
    return _read("settings", {
        "site_name": "DefencePrep AI",
        "tagline": "Crack Your Defence Exam",
        "announcement": "",
        "maintenance_mode": False,
        "total_users": 0,
        "contact_email": "",
    })

def save_settings(s: Dict) -> Dict:
    _write("settings", s)
    return s

# ── PDF Uploads ────────────────────────────────────────────
def get_uploads() -> List[Dict]:
    return _read("uploads", [])

def save_upload(u: Dict) -> Dict:
    uploads = get_uploads()
    uploads.append(u)
    _write("uploads", uploads)
    return u
