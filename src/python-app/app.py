from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go # or plotly.express as px
import numpy as np 
import pandas as pd
import math
import random
from server import UDPServer

# fig.add_trace( ... )


app = Dash(__name__, update_title=None)

app.layout = html.Div([
    html.Div(
        dcc.Graph(id='graph', style={'width': '100%'}),
        style={'width': '100%'}  
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

@callback(
        Output('graph', 'figure'),
        Input("graph", "relayoutData"),  
        Input('interval-component', 'n_intervals'))
def update_metrics(relayout_data, n):
    x = np.array([i for i in range(600)])
    y = np.zeros(600)
    z = np.array([-100 * math.cos(i/100) for i in range(600)])
    z = np.array([random.randint(0, 100) for _ in range(600)])
    df = pd.DataFrame({"x": x, "y":y, "z":z})
    fig = px.line_3d(df, x="x", y="y", z="z")

    # if relayout_data and "scene.camera" in relayout_data:
    #     fig.update_layout(scene_camera=relayout_data["scene.camera"])
        
    return fig


app.run(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter