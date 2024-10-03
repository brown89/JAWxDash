# Library imports
import plotly.graph_objs as go
import numpy as np
import pandas as pd


def gen_spot(x:float, y:float, color, dia_beam:float, angle_incident:float) -> dict:
    minor = dia_beam
    major = dia_beam / np.cos(np.deg2rad(angle_incident))

    x0 = x - 0.5*major
    x1 = x + 0.5*major
    y0 = y - 0.5*minor
    y1 = y + 0.5*minor

    return dict(
        type='circle',
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line=dict(
            color=color,
            width=1,
            dash='solid',
        ),
        fillcolor=color,
        name="spot",
    )


def find_shape_by_attribute(figure:go.Figure, attribute:str, value:str):
    
    # Loops through shapes in figure layout
    for shape in figure.layout.shapes:
        if hasattr(shape, attribute):
            if getattr(shape, attribute) == value:
                return shape
    
    return None


def delete_shape_by_attribute(figure:go.Figure, attribute:str, value:str) -> list:

    # If list empty return empty list
    if not figure.layout.shapes:
        return []
    
    # Collecting index of the shapes matching the attribute value
    to_delete = []
    for i, shape in enumerate(figure.layout.shapes):
        if hasattr(shape, attribute):
            if getattr(shape, attribute) == value:
                to_delete.append(i)
    
    # Removing the matching shapes
    shapes = list(figure.layout.shapes)
    for i in reversed(to_delete):
        shapes.pop(i)
    
    # Setting the shapes
    return shapes


def find_trace_by_attribute(figure:go.Figure, attribute:str, value:str):

    # Loops through data in figure layout
    for trace in figure.data:

        # Check to see if attribute is present
        if hasattr(trace, attribute):

            # Check if attribute value matches
            if getattr(trace, attribute) == value:
                return trace
    
    return None


# Base data structure for xyz-data
class DataXYZ:

    @classmethod
    def from_dataframe(cls, data_frame:pd.DataFrame):
        return DataXYZ(
            data_frame['x'].to_list(),
            data_frame['y'].to_list(),
            data_frame['z'].to_list()
        )
    

    @classmethod
    def from_dict(cls, data_xyz:dict) -> "DataXYZ":
        return DataXYZ(
            data_xyz['x'],
            data_xyz['y'],
            data_xyz['z']
        )
    
    
    def __init__(self, x:list[float], y:list[float], z:list[float]) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
    
    def z_normalized(self) -> list:
        z_baseline = [z - min(self.z) for z in self.z]
        z_max = max(z_baseline)
        return [z/z_max for z in z_baseline]
    

    def width(self) -> float:
        return max(self.x) - min(self.x)
    

    def height(self) -> float:
        return max(self.y) - min(self.y)