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

    global_stats = controller.get_global_stats(db)
    players = controller.get_players(db)
    games = controller.get_games(db)

    return templates.TemplateResponse("frontpage/index.html", {"request": request, 
                                                               "global_stats_games": global_stats["games"], 
                                                               "global_stats_kills": global_stats["kill_count"],
                                                               "global_stats_medals": global_stats["medal_count"],
                                                               "global_stats_zombies": global_stats["zombies_killed"],
                                                               "player_list": players,
                                                               "games": games} )  