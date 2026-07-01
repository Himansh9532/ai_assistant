# Placeholder for backend/routes/candidate_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.candidate import Candidate
from schemas.candidate_schema import CandidateCreate

router = APIRouter(prefix="/candidate", tags=["Candidate"])


@router.post("/register")
def register_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Candidate).filter(
        Candidate.email == candidate.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_candidate = Candidate(**candidate.model_dump())

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return {
        "message": "Registration successful",
        "candidate_id": new_candidate.id
    }