# package import
import dash
from dash import callback, dcc, html, Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import numpy as np

# local import
from uploads.drag_n_drop import drag_n_drop
from delete_button import delete_button


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    html.H1("Interactive Dash App with File Upload"),

    # Far left column (File Upload, file_dropdown, Delete button)
    html.Div([
        # Store for keeping uploaded file data
        dcc.Store(id='uploaded-files'),

        html.H4("Upload .txt or .csv Files"),
        drag_n_drop,

        html.H4("Uploaded Files"),
        dcc.Dropdown(id='file_dropdown', multi=True),

        # Delete button
        delete_button,

        html.Div(id='info', style={'border': '1px solid black', 'padding': '10px', 'marginTop': '20px'})

    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    # Middle column (Slider, Plot Area, Info Text Field)
    html.Div([
        html.H4("Slider (0 to 90)"),
        dcc.Slider(id='slider', min=0, max=90, step=1, value=0,
                   marks={i: str(i) for i in range(0, 91, 10)}),

        html.Div([
            dcc.Graph(id='plot-area', style={'height': '400px', 'width': '100%'})
        ], style={'marginTop': '20px'}),

        html.H4("Computed Values"),
        html.Div(id='computed-values', style={'border': '1px solid black', 'padding': '10px', 'marginTop': '20px'})
    ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    # Far right column (Dropdown, Rotate Input, Translate Input)
    html.Div([
        html.H4("Shape Selector"),
        dcc.Dropdown(id='shape-selector', options=[
            {'label': 'Circle', 'value': 'circle'},
            {'label': 'Rectangle', 'value': 'rectangle'},
            {'label': 'Sector', 'value': 'sector'}
        ], value='circle'),

        html.H4("Rotation and Translation Settings"),
        dcc.Input(id="rotation-input", type="number", placeholder="Rotation (degrees)", value=0, style={'marginTop': '10px'}),
        dcc.Input(id="translation-input", type="number", placeholder="Translation (units)", value=0, style={'marginTop': '10px'}),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'})
])


# Callback for plotting items in file_dropdown
@callback(
    Output('plot-area', 'figure'),
    Input('file_dropdown', 'value'),
    Input('shape-selector', 'value'),
    Input('slider', 'value'),
    Input('rotation-input', 'value'),
    Input('translation-input', 'value')
)
def update_plot(selected_files, shape, slider_value, rotation, translation):
    # Plot area setup
    fig = go.Figure()

    # Example plotting logic based on shape and file_dropdown items (no real data yet)
    for file in selected_files:
        if shape == 'circle':
            t = np.linspace(0, 2 * np.pi, 100)
            x = np.cos(t)
            y = np.sin(t)
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=file))
        elif shape == 'rectangle':
            rect_x = [-1, 1, 1, -1, -1]
            rect_y = [-1, -1, 1, 1, -1]
            fig.add_trace(go.Scatter(x=rect_x, y=rect_y, mode='lines', name=file))
        elif shape == 'sector':
            sector_x = [0, 1, 0]
            sector_y = [0, 1, 1]
            fig.add_trace(go.Scatter(x=sector_x, y=sector_y, mode='lines', name=file))

        # Apply rotation and translation (dummy effect for illustration)
        fig.update_layout(
            title=f"Slider: {slider_value}, Rotation: {rotation}, Translation: {translation}"
        )

    return fig

# Callback for computing and displaying values
@callback(
    Output('computed-values', 'children'),
    Input('file_dropdown', 'value'),
    Input('rotation-input', 'value'),
    Input('translation-input', 'value')
)
def compute_values(selected_files, rotation, translation):
    # Example computation
    total_items = len(selected_files)
    computed_val = f"Total files: {total_items}, Rotation: {rotation}, Translation: {translation}"
    return computed_val

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
