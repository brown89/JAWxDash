# Package import
from dash import dcc, html, callback, Output, Input, State
#import base64
#import io
#import pandas as pd

# Local import
import ids

drag_n_drop = dcc.Upload(
    id=ids.Upload.DRAG_N_DROP,
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=True
)

@callback(
    Output(ids.DropDown.UPLOADED_FILES, 'options', allow_duplicate=True),
    Input(ids.Upload.DRAG_N_DROP, 'contents'),
    State(ids.Upload.DRAG_N_DROP, 'filename'),
    State(ids.DropDown.UPLOADED_FILES, 'options'),
    prevent_initial_call=True
)
def update_dropdown(contents, dropped_files, current_files):
    if contents != None:
        new_files = [name for name in dropped_files]

    return sorted(current_files + new_files) if current_files else sorted(new_files)
