from dash import dcc
import numpy as np

# Local import
import ids


angle_of_incident = dcc.Slider(
    id=ids.Slider.ANGLE_OF_INCIDENT, 
    min=45, 
    max=89, 
    step=1, 
    value=65,
    marks={i: str(i) for i in range(45, 89, 5)},
)

spot_size = dcc.Slider(
    id=ids.Slider.SPOT_SIZE, 
    min=0.3, 
    max=3, 
    step=0.3, 
    value=3,
    marks={i: f"{i:.1f}" for i in np.arange(0.3, 3.3, 0.3)},
)
