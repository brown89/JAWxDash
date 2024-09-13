from dash import Dash, dcc, html 


# Local import
import ids
from uploads.drag_n_drop import drag_n_drop
from dropdowns.file_listbox import file_listbox
from divs.info_panel import info_panel
from buttons.buttons import delete_selected 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Initiating 'Store' for holding uploaded files i.e. *.txt and *.csv
    dcc.Store(id=ids.Store.UPLOADED_FILES),

    # Left column
    html.Div([
        drag_n_drop,
        file_listbox,
        delete_selected,
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
    info_panel
])



if __name__ == '__main__':
    app.run(debug=True)
