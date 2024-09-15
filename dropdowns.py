# Package import
from dash import dcc
import plotly.express as px


# Local import
import ids


file_listbox = dcc.Dropdown(
    id=ids.DropDown.UPLOADED_FILES,
    options=[],
    value='',
    multi=False,
    clearable=False,
)


colormaps = dcc.Dropdown(
    id=ids.DropDown.COLORMAPS,
    options=sorted([colorscale for colorscale in px.colors.named_colorscales()]),
    value='viridis',
    multi=False,
    clearable=False,
)
