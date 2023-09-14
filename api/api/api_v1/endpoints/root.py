from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi_pagination import paginate, Page, Params
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
    players = controller.get_leaderboard(db)
    games = controller.get_games(db)

    return templates.TemplateResponse("frontpage/index.html", {"request": request, 
                                                               "global_stats_games": global_stats["games"], 
                                                               "global_stats_kills": global_stats["kill_count"],
                                                               "global_stats_medals": global_stats["medal_count"],
                                                               "global_stats_zombies": global_stats["zombies_killed"],
                                                               "global_stats_humans_infected":global_stats["humans_infected"],
                                                               "global_stats_friendly_fire":global_stats["friendly_fire"],
                                                               "player_list": players,
                                                               "games": games} )  


@router.get("/leaderboard")
def leaderboard(request: Request, params: Params = Depends(), db: Session = Depends(get_db)):

    leaderboard = controller.get_leaderboard(db)

    return paginate(leaderboard, params)