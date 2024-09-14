# Package import
from dash import dcc, callback, Output, Input, State

# Local import
import ids


file_listbox = dcc.Dropdown(id=ids.DropDown.UPLOADED_FILES)

@callback(
    Output(ids.DropDown.UPLOADED_FILES, 'options', allow_duplicate=True),
    Input(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def update_listbox(current_data) -> list[str]:
    entries = list(current_data.keys())

    return sorted(entries)
