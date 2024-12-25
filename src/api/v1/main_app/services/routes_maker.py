from typing import Annotated, Protocol, Self, Union

from fastapi import Depends
from openrouteservice import convert
from api.v1.main_app.gateway.valhalla_api import (
    ValhallaGateway,
    ValhallaApiGatewayProtocol
)
from api.v1.main_app.schemas.schemeMap import Coords, Route, Transport_type
from logger import get_logger




logger = get_logger(__name__)


class RoutesMakerServiceProtocol(Protocol):
    async def create_route(
            self: Self,
            coords: Coords,
            transport_type: Transport_type,

    ) -> Route:
        pass


class RoutesMakerServiceImpl:
    def __init__(
            self: Self,
            ValhallaGateway: ValhallaApiGatewayProtocol
    ):
        self.ValhallaGateway = ValhallaGateway


    async def create_route(
            self: Self,
            coords: Coords,
            transport_type: Transport_type,
    ) -> Route:
        valhalla_response = await self.ValhallaGateway.valhalla_request(
            coords=coords,
            transport_type=transport_type
        )
        polylines = []
        for leg in valhalla_response['trip']['legs']:
            geometry = leg["shape"]
            decoded_geometry = convert.decode_polyline(geometry)
            self.route_locations=[
                (coord[1]/10, coord[0]/10) for coord in decoded_geometry['coordinates']
            ]
            polylines.append(self.route_locations)
        
        route = Route(
            coords=coords,
            transport_type=transport_type,
            polylines=polylines,
            legs=valhalla_response['trip']['legs'],
            summary_time=valhalla_response['trip']['summary']['time'],
            distance=valhalla_response['trip']['summary']['length']
        )
        return route
    



async def get_routes_maker(
        ValhallaGateway: ValhallaGateway
):
    return RoutesMakerServiceImpl(
        ValhallaGateway=ValhallaGateway
    )


RoutesMakerService = Annotated[
    RoutesMakerServiceProtocol,
    Depends(get_routes_maker)
]