from decimal import Decimal
from typing import Literal, Optional, Self
from fastapi import Query
from pydantic import BaseModel, field_validator, validator
from enum import Enum

class PointType(str, Enum):
    REST = 'rest'
    INITIAL = 'initial'


class Transport_type(str, Enum):
    auto = 'auto'
    bicycle = 'bicycle'
    pedestrian = 'pedestrian'




class Point(BaseModel):
    coord: tuple[float, float]
    index: int
    type: PointType


class Points(BaseModel):
    points: Optional[list[Point]] = []


class Route(BaseModel):
    points: Points
    transport_type: Transport_type
    polylines: list[list[tuple[float, float]]]
    legs: list[dict]
    summary_time: float   # seconds
    distance: float     # metres


class PlaceAddress(BaseModel):
    city: str | None
    street: str | None
    house_num: str | None


class RestPlaceInfo(BaseModel):
    type: str | None
    name: str
    address: PlaceAddress
    phone: str | None
    reservation: str | None


class RestPlace(BaseModel):
    point: Point
    place: RestPlaceInfo



class MapRequestSchema(BaseModel):
    addresses: Optional[list[str]]
    rests: bool
    transport_type: Transport_type


    @classmethod
    def as_query(
        cls,
        addresses: list[str] = Query(default=[]),
        rests: Optional[bool] = Query(default=False),
        transport_type: Transport_type = Query(default=Transport_type.auto)
    ) -> Self:
        return cls(
            addresses=addresses,
            rests=rests,
            transport_type=transport_type
        )


