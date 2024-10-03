# Library imports
from dash import dcc, callback, Output, Input, State
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# Local imports
import ids
from utilities import DataXYZ, gen_spot, find_trace_by_attribute, delete_shape_by_attribute
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
    State(ids.DropDown.SAMPLE_OUTLINE, 'value'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def update_graph(selected_file, angle_of_incident, spot_size, selected_colormap, selected_outline:str, current_files) -> go.Figure:
    """
    Updates the graph object uppon changes to one of the following:
    - File dropdown
    - Angle of incident
    - Spot size
    - Colormap dropdown
    - Sample outline


    """
    # Ensuring valid selection and file store
    if not selected_file or not current_files:
        return None
    
        
    # Retriving data from dcc.Store
    selected_data = current_files[selected_file]

    # Retriving data
    data = DataXYZ.from_dict(selected_data)

    # Making colors
    colormap = selected_colormap
    colors = px.colors.sample_colorscale(colormap, data.z_normalized())

    # Initializing list of shapes
    shapes = []
    
    # Generating spots and collecting
    for x, y, c in zip(data.x, data.y, colors):
        shapes.append(gen_spot(x, y, c, spot_size, angle_of_incident))
    
    # Generating outline if any
    if selected_outline:
        shapes.append(sample_outlines[selected_outline])
    
    # Calculating zoom window
    x_min, x_max = min(data.x), max(data.x)
    y_min, y_max = min(data.y), max(data.y)

    scale = 0.2  # scale factor for amount of padding

    # Creating a new figure object
    figure = go.Figure(
        layout=go.Layout(
            title=f"Selected file: {selected_file}",
            shapes=tuple(shapes),
            xaxis_title='X-axis (mm)',
            yaxis_title='Y-axis (mm)',
            xaxis=dict(
                range=[x_min-scale*data.width(), x_max+scale*data.width()],
                scaleanchor="y",
                scaleratio=1,
            ),
            yaxis=dict(
                range=[y_min-scale*data.height(), y_max+scale*data.height()],
                scaleanchor="x",
                scaleratio=1,
            ),
        ),
    )
    

    # Adding a dummy scatter plot to display colorbar
    figure.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            size=10,
            color=[int(min(data.z)), int(max(data.z))],
            showscale=True,
            colorscale=colormap,
            colorbar=dict(
                title="Color Scale",
                titleside="right",
                tickvals=[t for t in range(int(min(data.z)), int(max(data.z)), 5)],
                ticks="outside",
                len=0.8,
            )
        ),
        name='colormap_placeholder',
    ))
    
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
    shapes = delete_shape_by_attribute(figure, "name", "sample_outline")

    # Creates new "sample_outline" and adds it to the figure
    shape = sample_outlines[selected_outline]
    
    # Add outline to list of shapes
    shapes.append(shape)

    # Explicit update of the figure
    figure.layout.shapes = shapes
        #shapes=tuple(shapes),
    #)

    return figure