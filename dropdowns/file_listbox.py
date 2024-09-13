# Package import
from dash import dcc, callback, Output, Input, State

# Local import
import ids


file_listbox = dcc.Dropdown(id=ids.DropDown.UPLOADED_FILES)

