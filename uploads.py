# Package import
from dash import dcc, html, callback, Output, Input, State

# Local import
import ids
from readers import parse_contents


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
        'borderRadius': '10px',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=True
)



@callback(
    Output(ids.Store.UPLOADED_FILES, 'data', allow_duplicate=True),
    Output(ids.Div.INFO, 'children', allow_duplicate=True),
    Input(ids.Upload.DRAG_N_DROP, 'contents'),
    State(ids.Upload.DRAG_N_DROP, 'filename'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def update_uploaded_files(contents, filename:str, current_data:dict):
    
    # check if the 'contents' is NOT none
    if contents != None:
        
        # iterate over the contents and filename pairs
        for content, file in zip(contents, filename):

            # check if the file is already loaded
            if file not in current_data:
                data = parse_contents(content, file)

                # check if 'data' is NOT none
                if data:
                    current_data[file] = data.to_dict()
        
        return current_data, html.Div("Uploaded: " + ', '.join([name for name in filename]))
    