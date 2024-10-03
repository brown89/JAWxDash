# Library imports
import plotly.graph_objs as go
import numpy as np


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
