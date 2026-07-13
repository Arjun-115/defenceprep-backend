from fastapi import APIRouter, HTTPException
from app.admin.database import get_materials

router = APIRouter()

@router.get("/")
def get_all_materials():
    materials = get_materials()
    return {"materials": materials}

@router.get("/{mid}")
def get_material(mid: int):
    materials = get_materials()
    m = next((x for x in materials if x["id"] == mid), None)
    if not m:
        raise HTTPException(404, "Not found")
    return m
