from typing import Annotated, Protocol, Self
from fastapi import Depends

from api.v1.main_app.schemas.schemeMap import MapRequestSchema
from config import settings
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
from api.v1.main_app.services.map_render import (
    MapRenderService,
    MapRenderServiceProtocol
)




class RouteControllerProtocol(Protocol):
    async def get_route(self: Self):
        pass



class RouteControllerImpl:
    def __init__(
            self: Self,
            CoordsByAddressService: CoordsByAddressServiceProtocol,
            RoutesMakerService: RoutesMakerServiceProtocol,
            RestAdderService: RestAdderServiceProtocol,
            MapRenderService: MapRenderServiceProtocol
    ):
        self.CoordsByAddressService = CoordsByAddressService
        self.RoutesMakerService = RoutesMakerService
        self.RestAdderService = RestAdderService
        self.MapRenderService = MapRenderService
        

    async def get_route(self: Self, request_schema: MapRequestSchema):
        try:
            coords = await self.CoordsByAddressService.get_coords_by_address(
                request_schema
            )
            route = await self.RoutesMakerService.create_route(
                    coords=coords,
                    transport_type=request_schema.transport_type,
                )
            if request_schema.rests and route.summary_time >= settings.setup.non_stop_drive_limit:
                refreshed_coords = await self.RestAdderService.add_rest_place_to_coords(
                    route=route
                )
                route = await self.RoutesMakerService.create_route(
                    coords=refreshed_coords,
                    transport_type=request_schema.transport_type
                )
            map_html: str = self.MapRenderService.render_by_polyline(
                route=route
            )


            with open(file='map.html', mode='w', encoding='utf-8') as file:
                file.write(map_html)
            return map_html
        except Exception as e:
            raise e
            
            




async def get_route_controller(
        CoordsByAddressService: CoordsByAddressService,
        RoutesMakerService: RoutesMakerService,
        RestAdderService: RestAdderService,
        MapRenderService: MapRenderService
) -> RouteControllerImpl:
    
    return RouteControllerImpl(
        CoordsByAddressService=CoordsByAddressService,
        RoutesMakerService=RoutesMakerService,
        RestAdderService=RestAdderService,
        MapRenderService=MapRenderService
    )



RouteController = Annotated[
    RouteControllerProtocol,
    Depends(get_route_controller),
]


