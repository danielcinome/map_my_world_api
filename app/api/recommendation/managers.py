import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from greenletio import async_
from typing import List
from app.models.models import Location, Category, LocationCategoryReviewed
from app.api.crud.base import CRUDBase
from app.api.recommendation.schemas import RecommendationModel, RecommendationBaseSchema, RecommendationCreateSchema, RecommendationBaseResponseSchema
from app.api.core.utils import format_datetime

logger = logging.getLogger(__name__)

async def create_location_category_reviewed(db: Session, obj_id: int, is_location: bool):
    try:
        existing_reviews = await async_(db.query(LocationCategoryReviewed).filter(LocationCategoryReviewed.location_uuid == obj_id).all)() if is_location else await async_(db.query(LocationCategoryReviewed).filter(LocationCategoryReviewed.category_uuid == obj_id).all)()
        existing_category_ids = set(review.category_id if is_location else review.location_id for review in existing_reviews)

        if is_location:
            obj_type = "location"
            all_objs = await async_(db.query(Category).all)()
        else:
            obj_type = "category"
            all_objs = await async_(db.query(Location).all)()

        new_reviews = []
        for obj in all_objs:
            if obj.uuid not in existing_category_ids:
                new_reviews.append(
                    LocationCategoryReviewed(
                        location_uuid=obj_id,
                        category_uuid=obj.uuid,
                    ) if is_location else 
                    LocationCategoryReviewed(
                        location_uuid=obj.uuid,
                        category_uuid=obj_id,
                    )
                )

        db.add_all(new_reviews)
        db.commit()
    except Exception as e:
        logger.exception(f"Error creating location-category reviewed: {e}")
        db.rollback()
        raise e

async def update_reviewed_dates(db: Session, reviewed_combinations):
    try:
        for reviewed in reviewed_combinations:
            # update last_reviewed_date field with current date
            location_uuid = str(reviewed.LocationCategoryReviewed.location_uuid)
            category_uuid = str(reviewed.LocationCategoryReviewed.category_uuid)

            db.query(LocationCategoryReviewed)\
                .filter(LocationCategoryReviewed.location_uuid == location_uuid, LocationCategoryReviewed.category_uuid == category_uuid)\
                .update({LocationCategoryReviewed.last_reviewed_date: datetime.now()})
        
        # Confirm database changes
        db.commit()
    except Exception as e:
        logger.exception(f"Error updating reviewed dates: {e}")
        db.rollback()
        raise e

class CRUDLocationCategoryReviewed(CRUDBase[LocationCategoryReviewed, RecommendationCreateSchema, RecommendationModel]):

    async def get_recommendations(self, db: Session) -> List[RecommendationBaseSchema]:
        thirty_days_ago = datetime.now() - timedelta(days=30)

        try:
            # Get all location-category combinations that have not been reviewed in the last 30 days.
            unreviewed_combinations = db.query(LocationCategoryReviewed, Category, Location)\
                .join(Category, LocationCategoryReviewed.category_uuid == Category.uuid)\
                .join(Location, LocationCategoryReviewed.location_uuid == Location.uuid)\
                .filter((LocationCategoryReviewed.last_reviewed_date == None) | (LocationCategoryReviewed.last_reviewed_date <= thirty_days_ago) | (LocationCategoryReviewed.last_reviewed_date >= thirty_days_ago))\
                .order_by(LocationCategoryReviewed.last_reviewed_date.is_(None).desc(), LocationCategoryReviewed.last_reviewed_date.desc())\
                .limit(10).all()

            recommendations = [
                RecommendationBaseResponseSchema(
                    location=unreviewed.Location.__dict__,
                    category=unreviewed.Category.__dict__,
                    last_reviewed_date=format_datetime(unreviewed.LocationCategoryReviewed.last_reviewed_date)
                    ) for unreviewed in unreviewed_combinations
                ]
            
            await update_reviewed_dates(db, unreviewed_combinations)
        except Exception as e:
            logger.exception(f"Error get recommendations: {e}")
            raise e

        return recommendations
    

location_category_reviewed_crud = CRUDLocationCategoryReviewed(LocationCategoryReviewed)