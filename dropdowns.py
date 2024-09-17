# Package import
from dash import dcc
import plotly.express as px


# Local import
import ids
from sample_outlines import sample_outlines


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


sample_outline = dcc.Dropdown(
    id=ids.DropDown.SAMPLE_OUTLINE,
    options=list(sample_outlines.keys()),
    multi=False,
    clearable=True,
)