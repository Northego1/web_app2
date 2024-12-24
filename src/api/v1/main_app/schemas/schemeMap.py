from decimal import Decimal
from typing import Literal, Optional, Self
from fastapi import Query
from pydantic import BaseModel, field_validator, validator
from enum import Enum

class PointType(str, Enum):
    REST = 'rest'
    INITIAL = 'initial'


class Point(BaseModel):
    coord: tuple[float, float]
    index: int
    type: PointType


    

class Coords(BaseModel):
    coords: Optional[list[Point]] = []



class Transport_type(str, Enum):
    auto = 'auto'
    bicycle = 'bicycle'
    pedestrian = 'pedestrian'


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


