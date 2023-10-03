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


#Endpoint to load single server
@router.get("/server/{server_name}")
async def get_server(request: Request, server_name: str, db: Session = Depends(get_db)):
    server_data = controller.get_server(db, sName=server_name)

    if not server_data:
        return HTTPException(status_code=500, detail="Failed to find server")
    
    else:
        return templates.TemplateResponse("server/index.html", {"request": request, 
                                                               "server_data": server_data
                                                               } )