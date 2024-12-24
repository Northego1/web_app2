from typing import Annotated, Protocol, Self
from fastapi import Depends

from api.v1.main_app.schemas.schemeMap import MapRequestSchema
from api.v1.main_app.services.coord_by_address import (
    CoordsByAddressService,
    CoordsByAddressServiceProtocol
)


class RouteControllerProtocol(Protocol):
    async def get_route(self: Self):
        pass



class RouteControllerImpl:
    def __init__(
            self: Self,
            CoordsByAddressService: CoordsByAddressServiceProtocol
    ):
        self.CoordsByAddressService = CoordsByAddressService


    async def get_route(self: Self, request_schema: MapRequestSchema):
        coords = await self.CoordsByAddressService.get_coords_by_address(
            request_schema
        )
        




async def get_route_controller(
        CoordsByAddressService: CoordsByAddressService,
) -> RouteControllerImpl:
    
    return RouteControllerImpl(
        CoordsByAddressService=CoordsByAddressService,
    )



RouteController = Annotated[
    RouteControllerProtocol,
    Depends(get_route_controller),
]


