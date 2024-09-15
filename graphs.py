# Library imports
from dash import dcc, callback, Output, Input, State
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Local imports
import ids
from utilities import add_spot


main_graph = dcc.Graph(
    id=ids.Graph.MAIN, 
    style={'height': '900px', 'width': '100%'}
)

@callback(
    Output(ids.Graph.MAIN, 'figure'),
    Input(ids.DropDown.UPLOADED_FILES, 'value'),
    Input(ids.Slider.ANGLE_OF_INCIDENT, 'value'),
    Input(ids.Slider.SPOT_SIZE, 'value'),
    Input(ids.DropDown.COLORMAPS, 'value'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    #prevent_initial_call=True,
)
def update_graph(selected_file, angle_of_incident, spot_size, selected_colormap, current_files) -> go.Figure:

    # Ensuring valid selection and file store
    if not selected_file or not current_files:
        return go.Figure(
            layout=go.Layout(
                xaxis_title='X-axis (mm)',
                yaxis_title='Y-axis (mm)',
            )
        )
    
    # Retriving data from dcc.Store
    selected_data = current_files[selected_file]

    # Retriving x and y coordinates
    x_coor = selected_data['x']
    y_coor = selected_data['y']
    z_coor = np.asarray(selected_data['z'])

    # Normalizing z_coor to colors
    z_offset = z_coor - min(z_coor)
    z_norm = z_offset/max(z_offset)

    # Making colors
    colormap = selected_colormap
    colors = px.colors.sample_colorscale(colormap, z_norm)

    # Creating a scatter plot
    figure = go.Figure(
        layout=go.Layout(
            title=f'Selected File: {selected_file}',
            xaxis_title='X-axis (mm)',
            yaxis_title='Y-axis (mm)',
        ),
    )

    for x, y, c in zip(x_coor, y_coor, colors):
        add_spot(figure, x, y, c, spot_size, angle_of_incident)
    
    figure.update_layout(
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            range=[-45, 5],
            scaleanchor="x",
            scaleratio=1,
        )
    )

    return figure