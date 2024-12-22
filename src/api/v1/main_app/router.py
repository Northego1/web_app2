from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from logger import get_logger
from v1.main_app.schemas.schemeMap import SchemeMap
from api.v1.main_app import controllers
# from Exceptions.ExcMap import MapError
# from auth.user_model import User


# from main_logics.schemas.schemeMap import SchemeMap
# from main_logics.services.map_services import (
#     AddressCoords, Hotelsadder, MapRender, RoutesMaker, AddRouteToDb)
# from main_logics.dependencies import current_user, optional_current_user, get_session

# from logger import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix='/routes',
    tags=['get_map']
)


@router.post('/get_map')
async def get_route_by_coords(
    request_data: SchemeMap,
    RouteController: controllers.RouteController
):
    response_schema = await RouteController.get_route()