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


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


#Endpoint to catch game stats
@router.post("/stats")
async def post_stats(request: Request, db: Session = Depends(get_db)):
    stats = controller.create_stats(db, stats=request.json())

    if not stats:
        return HTTPException(status_code=500, detail="Failed to create stats")
    
    else:
        return HTTPException(status_code=200)