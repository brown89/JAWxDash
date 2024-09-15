import plotly.graph_objs as go
import numpy as np


def add_spot(fig:go.Figure, x:float, y:float, c, d_beam:float, a_incident:float) -> None:

    minor = d_beam
    major = d_beam / np.cos(np.deg2rad(a_incident))

    x0 = x - 0.5*major
    x1 = x + 0.5*major
    y0 = y - 0.5*minor
    y1 = y + 0.5*minor

    fig.add_shape(
        type='circle',
        x0=x0,
        y0=y0,
        x1=x1,
        y1=y1,
        line=dict(
            color=c,
            width=1,
            dash='solid',
        ),
        fillcolor=c,
    )
    return None
