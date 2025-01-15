from typing import cast
from api.v1.main_app.controllers.route_controller import RouteControllerProtocol
from unittest.mock import AsyncMock, Mock



RouteController = cast(
    RouteControllerProtocol,
    Mock()
)

RouteController.get_route = AsyncMock(
    return_value='Map'
)
