import plotly.express as px
import numpy as np 
import pandas as pd
import math

x = np.array([i for i in range(600)])
y = np.zeros(600)
z = np.array([-100 * math.cos(i/100) for i in range(600)])
df = pd.DataFrame({"x": x, "y":y, "z":z})



import plotly.graph_objects as go # or plotly.express as px
fig = px.line_3d(df, x="x", y="y", z="z")
# fig.add_trace( ... )
# fig.update_layout( ... )

from dash import Dash, dcc, html

app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter