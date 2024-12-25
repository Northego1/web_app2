from typing import Annotated, Protocol, Self

import aiohttp
from fastapi import Depends
from openrouteservice import convert
from api.v1.main_app.schemas.schemeMap import Coords, Route, Transport_type
from exception import ValhallaError
from logger import get_logger
from config import settings


logger = get_logger(__name__)


class ValhallaApiGatewayProtocol(Protocol):
    async def valhalla_request(
            self: Self,
            coords: Coords,
            transport_type: Transport_type = Transport_type.auto,
            *,
            units: str = "kilometres",
            language: str = "ru",
            directions_type: str = "maneuvers"
    ):
        pass


class ValhallaApiGatewayImpl:
    async def _request(self: Self, json_request: dict):
        logger.debug('Обращение к API valhalla')
        async with aiohttp.request(
            'post',
            url=settings.gateway.valhalla_request_url,
            json=json_request
        ) as response:
            if response.status == 200:
                logger.debug('Успешный ответ API valhalla')
                return await response.json()     
            else:
                logger.error('Ошибка ответа API valhalla')
                raise ValhallaError(
                    status_code=response.status,
                    detail="Маршрут не найден"
                )
            

    async def valhalla_request(
            self: Self,
            coords: Coords,
            transport_type: Transport_type = Transport_type.auto,
            *,
            units: str = "kilometres",
            language: str = "ru",
            directions_type: str = "maneuvers"
    ):
        json_request = {
            "locations": [0] * len(coords.coords),
            "costing": transport_type,
            "directions_options": {
                "units": units,
                "language": language,
                "directions_type": directions_type
            }
        }
        for point in coords.coords:
            json_request["locations"][point.index] = {
                "lat": point.coord[0],
                "lon": point.coord[1],
                "type": "break"
            }
        valhalla_response = await self._request(json_request=json_request)
        return valhalla_response




async def get_valhalla_gateway() -> ValhallaApiGatewayImpl:
    return ValhallaApiGatewayImpl()


ValhallaGateway = Annotated[
    ValhallaApiGatewayProtocol,
    Depends(get_valhalla_gateway)
]