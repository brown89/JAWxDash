from dash import Dash, dcc, html 


# Local import
import ids
from uploads import drag_n_drop
from dropdowns import file_listbox
from divs import info_panel
from buttons import delete_selected
from sliders import angle_of_incident


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Initiating 'Store' for holding uploaded files i.e. *.txt and *.csv
    dcc.Store(id=ids.Store.UPLOADED_FILES, data={}),

    # Left column
    html.Div(
        [
            drag_n_drop,
            file_listbox,
            delete_selected,
        ], 
        style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}
    ),

    # Middle column
    html.Div(
        [
            html.H4("Slider (0 to 89)"),
            angle_of_incident,
        ], 
        style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}
    ),
    
    # Bottom info panel
    info_panel
])



if __name__ == '__main__':
    app.run(debug=True)
