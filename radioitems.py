from dash import dcc

# Local imports
import ids


plot_style = dcc.RadioItems(
    id=ids.RadioItems.PLOT_STYLE,
    options=[
       {'label': 'Point', 'value': 'point'},
       {'label': 'Ellipse', 'value': 'ellipse'},
    ],
    value='point',
    inline=True,
)


spot_size = dcc.RadioItems(
    id=ids.RadioItems.SPOT_SIZE,
    options=[
        {'label': 'wo. FP', 'value': 0.3},
        {'label': 'w. FP', 'value': 0.03},
    ],
    value=0.3,
    inline=True,
)