from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from sqlalchemy.orm import Session
from app.db.postgres.engine import PostgresqlManager
from app.models.models import User
from app.api.login import get_current_active_user
from app.api.location.schemas import LocationResponseSchema, LocationCreateSchema, LocationListResponseSchema, LocationUpdateSchema
from app.api.location.managers import location_crud
from app.api.recommendation.managers import create_location_category_reviewed


router = APIRouter()
validate_user = Annotated[User, Depends(get_current_active_user)]

@router.get("/all", response_model=LocationListResponseSchema)
async def get_locations(current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        all_locations = location_crud.get_all(db)
        return {
            "data": all_locations,
            "message": "Locations retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving locations")


@router.get("/{location_id}", response_model=LocationResponseSchema)
async def get_location(location_id: str, current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        location = location_crud.get(db, location_id)
        if location is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
        return {
            "data": location,
            "message": "Location retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving location")


@router.post("/create", response_model=LocationResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_location(location_create_schema: LocationCreateSchema, current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        location = location_crud.create(db=db, obj_in=location_create_schema)
        await create_location_category_reviewed(db, location.uuid, is_location=True)
        return {
            "data": location,
            "message": "Location created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating location")

    
