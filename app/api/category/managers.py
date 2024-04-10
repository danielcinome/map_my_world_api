from greenletio import async_

from app.api.crud.base import CRUDBase
from app.models.models import Category
from app.api.category.schemas import CategoryCreateSchema, CategoryModel


class CRUDCategory(CRUDBase[Category, CategoryCreateSchema, CategoryModel]):

    pass

category_crud = CRUDCategory(Category)