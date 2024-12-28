import asyncio
from typing import Annotated, Protocol, Self
import aiohttp
from fastapi import Depends
from api.v1.main_app.schemas.schemeMap import Points, Point, PointType
from config import settings

from exception import AddressError
from logger import get_logger


logger = get_logger(__name__)



class NominatimApiGatewayProtocol(Protocol):
    async def nominatim_request(self: Self, **addresses: str) -> Points:
        pass


class NominatimApiGatewayImpl:
    def __init__(self: Self):
        self.return_coords = Points()


    async def _request(self: Self, address: str, index: int):
        url = settings.gateway.nominatim_request_url(address)
        async with self.session.get(url=url) as response:
            if response.status == 200:
                data = await response.json()    
                if data:
                    lat = data[0]['lat']
                    lon = data[0]['lon']
                    point = Point(
                        coord=(float(lat), float(lon)),
                        index=index,
                        type=PointType.INITIAL,
                    )
                    self.return_coords.points.append(point)
                else:
                    logger.error(f'API nominatim - нет данных по {address!r}')
                    raise AddressError(detail=f'Address {address!r} not found')
            else:
                error_text = await response.text()
                logger.error(f'Ошибка ответа от API nominatim: {error_text!r}')
                raise AddressError(
                    status_code=response.status,
                    detail=f"{error_text}"
                )

    
    async def nominatim_request(self: Self, addresses: list[str]) -> Points:
        async with aiohttp.ClientSession() as self.session:
            logger.debug('Формируем "task_list" для отправки сообщений в "nominatim_api"')
            tasks = [
                asyncio.create_task(self._request(index=index, address=address))
                for index, address in enumerate(addresses)
            ]
            await asyncio.gather(*tasks)
            logger.debug('Получены координаты от nominatim_api')
            return self.return_coords
        


async def get_nominatim_gateway() -> NominatimApiGatewayImpl:
    return NominatimApiGatewayImpl()



NominatimApiGateway = Annotated[
    NominatimApiGatewayProtocol,
    Depends(get_nominatim_gateway)
]