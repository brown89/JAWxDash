# Library imports
from dash import dcc

# Local imports
import ids


main_graph = dcc.Graph(
    id=ids.Graph.MAIN, 
    style={'height': '900px', 'width': '100%'}
)
