import asyncio
from collections import deque
from typing import Annotated, Protocol, Self

import aiohttp
from fastapi import Depends, HTTPException
from api.v1.main_app.schemas.schemeMap import Points, PlaceAddress, Point, PointType, RestPlace, RestPlaceInfo, Route
from exception import ServerError
from logger import get_logger
import numpy as np
from api.v1.main_app.gateway.overpass_api import (
    OverpassApiGateway,
    OverpassApiGatewayProtocol
)
from config import settings


logger = get_logger(__name__)


class RestAdderServiceProtocol(Protocol):
    async def add_rest_place_to_coords(
            self: Self,
            route: Route,
    ) -> Points:
        pass


class RestAdderServiceImpl:
    def __init__(
            self: Self,
            OverpassApiGateway: OverpassApiGatewayProtocol,
    ):
        self.OverpassApiGateway = OverpassApiGateway

        self.rest_places: list[RestPlace] = []
        self.rest_times: int = 0


    def _search_rest_coords(
            self: Self,
            route: Route,
            summary_travel_time: float
    ) -> dict[int, list[list]]:
        if summary_travel_time < settings.setup.non_stop_drive_limit:
            raise ServerError()
        self.rest_times = int(summary_travel_time // settings.setup.non_stop_drive_limit)
        nonstop_driving = route.summary_time / (self.rest_times) 
        time_to_next_stop = stops_found = 0  
        logger.debug(f'Количество заданых остановок: {self.rest_times}')

        indexed_rest_coords = {key: list() for key, _ in enumerate(route.legs)}
        for index, leg in enumerate(route.legs):
            for maneuver in leg["maneuvers"]:
                time_to_next_stop += maneuver["time"]
                if time_to_next_stop > settings.setup.non_stop_drive_limit:
                    time_to_next_stop += maneuver["time"]
                    time_by_order_percents = (
                        (nonstop_driving - time_to_next_stop) / maneuver['time']
                    )
                    begin_shape_index = maneuver['begin_shape_index']
                    end_shape_index = maneuver['end_shape_index']

                    begin_coords  = np.array(route.polylines[index][begin_shape_index])
                    end_coords = np.array(route.polylines[index][end_shape_index])

                    interpolated_coords: np.ndarray = (
                        begin_coords + time_by_order_percents * (end_coords - begin_coords)
                    )
                    indexed_rest_coords[index].append(interpolated_coords.tolist())
                    stops_found += 1
                    if stops_found == self.rest_times:
                        return indexed_rest_coords
                    time_to_next_stop = maneuver['time'] * (1 - time_by_order_percents)



    async def add_rest_place_to_coords(
            self: Self,
            route: Route,
    ) -> Points:
        rest_coords = self._search_rest_coords(
            route=route,
            summary_travel_time=route.summary_time
        )
        places = await self.OverpassApiGateway.overpass_request(
            rest_coords=rest_coords,
            rest_times=self.rest_times,
        )
        new_coords = []
        seq = 0
        for point in sorted(route.points.points, key=lambda x: x.index):
            index = point.index
            point.index = seq
            new_coords.append(point)
            seq += 1
            for place in places:
                if place.point.index == index:
                    place.point.index = seq
                    new_coords.append(place.point)
                    places.remove(place)
                    seq += 1
        return Points(points=new_coords)



async def get_rest_adder_service(
        OverpassApiGateway: OverpassApiGateway
) -> RestAdderServiceImpl:
    return RestAdderServiceImpl(
        OverpassApiGateway=OverpassApiGateway
    )


RestAdderService = Annotated[
    RestAdderServiceProtocol,
    Depends(get_rest_adder_service)
]