from dash import dcc
import numpy as np

# Local import
import ids


angle_of_incident = dcc.Slider(
    id=ids.Slider.ANGLE_OF_INCIDENT, 
    min=45, 
    max=85, 
    step=1, 
    value=65,
    marks={i: str(i) for i in range(45, 86, 5)},
)
