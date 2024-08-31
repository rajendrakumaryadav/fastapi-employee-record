from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from ..data.employee import get_employees
from ..db.db_session import get_session

templates = Jinja2Templates(directory="templates")
frontend_routes = APIRouter(tags=["Frontend"])


@frontend_routes.get("/")
async def home(*, session: Session = Depends(get_session), request: Request):
    employees = get_employees(session)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "App", "employees": employees},
    )
