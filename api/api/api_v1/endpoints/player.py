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


#Endpoint to load single player
@router.get("/player/{player_id}")
async def get_player(request: Request, player_id: str, db: Session = Depends(get_db)):
    player_data = controller.get_player(db, id=player_id)

    if not player_data:
        return HTTPException(status_code=500, detail="Failed to find player")
    
    else:
        return templates.TemplateResponse("player/index.html", {"request": request, 
                                                               "player_data": player_data
                                                               } )