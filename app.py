from dash import Dash, dcc, html 
import plotly.graph_objs as go

# Local import
import ids
from uploads import drag_n_drop
from dropdowns import file_listbox, colormaps, sample_outline
from divs import info_panel
from buttons import delete_selected
from sliders import angle_of_incident, spot_size
from graphs import main_graph
from stores import files_store


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Initiating 'Store' for holding uploaded files i.e. *.txt and *.csv
    files_store,

    # Left column
    html.Div(
        [
            drag_n_drop,
            file_listbox,
            delete_selected,
        ], 
        style={
            'width': '15%', 
            'display': 'inline-block', 
            'verticalAlign': 'top', 
            'padding': '10px'
        }
    ),

    # Middle column
    html.Div(
        [
            # Main graph window
            main_graph,
        ], 
        style={
            'width': '60%', 
            'display': 'inline-block', 
            'verticalAlign': 'top', 
            'padding': '10px'
        }
    ),

    # Right column
    html.Div(
        [
            html.H6("Angle of incident (deg)", style={'textAlign': 'center',}),
            angle_of_incident,
            html.H6("Spot size (mm)", style={'textAlign': 'center',}),
            spot_size,
            html.H6("Colormap", style={'textAlign': 'center',}),
            colormaps,
            html.H6("Sample outline", style={'textAlign': 'center',}),
            sample_outline,
        ], 
        style={
            'width': '20%', 
            'display': 'inline-block', 
            'verticalAlign': 'top', 
            'padding': '10px'
        }
    ),
    
    # Bottom info panel
    info_panel
])



if __name__ == '__main__':
    app.run(debug=True)
