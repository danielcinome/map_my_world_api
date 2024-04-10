from pydantic import BaseModel, UUID4
from typing import Optional

class LocationBaseSchema(BaseModel):
    latitude: float
    longitude: float

class LocationModel(LocationBaseSchema):
    uuid: UUID4

class LocationCreateSchema(LocationBaseSchema):
    pass

class LocationUpdateSchema(BaseModel):
    uuid: UUID4
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0

class LocationResponseSchema(BaseModel):
    data: LocationModel
    message: str

    class Config:
        orm_mode = True

class LocationListResponseSchema(BaseModel):
    data: list[LocationModel]
    message: str

    class Config:
        orm_mode = True