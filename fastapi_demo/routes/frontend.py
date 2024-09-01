from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from fastapi_demo.data.designation import get_designation

from ..data.employee import get_employees
from ..db.db_session import get_session

templates = Jinja2Templates(directory="templates")
frontend_routes = APIRouter(tags=["Frontend"])


@frontend_routes.get("/")
async def home(*, session: Session = Depends(get_session), request: Request):
    employees = get_employees(session)
    designation = get_designation(session)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "App",
            "employees": employees,
            "designations": designation,
        },
    )


@frontend_routes.get("/designation")
async def index_designation(
    *, session: Session = Depends(get_session), request: Request
):
    designation = get_designation(session)

    return templates.TemplateResponse(
        "designation.html",
        {
            "request": request,
            "title": "App",
            "designations": designation,
        },
    )


@frontend_routes.get("/privacy_policy")
async def privacy_policy(request: Request):
    """Render the privacy policy page."""
    return templates.TemplateResponse(
        "privacy_policy.html", {"request": request, "title": "Privacy Policy"}
    )


@frontend_routes.get("/contact")
async def contact(request: Request):
    """Render the contact page."""
    return templates.TemplateResponse(
        "contact.html", {"request": request, "title": "Contact Us"}
    )


@frontend_routes.get("/about")
async def about(request: Request):
    """Render the about page."""
    return templates.TemplateResponse(
        "about.html", {"request": request, "title": "About Us"}
    )
