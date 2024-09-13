from dash import html, callback, Output, Input, State

import ids

delete_selected = html.Button(
    "Delete Selected",
    id=ids.Button.DELETE_SELECTED
)


@callback(
    Output(ids.DropDown.UPLOADED_FILES, 'options'),
    Input(ids.Button.DELETE_SELECTED, 'n_clicks'),
    State(ids.DropDown.UPLOADED_FILES, 'value'),
    State(ids.DropDown.UPLOADED_FILES, 'options'),
    prevent_initial_call=True,
)
def delete_selected_from_list(_, selected_file, current_files):
    # Removing selected file from dropdown
    valid_files = [f for f in current_files if f != selected_file]

    return valid_files