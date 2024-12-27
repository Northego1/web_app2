from typing import Annotated, Protocol, Self, Union

from fastapi import Depends
import folium

from api.v1.main_app.schemas.schemeMap import PointType, Route


class MapRenderServiceProtocol(Protocol):
    def render_by_polyline(
            self: Self,
            route: Route,
            *,
            zoom_start: int = 7,
            min_zoom: int = 5
        ) -> str:
        pass


    def render_empty_map(self: Self):
        pass


class MapRenderServiceImpl:
    def __init__(self: Self):
        self.transport_settings = {
            'auto': {'color': 'green', 'dash_array': None, 'weight': 5},
            'pedestrian': {'color': 'blue', 'dash_array': '4, 4', 'weight': 2},
            'bicycle': {'color': 'blue', 'dash_array': '6, 5', 'weight': 4}
        }
        self.colors = (
            'blue', 'green', 'purple', 'darkred', 'darkgreen', 'darkblue', 'pink', 'cadetblue')
        


    def render_by_polyline(
            self: Self,
            route: Route,
            *,
            zoom_start: int = 7,
            min_zoom: int = 5
        ) -> str:
        start_coord = next(filter(lambda x: x.index == 0, route.points.points))
        map = folium.Map(location=start_coord.coord, zoom_start=zoom_start, min_zoom=min_zoom)

        for point in route.points.points:
            if point.type == PointType.REST:
                folium.Marker(location=point.coord, popup='HOTEL',
                              icon=folium.Icon(color="blue", icon='home')).add_to(map)    
            elif point.index == 0:
                folium.Marker(location=point.coord, popup='START',
                              icon=folium.Icon(color='darkred', icon='flag')).add_to(map)
            elif point.index == len(route.points.points) - 1:
                folium.Marker(location=point.coord, popup="FINISH",
                              icon=folium.Icon(color='darkgreen', icon='flag')).add_to(map)
            else:
                folium.Marker(location=point.coord, popup="BETWEEN",
                              icon=folium.Icon(color='darkgreen', icon=False)).add_to(map)

        opacity = 0.5
        for polyline in route.polylines:
            folium.PolyLine(
                locations=polyline,
                color="darkgreen",
                weight=self.transport_settings[route.transport_type]['weight'],
                opacity=opacity,
                dash_array=self.transport_settings[route.transport_type]['dash_array']
            ).add_to(map)
            opacity = opacity / 2 + 0.2  

        return map._repr_html_()
    

    def render_empty_map(self: Self):
        pass


async def get_render_service():
    return MapRenderServiceImpl()



MapRenderService = Annotated[
    MapRenderServiceProtocol,
    Depends(get_render_service)
]