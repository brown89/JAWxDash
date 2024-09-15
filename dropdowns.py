# Package import
from dash import dcc, callback, Output, Input, State
import plotly.graph_objs as go


# Local import
import ids
from utilities import add_spot


file_listbox = dcc.Dropdown(id=ids.DropDown.UPLOADED_FILES)


@callback(
    Output(ids.Graph.MAIN, 'figure'),
    Input(ids.DropDown.UPLOADED_FILES, 'value'),
    Input(ids.Slider.ANGLE_OF_INCIDENT, 'value'),
    Input(ids.Slider.SPOT_SIZE, 'value'),
    State(ids.Store.UPLOADED_FILES, 'data'),
    prevent_initial_call=True,
)
def update_graph(selected_file, angle_of_incident, spot_size, current_files):

    # Ensuring valid selection and file store
    if not selected_file or not current_files:
        return go.Figure()
    
    # Retriving data from dcc.Store
    selected_data = current_files[selected_file]

    # Retriving x and y coordinates
    x_coor = selected_data['x']
    y_coor = selected_data['y']

    # Creating a scatter plot
    figure = go.Figure(
        layout=go.Layout(
            title=f'Selected File: {selected_file}',
            xaxis_title='X-axis',
            yaxis_title='Y-axis',
        ),
    )

    for x, y in zip(x_coor, y_coor):
        add_spot(figure, x, y, spot_size, angle_of_incident)
    
    figure.update_layout(
        xaxis=dict(
            #range=[-5, 5],
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