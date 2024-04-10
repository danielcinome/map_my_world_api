from greenletio import async_
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.crud.base import CRUDBase
from app.models.models import Location
from app.api.location.schemas import LocationCreateSchema, LocationModel


class CRUDLocation(CRUDBase[Location, LocationCreateSchema, LocationModel]):

    pass

location_crud = CRUDLocation(Location)