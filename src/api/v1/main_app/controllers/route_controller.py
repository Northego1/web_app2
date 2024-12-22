from typing import Annotated, Protocol, Self
from fastapi import Depends


class RouteControllerProtocol(Protocol):
    async def get_route(self: Self):
        pass



class RouteControllerImpl:
    def __init__(self: Self):
        pass



    async def get_route(self: Self):
        pass



async def get_route_controller():
    return RouteControllerImpl()



RouteController = Annotated[
    RouteControllerProtocol,
    Depends(get_route_controller),
]