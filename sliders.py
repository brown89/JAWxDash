from dash import dcc


# Local import
import ids


angle_of_incident = dcc.Slider(
    id=ids.Slider.ANGLE_OF_INCIDENT, 
    min=0, 
    max=89, 
    step=1, 
    value=65,
    marks={i: str(i) for i in range(0, 89, 5)},
)
