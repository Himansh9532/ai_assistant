import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# FastAPI app create
app = FastAPI()

# Static files
app.mount(
    "/static",
    StaticFiles(directory="../frontend/static"),
    name="static"
)

# Templates
templates = Jinja2Templates(
    directory="../frontend/templates"
)
# ----------------------------
# Logging
# ----------------------------

logging.basicConfig(level=logging.INFO)

# ----------------------------
# Environment Variables
# ----------------------------

load_dotenv()

print("MAIL USER:", os.getenv("MAIL_USERNAME"))
print("MAIL PASS OK:", bool(os.getenv("MAIL_PASSWORD")))

            # ----------------------------
# Database
# ----------------------------

from database.database import Base, engine

# Import models so tables get created
from models.candidate import Candidate
from models.question import Question
from models.answer import Answer
from models.result import Result
from models.admin import Admin
from models.otp import OTP

# Create tables
Base.metadata.create_all(bind=engine)

# ----------------------------
# Routers
# ----------------------------

from routes.candidate_routes import router as candidate_router
from routes.exam_routes import router as exam_router
from routes.result_routes import router as result_router

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

print("Template Directory:", TEMPLATE_DIR)
print("Static Directory:", STATIC_DIR)

print("home exists:", (TEMPLATE_DIR / "home.html").exists())
print("assessment exists:", (TEMPLATE_DIR / "assessment_form.html").exists())
print("exam exists:", (TEMPLATE_DIR / "exam.html").exists())
print("result exists:", (TEMPLATE_DIR / "result.html").exists())

# ----------------------------
# FastAPI App
# ----------------------------

app = FastAPI(
    title="AI Data Analyst Assessment API",
    version="1.0.0"
)

# ----------------------------
# CORS
# ----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Static Files
# ----------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

# ----------------------------
# Templates
# ----------------------------

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)

# ----------------------------
# Include Routers
# ----------------------------

app.include_router(candidate_router)
app.include_router(exam_router)
app.include_router(result_router)

# ----------------------------
# Pages
# ----------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register_new.html"
    )


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


@app.get("/assessment", response_class=HTMLResponse)
async def assessment(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="assessment_form.html"
    )


@app.get("/exam", response_class=HTMLResponse)
async def exam(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="exam.html"
    )


@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="result.html"
    )



# ----------------------------
# Health Check
# ----------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }