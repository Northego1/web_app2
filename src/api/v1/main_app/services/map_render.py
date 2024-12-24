from typing import Annotated, Protocol, Self, Union

from fastapi import Depends
import folium


class MapRenderServiceProtocol(Protocol):
    def render_by_polyline(self: Self):
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
        self.colors = colors = (
            'blue', 'green', 'purple', 'darkred', 'darkgreen', 'darkblue', 'pink', 'cadetblue')


    def render_by_polyline(
            self: Self,
            coords: Union[tuple, list],
            *,
            zoom_start: int = 7,
            min_zoom: int = 4
        ):
        map = folium.Map(location=self.coords[0], zoom_start=zoom_start, min_zoom=min_zoom)

        for index, coord in enumerate(coords):
            if isinstance(coord, list):
                folium.Marker(location=coord, popup='HOTEL',
                              icon=folium.Icon(color=self.colors[index], icon='home')).add_to(map)    
            elif index == 0:
                folium.Marker(location=self.coords[0], popup='START',
                              icon=folium.Icon(color='lightgray', icon='flag')).add_to(map)
            elif index == len(self.routes):
                folium.Marker(location=coord, popup="FINISH",
                              icon=folium.Icon(color='black', icon='flag')).add_to(map)
            else:
                folium.Marker(location=coord, popup="BETWEEN",
                              icon=folium.Icon(color=self.colors[index], icon=False)).add_to(map)
                

    def render_empty_map(self: Self):
        pass


async def get_render_service():
    return MapRenderServiceImpl()



MapRenderService = Annotated[
    MapRenderServiceProtocol,
    Depends(get_render_service)
]