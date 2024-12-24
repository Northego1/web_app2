from typing import Annotated, Protocol, Self

from fastapi import Depends

from api.v1.main_app.schemas.schemeMap import Transport_type


class ValhallaApiGatewayProtocol(Protocol):
    pass


class ValhallaApiGatewayImpl:
    async def valhalla_request(
            self: Self,
            coords,
            transport_type: Transport_type = Transport_type.auto
    ):
        pass


async def get_valhalla_gateway() -> ValhallaApiGatewayImpl:
    return ValhallaApiGatewayImpl()


ValhallaGateway = Annotated[
    ValhallaApiGatewayProtocol,
    Depends(get_valhalla_gateway)
]