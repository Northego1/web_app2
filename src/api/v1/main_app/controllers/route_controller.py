from typing import Annotated, Protocol, Self
from fastapi import Depends

from api.v1.main_app.schemas.schemeMap import MapRequestSchema
from api.v1.main_app.services.coord_by_address import (
    CoordsByAddressService,
    CoordsByAddressServiceProtocol
)
from api.v1.main_app.services.routes_maker import (
    RoutesMakerService,
    RoutesMakerServiceProtocol
)
from api.v1.main_app.services.rest_adder import (
    RestAdderService,
    RestAdderServiceProtocol
)


class RouteControllerProtocol(Protocol):
    async def get_route(self: Self):
        pass



class RouteControllerImpl:
    def __init__(
            self: Self,
            CoordsByAddressService: CoordsByAddressServiceProtocol,
            RoutesMakerService: RoutesMakerServiceProtocol,
            RestAdderService: RestAdderServiceProtocol
    ):
        self.CoordsByAddressService = CoordsByAddressService
        self.RoutesMakerService = RoutesMakerService
        self.RestAdderService = RestAdderService

    async def get_route(self: Self, request_schema: MapRequestSchema):
        try:
            coords = await self.CoordsByAddressService.get_coords_by_address(
                request_schema
            )
            route = await self.RoutesMakerService.create_route(
                    coords=coords,
                    transport_type=request_schema.transport_type,
                )
            if request_schema.rests:
                pass
        except Exception as e:
            raise e
            
            




async def get_route_controller(
        CoordsByAddressService: CoordsByAddressService,
        RoutesMakerService: RoutesMakerService,
        RestAdderService: RestAdderService
) -> RouteControllerImpl:
    
    return RouteControllerImpl(
        CoordsByAddressService=CoordsByAddressService,
        RoutesMakerService=RoutesMakerService,
        RestAdderService=RestAdderService
    )



RouteController = Annotated[
    RouteControllerProtocol,
    Depends(get_route_controller),
]


