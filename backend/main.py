from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database
from database.database import Base, engine

# Models import karna zaruri hai warna tables create nahi hongi
from models.candidate import Candidate
from models.question import Question
from models.answer import Answer
from models.result import Result
from models.admin import Admin

# Routes
from routes.candidate_routes import router as candidate_router
from routes.exam_routes import router as exam_router
from routes.result_routes import router as result_router

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

app = FastAPI(
    title="AI Data Analyst Assessment API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Database tables create karo
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(candidate_router)
app.include_router(exam_router)
app.include_router(result_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )


@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"request": request}
    )


@app.get("/exam", response_class=HTMLResponse)
def exam(request: Request):
    return templates.TemplateResponse(
        request,
        "exam.html",
        {"request": request}
    )


@app.get("/result", response_class=HTMLResponse)
def result(request: Request):
    return templates.TemplateResponse(
        request,
        "result.html",
        {"request": request}
    )


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }