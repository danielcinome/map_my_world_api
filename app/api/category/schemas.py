from pydantic import BaseModel, UUID4

class CategoryBaseSchema(BaseModel):
    name: str

class CategoryModel(CategoryBaseSchema):
    uuid: UUID4

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(CategoryModel):
    pass

class CategoryResponseSchema(BaseModel):
    data: CategoryModel
    message: str

    class Config:
        orm_mode = True

class CategoryListResponseSchema(BaseModel):
    data: list[CategoryModel]
    message: str

    class Config:
        orm_mode = True