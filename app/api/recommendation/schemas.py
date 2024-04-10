from pydantic import BaseModel, UUID4
from typing import List
from typing import Optional
from app.api.location.schemas import LocationBaseSchema
from app.api.category.schemas import CategoryBaseSchema

class RecommendationBaseSchema(BaseModel):
    location_uuid: str
    category_uuid: str
    last_reviewed_date: Optional[str] = None

class RecommendationModel(RecommendationBaseSchema):
    uuid: UUID4

class RecommendationCreateSchema(RecommendationBaseSchema):
    pass

class RecommendationUpdateSchema(BaseModel):
    uuid: UUID4
    location_uuid: str
    category_uuid: str
    last_reviewed_date: Optional[str] = None

class RecommendationResponseSchema(BaseModel):
    data: RecommendationModel
    message: str

    class Config:
        orm_mode = True

class RecommendationBaseResponseSchema(BaseModel):
    location: LocationBaseSchema
    category: CategoryBaseSchema
    last_reviewed_date: Optional[str] = None

class RecommendationListResponseSchema(BaseModel):
    data: List[RecommendationBaseResponseSchema]
    message: str

    class Config:
        orm_mode = True