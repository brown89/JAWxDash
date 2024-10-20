# Library imports
from dash import dcc, callback, Output, Input, State
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

# Local imports
import ids
from utilities import gen_spot, delete_shape_by_attribute
from readers import DataXYC
from sample_outlines import sample_outlines


# template for the figure layout
FIGURE_LAYOUT = dict(
    xaxis_title = "X-axis (mm)",
    yaxis_title = "Y-axis (mm)",
    xaxis=dict(
        scaleanchor="y",
        scaleratio=1,
    ),
    yaxis=dict(
        scaleanchor="x",
        scaleratio=1,
    ),
)


CRITICAL_COUNT = 500


# Base template for the figure
figure = go.Figure(
    layout=go.Layout(
        FIGURE_LAYOUT
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
layout = dcc.Graph(
    id=ids.Graph.MAIN, 
    style={'height': '900px', 'width': '100%'},
    figure=figure,
)

@callback(
    Output(ids.Graph.MAIN, 'figure', allow_duplicate=True),
    Output(ids.DropDown.Z_DATA, 'value'),
    Output(ids.DropDown.Z_DATA, 'options'),
    Input(ids.DropDown.UPLOADED_FILES, 'value'),
    Input(ids.Slider.ANGLE_OF_INCIDENT, 'value'),
    Input(ids.Slider.SPOT_SIZE, 'value'),
    Input(ids.DropDown.COLORMAPS, 'value'),
    Input(ids.DropDown.Z_DATA, 'value'),
    State(ids.DropDown.SAMPLE_OUTLINE, 'value'), # Sample outline as an input is handled seperatly
    State(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def update_graph(
        selected_file:str, 
        angle_of_incident:int, 
        spot_size:float, 
        selected_colormap:str,
        selected_z_data:str, 
        selected_outline:str, 
        current_files:dict
    ) -> go.Figure:
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
    sample = DataXYC.from_dict(selected_data)

    # Checking for selected Z-data
    if not selected_z_data:
        if sample.len() >= 8:
            # Defaults to 7, we're aiming for "Thickness nm"
            key = sample.data.columns[7]
        else:
            key = sample.data.columns[0]
    
    else:
        key = selected_z_data
    

    # Making colors
    colormap = selected_colormap
    colors = px.colors.sample_colorscale(
        colorscale=colormap, 
        samplepoints=sample.normalized()
    )

    shapes = []
    x = [None]
    y = [None]
    marker_color = 'rgb(255,0,0)'

    if sample.len() > CRITICAL_COUNT:
        # Plot at scatter
        x = sample.data.x
        y = sample.data.y
        marker_color = sample.data[key]

    
    else:
        # Plot as ellipse
        # Initializing list of shapes + Generating spots and collecting
        shapes = [
            gen_spot(x, y, c, spot_size, angle_of_incident) 
            for x, y, c 
            in zip(sample.data.x, sample.data.y, colors)
        ]

    
    
    # Generating outline if any
    if selected_outline:
        shapes.append(sample_outlines[selected_outline])
    
    # Creating a new figure object
    layout_updates = dict(
        title = f"Selected file: {selected_file}",
        shapes = tuple(shapes),
        xaxis = {'range': sample.x_range()} | FIGURE_LAYOUT['xaxis'],
        yaxis = {'range': sample.y_range()} | FIGURE_LAYOUT['yaxis'],
    )
 
    figure = go.Figure(
        layout=go.Layout(
            FIGURE_LAYOUT | layout_updates  # Joining the template with the updates
        ),
    )
    

    # Adding a dummy scatter plot to display colorbar
    figure.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker_color=marker_color,
        marker=dict(
            size=5,
            color=[int(min(sample.data[key])), int(max(sample.data[key]))],
            showscale=True,
            colorscale=colormap,
            colorbar=dict(
                title=key,
                titleside="right",
                tickvals=[int(x) for x in np.linspace(min(sample.data[key]), max(sample.data[key]), 10)],
                ticks="outside",
                len=0.8,
            )
        ),
        name='colormap_placeholder',
    ))
    
    value = key
    options = sample.data.columns
    
    return figure, value, options


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