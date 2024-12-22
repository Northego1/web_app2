from typing import Optional
from pydantic import BaseModel
from enum import Enum


class Transport_type(str, Enum):
    auto = 'auto'
    bicycle = 'bicycle'
    pedestrian = 'pedestrian'


class SchemeMap(BaseModel):
    addresses: list

    rests: bool
    transport_type: Transport_type

    class Config:
        anystr_strip_whitespace = True
