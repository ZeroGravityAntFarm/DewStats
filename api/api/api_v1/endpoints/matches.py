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
from fastapi_pagination import paginate, Page, Params

router = APIRouter()

templates = Jinja2Templates(directory="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


#Endpoint to load single match
@router.get("/match/{match_id}")
async def get_match(request: Request, match_id: int, db: Session = Depends(get_db)):
    match_data = controller.get_match(db, id=match_id)

    if not match_data:
        return HTTPException(status_code=500, detail="Failed to find match")
    
    else:
        return templates.TemplateResponse("match/index.html", {"request": request, 
                                                               "match_data": match_data
                                                               } )

#Endpoint to load all matches
@router.get("/matches")
async def get_match(request: Request, params: Params = Depends(), db: Session = Depends(get_db)):
    match_data = controller.get_all_games(db)

    if not match_data:
        return HTTPException(status_code=400, detail="Failed to find matches")
    
    else:
        return paginate(match_data, params)