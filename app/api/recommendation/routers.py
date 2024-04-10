from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from sqlalchemy.orm import Session
from app.db.postgres.engine import PostgresqlManager
from app.models.models import User
from app.api.login import get_current_active_user
from app.api.recommendation.schemas import RecommendationListResponseSchema
from app.api.recommendation.managers import location_category_reviewed_crud


router = APIRouter()
validate_user = Annotated[User, Depends(get_current_active_user)]

@router.get("", response_model=RecommendationListResponseSchema)
async def get_recommendations(current_user: validate_user, db: Session = Depends(PostgresqlManager.get_db)):
    try:
        recommendations = await location_category_reviewed_crud.get_recommendations(db)
        return {
            "data": recommendations,
            "message": "Recommendations retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving recommendations")
