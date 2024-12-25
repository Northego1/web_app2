from typing import Annotated, Protocol, Self

from fastapi import Depends
from api.v1.main_app.schemas.schemeMap import Route
from logger import get_logger
import numpy as np


logger = get_logger(__name__)


class RestAdderServiceProtocol(Protocol):
    async def add_rest_place_to_coords(self: Self):
        pass


class RestAdderServiceImpl:
    def __init__(self: Self):
        pass


    def _search_rest_coords(
            self: Self,
            route: Route,
            non_stop_drive_limit: int,
            summary_travel_time: float
    ):
        rest_times = summary_travel_time // non_stop_drive_limit 
        nonstop_driving = route.summary_time / (rest_times + 1) 
        time_to_next_stop = stops_found = 0  
        logger.debug(f'Количество заданых остановок: {rest_times}')
        rest_coords = []
        for index, leg in enumerate(route.legs):
            for maneuver in leg["maneuvers"]:
                if time_to_next_stop + maneuver['time'] > non_stop_drive_limit:
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
                    rest_coords.append([index, interpolated_coords.tolist()])
                    stops_found += 1
                    # Пересчёт оставшегося времени после остановки
                    time_to_next_stop = maneuver['time'] * (1 - time_by_order_percents)
                else:
                    continue
        return rest_coords

    async def add_rest_place_to_coords(
            self: Self,
            *,
            radius_incremet: int = 2000,
            non_stop_drive_limit: int = 7
    ):
        rest_coords = self._search_rest_coords()



async def get_rest_adder_service() -> RestAdderServiceImpl:
    return RestAdderServiceImpl()


RestAdderService = Annotated[
    RestAdderServiceProtocol,
    Depends(get_rest_adder_service)
]