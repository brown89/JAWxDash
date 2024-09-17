# Library imports
from dash import dcc, callback, Output, Input, State
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Local imports
import ids
from utilities import gen_spot, find_data_by_attribute, delete_shape_by_attribute
from sample_outlines import sample_outlines


# Initializing the plotly figure with axis titles
figure = go.Figure(
    layout=go.Layout(
        xaxis_title='X-axis (mm)',
        yaxis_title='Y-axis (mm)',
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
    ),
)

# Adding a placeholder for colormap
figure.add_trace(go.Scatter(
        x=[None],
        y=[None],
        name='colormap_placeholder',
    ))

# Adding a placeholder for sample outline
# 8in wafer
r = 1*25.4



# Setting dcc.Graph object
main_graph = dcc.Graph(
    id=ids.Graph.MAIN, 
    style={'height': '900px', 'width': '100%'},
    figure=figure,
)

@callback(
    Output(ids.Graph.MAIN, 'figure', allow_duplicate=True),
    Input(ids.DropDown.UPLOADED_FILES, 'value'),
    Input(ids.Slider.ANGLE_OF_INCIDENT, 'value'),
    Input(ids.Slider.SPOT_SIZE, 'value'),
    Input(ids.DropDown.COLORMAPS, 'value'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    State(ids.Graph.MAIN, 'figure'),
    prevent_initial_call=True,
)
def update_graph(selected_file, angle_of_incident, spot_size, selected_colormap, current_files, figure) -> go.Figure:

    # Ensuring valid selection and file store
    if not selected_file or not current_files:
        return None
    
    figure = go.Figure(figure)
    
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

    # Generating spots and collecting
    shapes = []
    for x, y, c in zip(x_coor, y_coor, colors):
        shapes.append(gen_spot(x, y, c, spot_size, angle_of_incident))
    
    # Calculating zoom window
    x_min, x_max = min(x_coor), max(x_coor)
    y_min, y_max = min(y_coor), max(y_coor)

    width = x_max - x_min
    height = y_max - y_min

    scale = 0.2  # scale factor for amount of padding

    # Updating layout with
    # - title
    # - shapes
    # - axis ratio 1:1
    figure.update_layout(
        title=f"Selected file: {selected_file}",
        shapes=shapes,
        xaxis=dict(
            range=[x_min-scale*width, x_max+scale*width],
            #scaleanchor="y",
            #scaleratio=1,
        ),
        yaxis=dict(
            range=[y_min-scale*height, y_max+scale*height],
            #scaleanchor="x",
            #scaleratio=1,
        ),
    )

    # Adding a dummy scatter plot to display colorbar
    data = find_data_by_attribute(figure, "name", "colormap_placeholder")
    data.update(
        mode='markers',
        marker=dict(
            size=10,
            color=[int(min(z_coor)), int(max(z_coor))],
            showscale=True,
            colorscale=colormap,
            colorbar=dict(
                title="Color Scale",
                titleside="right",
                tickvals=[t for t in range(int(min(z_coor)), int(max(z_coor)), 5)],
                ticks="outside",
                len=0.8,
            )
        )
    )

    return figure


@callback(
    Output(ids.Graph.MAIN, 'figure'),
    Input(ids.DropDown.SAMPLE_OUTLINE, 'value'),
    State(ids.Graph.MAIN, 'figure'),
    prevent_initial_call=True,
)
def update_sample_outline(selected_outline:str, figure:dict) -> go.Figure:

    # Converting the figure from dict to go.Figure
    figure = go.Figure(figure)

    # If no outline selected return the same figure
    if not selected_outline:
        return figure
    
    # Deletes shape if exist
    figure = delete_shape_by_attribute(figure, "name", "sample_outline")

    # Creates new "sample_outline" and adds it to the figure
    shape = sample_outlines[selected_outline]
    figure.add_shape(
        shape
    )

    # Explicit update of the figure
    figure.update_layout()

    return figure
