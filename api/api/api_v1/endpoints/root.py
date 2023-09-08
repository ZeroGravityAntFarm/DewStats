from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.schemas import schemas
from db import controller

router = APIRouter()

templates = Jinja2Templates(directory="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def root(request: Request, db: Session = Depends(get_db)):

    return templates.TemplateResponse("frontpage/index.html", {"request": request})