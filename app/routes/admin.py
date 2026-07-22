from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import os, json

from app.admin.auth import require_admin, verify_password, create_token, ADMIN_USERNAME
from app.admin.database import (
    get_custom_questions, save_question, delete_question, get_all_questions_combined,
    get_materials, save_material, delete_material,
    get_custom_ca, save_ca,
    get_settings, save_settings,
    get_uploads, save_upload
)
from app.admin.pdf_parser import extract_text_from_pdf, parse_questions_from_text
from app.data.cds_pyq import CDS_PYQ

router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ── PUBLIC NOTIFICATIONS (no auth) ────────────────────────
@router.get("/public/notifications")
def get_public_notifications():
    settings = get_settings()
    notifs = settings.get("notifications", [
        {"id":1,"text":"CDS II 2024 notification released by UPSC","date":"2024-06-01","type":"exam"},
        {"id":2,"text":"975+ PYQs now available across all subjects","date":"2024-07-01","type":"update"},
        {"id":3,"text":"SSB preparation module updated with latest OLQ guide","date":"2024-07-10","type":"update"},
    ])
    return {"notifications": notifs}

# ── AUTH ───────────────────────────────────────────────────
@router.post("/login")
def admin_login(payload: dict = Body(...)):
    username = payload.get("username", "")
    password = payload.get("password", "")
    if username != ADMIN_USERNAME or not verify_password(password, ""):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": username, "role": "admin"})
    return {"token": token, "username": username, "expires_in": "24h"}

# ── DASHBOARD ──────────────────────────────────────────────
@router.get("/dashboard")
def dashboard(admin=Depends(require_admin)):
    from app.data.cds_pyq import CDS_PYQ
    custom = get_custom_questions()
    materials = get_materials()
    uploads = get_uploads()
    ca = get_custom_ca()
    settings = get_settings()

    subject_counts = {}
    for q in CDS_PYQ + custom:
        s = q.get("subject", "Unknown")
        subject_counts[s] = subject_counts.get(s, 0) + 1

    return {
        "stats": {
            "total_pyq": len(CDS_PYQ),
            "custom_questions": len(custom),
            "total_questions": len(CDS_PYQ) + len(custom),
            "study_materials": len(materials),
            "pdf_uploads": len(uploads),
            "current_affairs": len(ca),
        },
        "subject_breakdown": subject_counts,
        "recent_uploads": uploads[-5:] if uploads else [],
        "site_settings": settings,
    }

# ── QUESTIONS ──────────────────────────────────────────────
@router.get("/questions")
def list_questions(subject: Optional[str] = None, source: Optional[str] = None,
                   page: int = 1, limit: int = 50, admin=Depends(require_admin)):
    all_q = get_all_questions_combined()
    if subject:
        all_q = [q for q in all_q if subject.lower() in q.get("subject","").lower()]
    if source:
        all_q = [q for q in all_q if q.get("source","builtin") == source]
    total = len(all_q)
    start = (page - 1) * limit
    return {"total": total, "page": page, "limit": limit,
            "questions": all_q[start:start+limit]}

@router.post("/questions")
def add_question(q: dict = Body(...), admin=Depends(require_admin)):
    saved = save_question(q)
    return {"message": "Question saved", "question": saved}

@router.put("/questions/{qid}")
def update_question(qid: int, q: dict = Body(...), admin=Depends(require_admin)):
    q["id"] = qid
    saved = save_question(q)
    return {"message": "Question updated", "question": saved}

@router.delete("/questions/{qid}")
def remove_question(qid: int, admin=Depends(require_admin)):
    if not delete_question(qid):
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted"}

# ── PDF UPLOAD ─────────────────────────────────────────────
@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    subject: str = Form("General Knowledge"),
    exam: str = Form("cds"),
    year: int = Form(2024),
    paper: str = Form("I"),
    admin=Depends(require_admin)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    # Save file
    safe_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        f.write(content)

    # Extract text and parse questions
    try:
        text = extract_text_from_pdf(content)
        questions = parse_questions_from_text(text, subject, exam, year, paper)
    except Exception as e:
        questions = []
        text = f"Parse error: {str(e)}"

    # Save each parsed question
    saved_questions = []
    for q in questions:
        saved_questions.append(save_question(q))

    # Record upload
    upload_record = {
        "filename": file.filename,
        "safe_name": safe_name,
        "subject": subject,
        "exam": exam,
        "year": year,
        "questions_extracted": len(saved_questions),
        "uploaded_at": datetime.utcnow().isoformat(),
        "file_size_kb": round(len(content) / 1024, 1),
    }
    save_upload(upload_record)

    return {
        "message": f"PDF uploaded. {len(saved_questions)} questions extracted.",
        "upload": upload_record,
        "questions_preview": saved_questions[:5],
        "extracted_text_preview": text[:500] if text else "",
    }

@router.get("/uploads")
def list_uploads(admin=Depends(require_admin)):
    return {"uploads": get_uploads()}

