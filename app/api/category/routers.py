from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from sqlalchemy.orm import Session
from app.db.postgres.engine import PostgresqlManager
from app.models.models import User
from app.api.login import get_current_active_user
from app.api.category.schemas import CategoryCreateSchema, CategoryResponseSchema, CategoryListResponseSchema
from app.api.category.managers import  category_crud
from app.api.recommendation.managers import create_location_category_reviewed
from app.api.core.exceptions import ExistingValueError

router = APIRouter()
validate_user = Annotated[User, Depends(get_current_active_user)]

@router.get("/all", response_model=CategoryListResponseSchema)
async def get_categories(current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        all_categories = category_crud.get_all(db)
        return {
            "data": all_categories,
            "message": "Categories retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving categories")

@router.post("/create", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreateSchema, current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        category = category_crud.create(db, obj_in=category)
        await create_location_category_reviewed(db, category.uuid, is_location=False)
        return {"data": category, "message": "Category created successfully"}
    except ExistingValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exists')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating category")
    
@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(category_id: str, current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        category = category_crud.get(db, category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return {
            "data": category,
            "message": "Category retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving category")