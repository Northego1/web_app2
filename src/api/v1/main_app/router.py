from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse

from logger import get_logger
from api.v1.main_app import controllers
from api.v1.main_app.schemas.schemeMap import MapRequestSchema


logger = get_logger(__name__)

router = APIRouter(
    prefix='/routes',
    tags=['get_map']
)


@router.get('/get_map/')
async def get_route_by_coords(
    RouteController: controllers.RouteController,
    request_schema: MapRequestSchema = Depends(MapRequestSchema.as_query)
):
    response_schema = await RouteController.get_route(request_schema=request_schema)
    return HTMLResponse()