@router.get("/uploads/public")
def list_uploads_public():
    """Public endpoint — shows uploaded materials (no auth needed for viewing)"""
    uploads = get_uploads()
    return {"uploads": uploads}

# ── STUDY MATERIALS ────────────────────────────────────────
@router.get("/materials")
def list_materials(admin=Depends(require_admin)):
    return {"materials": get_materials()}

@router.post("/materials")
def add_material(m: dict = Body(...), admin=Depends(require_admin)):
    saved = save_material(m)
    return {"message": "Material saved", "material": saved}

@router.put("/materials/{mid}")
def update_material(mid: int, m: dict = Body(...), admin=Depends(require_admin)):
    m["id"] = mid
    saved = save_material(m)
    return {"message": "Material updated", "material": saved}

@router.delete("/materials/{mid}")
def remove_material(mid: int, admin=Depends(require_admin)):
    if not delete_material(mid):
        raise HTTPException(status_code=404, detail="Material not found")
    return {"message": "Material deleted"}

@router.post("/materials/upload-pdf")
async def upload_material_pdf(
    file: UploadFile = File(...),
    title: str = Form(...),
    subject: str = Form("General"),
    description: str = Form(""),
    admin=Depends(require_admin)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    content = await file.read()
    safe_name = f"material_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        text = extract_text_from_pdf(content)
    except Exception as e:
        text = f"Could not extract text: {e}"

    material = save_material({
        "title": title,
        "subject": subject,
        "description": description,
        "type": "pdf",
        "filename": safe_name,
        "original_filename": file.filename,
        "content": text[:5000],
        "file_size_kb": round(len(content) / 1024, 1),
    })
    return {"message": "Material PDF uploaded", "material": material}

# ── CURRENT AFFAIRS ────────────────────────────────────────
@router.get("/currentaffairs")
def list_ca(admin=Depends(require_admin)):
    return {"items": get_custom_ca()}

@router.post("/currentaffairs")
def add_ca(ca: dict = Body(...), admin=Depends(require_admin)):
    saved = save_ca(ca)
    return {"message": "Current affair saved", "item": saved}

# ── SITE SETTINGS ──────────────────────────────────────────
@router.get("/settings")
def get_site_settings(admin=Depends(require_admin)):
    return get_settings()

@router.put("/settings")
def update_settings(s: dict = Body(...), admin=Depends(require_admin)):
    saved = save_settings(s)
    return {"message": "Settings updated", "settings": saved}

# ── BULK QUESTION IMPORT (JSON) ────────────────────────────
@router.post("/import/json")
async def import_json(
    file: UploadFile = File(...),
    admin=Depends(require_admin)
):
    content = await file.read()
    try:
        questions = json.loads(content)
        if not isinstance(questions, list):
            raise ValueError("JSON must be an array of questions")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    saved = []
    for q in questions:
        required = ["question", "options", "answer", "subject"]
        if all(k in q for k in required):
            saved.append(save_question(q))

    return {"message": f"{len(saved)} questions imported", "imported": len(saved), "skipped": len(questions) - len(saved)}


# ── PUBLIC ENDPOINTS (no auth) ────────────────────────────
@router.get("/public/notifications")
def get_public_notifications():
    settings = get_settings()
    notifs = settings.get("notifications", [
        {"id":1,"text":"CDS II 2025 notification released by UPSC — Apply now!","date":"2025-01-15","type":"exam"},
        {"id":2,"text":"975+ PYQs now available across CDS, NDA, AFCAT subjects","date":"2024-07-01","type":"update"},
        {"id":3,"text":"New SSB Psychology Tests (TAT/WAT/SRT/PPDT) added","date":"2024-07-10","type":"update"},
        {"id":4,"text":"Evening Daily Tests now live — attempt every day to build streak","date":"2024-07-12","type":"feature"},
        {"id":5,"text":"Free Notes section added — Formula sheets, Grammar, GK cheatsheets","date":"2024-07-13","type":"feature"},
    ])
    return {"notifications": notifs}

@router.post("/public/notifications")
def add_notification(payload: dict = Body(...), admin=Depends(require_admin)):
    settings = get_settings()
    notifs = settings.get("notifications", [])
    new_notif = {
        "id": max([n.get("id",0) for n in notifs], default=0) + 1,
        "text": payload.get("text",""),
        "date": payload.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
        "type": payload.get("type","update"),
    }
    notifs.insert(0, new_notif)
    settings["notifications"] = notifs[:20]
    save_settings(settings)
    return {"message": "Notification added", "notification": new_notif}

@router.delete("/public/notifications/{nid}")
def delete_notification(nid: int, admin=Depends(require_admin)):
    settings = get_settings()
    notifs = [n for n in settings.get("notifications",[]) if n.get("id") != nid]
    settings["notifications"] = notifs
    save_settings(settings)
    return {"message": "Deleted"}
