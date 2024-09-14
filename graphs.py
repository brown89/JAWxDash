# Library imports
from dash import dcc

# Local imports
import ids


main_graph = dcc.Graph(id=ids.Graph.MAIN, style={'height': '800px', 'width': '100%'})
