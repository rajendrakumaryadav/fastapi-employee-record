import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from ..data.designation import create_designation, delete_designation
from ..db.db_session import get_session
from ..models.designation import Designation, DesignationCreate
from ..utils.utility import MissingEmployeeRecord

designation_router = APIRouter()


@designation_router.post("/designations/", response_model=Designation)
async def create_department_route(
    *, designation: DesignationCreate, db: Session = Depends(get_session)
):
    try:
        db_designation = create_designation(db, designation)
        return db_designation
    except ValueError as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    except sqlalchemy.exc.IntegrityError as ex:
        return JSONResponse(status_code=409, content={"message": str(ex)})


@designation_router.delete(
    "/designations/{id}", description="Delete designation by id"
)
async def delete_designation_route(
    *, db: Session = Depends(get_session), id: str, response: Response
):
    try:
        deleted_status = delete_designation(db, id)
        if deleted_status is True:
            response.status_code = 204
            return None
    except MissingEmployeeRecord as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
        response.status_code = 404
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex)
        )
        response.status_code = 500
