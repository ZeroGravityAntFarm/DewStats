from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from fastapi_pagination import paginate, Page, Params
from db.schemas import schemas
from db import controller
from db.session import SessionLocal
from internal.auth import get_current_user
from sqlalchemy.orm import Session
from internal.limiter import limiter 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


#Endpoint to catch game stats
@router.get("/match/{match_id}")
async def get_match(request: Request, match_id: int, db: Session = Depends(get_db)):
    match = controller.get_match(db, id=match_id)

    if not match:
        return HTTPException(status_code=500, detail="Failed to find match")
    
    else:
        return match
