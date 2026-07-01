# Placeholder for backend/routes/exam_routes.py
from fastapi import APIRouter
from services.ai_service import generate_questions

router = APIRouter(
    prefix="/exam",
    tags=["Exam"]
)


@router.get("/generate/{stream}")
def generate_exam(stream: str):
    questions = generate_questions(stream)

    return {
        "total_questions": len(questions),
        "questions": questions
    }