from typing import Annotated, Protocol, Self, Union

from fastapi import Depends
from openrouteservice import convert
from api.v1.main_app.schemas.schemeMap import Transport_type
from logger import get_logger

logger = get_logger(__name__)


class RoutesMakerServiceProtocol(Protocol):
    async def create_route(self: Self):
        pass


class RoutesMakerServiceImpl:
    def __init__(
            self: Self,
            ValhallaApi
        ):
        self.valhalla_api = ValhallaApi




    async def create_route(
            self: Self,
            coords: Union[tuple, list],
            transport_type: Transport_type
    ):
        route_data = await self.valhalla_api()
        routes = []
        logger.debug('Формирование полилинии для всех точек маршрута')
        for leg in route_data['trip']['legs']:
            geometry = leg["shape"]
            
            decoded_geometry = convert.decode_polyline(geometry)

            self.route_locations=[
                (coord[1]/10, coord[0]/10) for coord in decoded_geometry['coordinates']
            ]
            routes.append(self.route_locations)
        logger.debug('Возварт информации о маршруте и полилинии')
        return {
            'route': routes,
            'route_data': route_data,
            'coords': self.coords,
            'transport_type': self.transport_type
            }
    



async def get_routes_maker():
    return RoutesMakerServiceImpl()


RoutesMakerService = Annotated[
    RoutesMakerServiceProtocol,
    Depends(get_routes_maker)
]