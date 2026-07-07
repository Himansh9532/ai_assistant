import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.candidate import Candidate
from schemas.candidate_schema import CandidateCreate
from services.email_service import (
    generate_otp,
    send_otp_email,
    save_otp,
    verify_otp
)

router = APIRouter(prefix="/candidate", tags=["Candidate"])


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate_candidate(email: str, password: str, db: Session):
    candidate = db.query(Candidate).filter(
        Candidate.email == email
    ).first()

    if not candidate:
        return None

    if not candidate.password_hash:
        return None

    if candidate.password_hash != hash_password(password):
        return None

    return candidate


@router.post("/register")
async def register_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    try:
        existing = db.query(Candidate).filter(
            Candidate.email == candidate.email
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        candidate_data = candidate.model_dump()

        if candidate_data.get("password"):
            candidate_data["password_hash"] = hash_password(
                candidate_data.pop("password")
            )
        else:
            candidate_data["password_hash"] = None

        new_candidate = Candidate(**candidate_data)

        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

        # Generate OTP
        otp_code = generate_otp()
        save_otp(db, candidate.email, otp_code)

    except HTTPException:
        raise

    except Exception as exc:
        import traceback
        print(f"Error during registration DB step: {exc}")
        traceback.print_exc()
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {exc}"
        )

    # Send OTP Email
    try:
        email_sent = await send_otp_email(
            candidate.email,
            otp_code
        )

    except Exception as exc:
        import traceback
        print(f"Unexpected error while sending OTP email: {exc}")
        traceback.print_exc()

        email_sent = False

    if not email_sent:
        return {
            "message": (
                "Registration successful but OTP email could not be sent."
            ),
            "candidate_id": new_candidate.id,
            "email": candidate.email,
            "email_sent": False
        }

    return {
        "message": "Registration successful. OTP sent to your email.",
        "candidate_id": new_candidate.id,
        "email": candidate.email,
        "email_sent": True
    }


@router.post("/verify-otp")
def verify_otp_endpoint(
    payload: dict,
    db: Session = Depends(get_db)
):
    email = payload.get("email")
    otp = payload.get("otp")

    if not email or not otp:
        raise HTTPException(
            status_code=400,
            detail="Email and OTP are required"
        )

    try:
        is_valid = verify_otp(db, email, otp)

    except Exception as exc:
        import traceback
        print(f"Error during verify_otp: {exc}")
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Error verifying OTP"
        )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired OTP"
        )

    candidate = db.query(Candidate).filter(
        Candidate.email == email
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    candidate.is_verified = 1
    db.commit()
    db.refresh(candidate)

    return {
        "message": "OTP verified successfully",
        "candidate_id": candidate.id,
        "full_name": candidate.full_name
    }


@router.post("/resend-otp")
async def resend_otp(
    payload: dict,
    db: Session = Depends(get_db)
):
    email = payload.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required"
        )

    candidate = db.query(Candidate).filter(
        Candidate.email == email
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    otp_code = generate_otp()
    save_otp(db, email, otp_code)

    try:
        email_sent = await send_otp_email(
            email,
            otp_code
        )

    except Exception as exc:
        print(
            f"Unexpected error while resending OTP email: {exc}"
        )
        email_sent = False

    if not email_sent:
        return {
            "message": (
                "OTP generated but email delivery failed."
            ),
            "email_sent": False
        }

    return {
        "message": "OTP resent successfully",
        "email_sent": True
    }


@router.post("/login")
def login_candidate(
    payload: dict,
    db: Session = Depends(get_db)
):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    candidate = authenticate_candidate(
        email,
        password,
        db
    )

    if not candidate:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "candidate_id": candidate.id,
        "full_name": candidate.full_name,
    }

