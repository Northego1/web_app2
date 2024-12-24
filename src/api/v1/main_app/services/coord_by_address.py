from typing import Annotated, Protocol, Self
from fastapi import Depends

from api.v1.main_app.schemas.schemeMap import Coords, MapRequestSchema
from api.v1.main_app.gateway.nominatim_api import (
    NominatimApiGateway,
    NominatimApiGatewayProtocol
)
from logger import get_logger

logger = get_logger(__name__)


class CoordsByAddressServiceProtocol(Protocol):
    async def get_coords_by_address(self: Self, request_schema: MapRequestSchema) -> Coords:
        pass


class CoordsByAddressServiceImpl:
    def __init__(
            self: Self,
            NominatimApiGateway: NominatimApiGatewayProtocol
    ):
        self.NominatimApiGateway = NominatimApiGateway


    async def get_coords_by_address(self: Self, request_schema: MapRequestSchema) -> Coords:
        logger.debug('Обращаяемся к nominatim_gateway')
        nominatim_response = await self.NominatimApiGateway.nominatim_request(
            addresses=request_schema.addresses
        )
        return nominatim_response



async def get_coords_service(
        NominatimApiGateway: NominatimApiGateway
) -> CoordsByAddressServiceImpl:
    
    return CoordsByAddressServiceImpl(
        NominatimApiGateway=NominatimApiGateway
    )


CoordsByAddressService =  Annotated[
    CoordsByAddressServiceProtocol,
    Depends(get_coords_service)
]