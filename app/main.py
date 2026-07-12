from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import exams, pyq, ssb, learning, cds, mentor

app = FastAPI(title="DefencePrep AI", version="1.0.0")

import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://defenceprep-api.netlify.app").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exams.router, prefix="/api/exams", tags=["Exams"])
app.include_router(pyq.router, prefix="/api/pyq", tags=["PYQ"])
app.include_router(ssb.router, prefix="/api/ssb", tags=["SSB"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(cds.router, prefix="/api/cds", tags=["CDS"])
app.include_router(mentor.router, prefix="/api/mentor", tags=["AI Mentor"])

@app.get("/")
def root():
    return {"message": "DefencePrep AI API is running"}
