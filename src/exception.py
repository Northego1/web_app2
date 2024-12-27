from typing import Self
from fastapi import HTTPException

class ServerError(HTTPException):
    def __init__(
            self: Self,
            status_code:int = 500,
            detail = "unknown error",
            headers = None
    ):
        super().__init__(status_code, detail, headers)


class MapError(HTTPException):
    def __init__(self, status_code, detail = None):
        super().__init__(status_code, detail)


class AddressError(MapError):
    def __init__(self,
            status_code: int = 400,
            detail: str = "Address Error"):
        super().__init__(status_code=status_code, detail=detail)


class ValhallaError(MapError):
    def __init__(self,
            status_code: int = 500,
            detail: str = "Valhalla Error"):
        super().__init__(status_code=status_code, detail=detail)

    

