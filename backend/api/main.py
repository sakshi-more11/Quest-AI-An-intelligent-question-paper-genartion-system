"""
main.py

QuestAI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import upload_management
from backend.api.routes import upload_center
from backend.api.routes import question_generation
from backend.api.routes import templates
# -----------------------------
# Database
# -----------------------------

from backend.database.database import engine
from backend.database.base import Base
from backend.api.routes.template_routes import router as template_router
# -----------------------------
# Import Models
# -----------------------------
from backend.api.routes import question_bank
import backend.models.user
import backend.models.subject
import backend.models.uploaded_file
import backend.models.knowledge
import backend.models.question
import backend.models.paper
import backend.models.history
import backend.models.material
# Create all database tables

Base.metadata.create_all(bind=engine)

# -----------------------------
# Configuration
# -----------------------------
from backend.api.routes import question_bank
from backend.api.core.config import settings
from backend.api.template_generation import router as template_router
# -----------------------------
# Middleware
# -----------------------------
from backend.api.routes.subject import router as subject_router
from backend.api.middleware.request_logger import (
    RequestLoggerMiddleware
)
from backend.api.routes import search
# -----------------------------
# Exception Handler
# -----------------------------

from backend.api.core.exception_handler import (
    global_exception_handler
)

# -----------------------------
# Routes
# -----------------------------

from backend.api.routes import (
    upload,
    knowledge,
    generate,
    paper,
    export,
    auth,
    admin,
    teachers        
)

# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="QuestAI Intelligent Question Paper Generation System"
)

# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------
# Middleware
# -----------------------------

app.add_middleware(
    RequestLoggerMiddleware
)

# -----------------------------
# Exception Handler
# -----------------------------

app.add_exception_handler(
    Exception,
    global_exception_handler
)

# -----------------------------
# Register Routes
# -----------------------------

app.include_router(upload.router)

app.include_router(knowledge.router)

app.include_router(generate.router)

app.include_router(paper.router)

app.include_router(export.router)

app.include_router(auth.router)
app.include_router(question_bank.router)
app.include_router(admin.router)
app.include_router(upload_management.router)
app.include_router(upload_center.router)
app.include_router(question_generation.router)
app.include_router(templates.router)
app.include_router(subject_router)
# ✅ Teacher Management
app.include_router(teachers.router)
app.include_router(search.router)
# -----------------------------
# Home Endpoint
# -----------------------------

@app.get("/")
def home():

    return {
        "application": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "Running"
    }

# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():

    return {
        "status": "Healthy",
        "database": "Connected",
        "version": settings.VERSION
    }