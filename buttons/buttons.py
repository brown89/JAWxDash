from dash import html, callback, Output, Input, State

import ids

delete_selected = html.Button(
    "Delete Selected",
    id=ids.Button.DELETE_SELECTED
)


@callback(
    Output(ids.Store.UPLOADED_FILES, 'data'),
    Output(ids.DropDown.UPLOADED_FILES, 'options'),
    Input(ids.Button.DELETE_SELECTED, 'n_clicks'),
    State(ids.DropDown.UPLOADED_FILES, 'value'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def delete_selected_from_list(_, selected_file, current_files):
    # Removing selected file from dropdown
    new_options = [f for f in current_files if f != selected_file]
    del current_files[selected_file]
    return current_files, new_options