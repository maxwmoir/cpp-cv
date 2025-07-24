"""
Ball trajectory tracker
- graph.py

Created: 
- 10/07/25

Author: 
- Max Moir
"""

# Package Imports
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from server import Server
from matplotlib.widgets import Slider

# Constants
GRAPH_WIDTH = 600
GRAPH_HEIGHT = 600
SOCK_PORT = 9999

# Initialise symbols
x = symbols('x')

# Create figure 
fig = plt.figure()
ax = fig.add_subplot()
plt.subplots_adjust(bottom=0.25)

ax.set_title('Target trajectory tracker')
ax.set_xlim(0, GRAPH_WIDTH)
ax.set_ylim(0, GRAPH_HEIGHT)
ax.set_xlabel('x (pixels)')
ax.set_ylabel('y (pixels)')

line, = ax.plot([], [], lw=2, color='blue')
line1, = ax.plot([], [], lw=2, color='red')
line.set_label('Ball trajectory')
line1.set_label('Trajectory derivative')
ax.legend(loc='upper right')

slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
point_slider = Slider(
    ax=slider_ax,
    label='Point (x)',
    valmin=0,
    valmax=GRAPH_WIDTH - 1,
    valinit=300,
    valstep=1
)

def validate_packet(packet):
    """
    Validate incoming packet data
    """
    if (len(packet) != 6):
        return False
    
    for value in packet:
        if value > 600 or value < 0:
            return False
    
    return True

def interpolate_polynomial(x_val, points):
    L0 = ((x_val - points[2]) * (x_val - points[4])) / ((points[0] - points[2]) * (points[0] - points[4]))
    L1 = ((x_val - points[0]) * (x_val - points[4])) / ((points[2] - points[0]) * (points[2] - points[4]))
    L2 = ((x_val - points[0]) * (x_val - points[2])) / ((points[4] - points[0]) * (points[4] - points[2]))

    return points[1] * L0 + points[3] * L1 + points[5] * L2


def derivative_calc(x, a, b, c, d):
    num = d * (2 * x - b - a) 
    denom = (c - a) * (c - b)
    return num / denom

def update(frame):
    """
    Function used to update the graph

    Args:
        frame (int): Given by the library
    """

    x_data = [0] * GRAPH_WIDTH
    y_data = [0] * GRAPH_WIDTH
    dy_data = [0] * GRAPH_WIDTH

    points = server.last_packet

    point = point_slider.val 

    # Interpolate a quadratic for the points using a Lagrangian basis
    if validate_packet(points):

        ay = interpolate_polynomial(point, points) 

        for c in range(600):
            x_data[c] = c
            
            L3 = derivative_calc(point, points[2], points[4], points[0], points[1])
            L4 = derivative_calc(point, points[0], points[4], points[2], points[3])
            L5 = derivative_calc(point, points[0], points[2], points[4], points[5])

            # Function and function derivative equations
            y = interpolate_polynomial(c, points)
            dy = L3 + L4 + L5 

            # Populate data vectors
            y_data[c] = -1 * y + GRAPH_HEIGHT
            dist =  (GRAPH_HEIGHT - ay) + dy * point
            dy_data[c] = -dy * c + dist

    # Update line plot
    line.set_data(x_data, y_data)
    line1.set_data(x_data,dy_data)
    return line,


if __name__ == "__main__":

    # Create and start server
    server = Server(port = SOCK_PORT)
    server.run_async()

    # Draw graph with update function
    ani = FuncAnimation(fig, update, interval = 0.1)
    plt.show()