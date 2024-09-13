from dash import html, callback, Output, Input

import ids

info_panel = html.Div(
    id=ids.Div.INFO, 
    style={'border': '1px solid black', 'padding': '10px', 'marginTop': '20px'}
)

@callback(
    Output(ids.Div.INFO, 'children'),
    Input(ids.Upload.DRAG_N_DROP, 'filename'),
    prevent_initial_call=True
)
def update_info_panel(filename):
    if filename != None:
        return html.Div([name for name in filename])
    