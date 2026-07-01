# Placeholder for backend/routes/result_routes.py
from fastapi import APIRouter
from services.evaluation_service import evaluate_exam

router = APIRouter(
    prefix="/result",
    tags=["Results"]
)


@router.post("/submit")
def submit_exam(payload: dict):

    result = evaluate_exam(
        payload["questions"],
        payload["answers"]
    )

    return result