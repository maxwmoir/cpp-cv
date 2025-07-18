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

# Constants
GRAPH_WIDTH = 600
GRAPH_HEIGHT = 600
SOCK_PORT = 9999

# Initialise symbols
x = symbols('x')

# Create figure 
fig = plt.figure()
ax = fig.add_subplot()

ax.set_title('Ball trajectory')
ax.set_xlim(0, GRAPH_WIDTH)
ax.set_ylim(0, GRAPH_HEIGHT)
ax.set_xlabel('x (pixels)')
ax.set_ylabel('y (pixels)')

line, = ax.plot([], [], lw=2, color='blue')
line1, = ax.plot([], [], lw=2, color='red')
line.set_label('Ball trajectory')
line1.set_label('Trajectory derivative')

def validate_packet(packet):
    """
    Validate incoming packet data
    """
    if (len(packet) != 3):
        return False
    
    for value in packet:
        if value > 600 or value < 0:
            return False
    
    return true

def update(frame):
    """
    Function used to update the graph

    Args:
        frame (int): Given by the library
    """
    points = server.last_packet

    # Interpolate a quadratic for the points using a Lagrangian basis
    if validate_packet(points):
        L0 = ((x - points[2]) * (x - points[4])) / ((points[0] - points[2]) * (points[0] - points[4]))
        L1 = ((x - points[0]) * (x - points[4])) / ((points[2] - points[0]) * (points[2] - points[4]))
        L2 = ((x - points[0]) * (x - points[2])) / ((points[4] - points[0]) * (points[4] - points[2]))

        # Function and function derivative equations
        eqn = points[1] * L0 + points[3] * L1 + points[5] * L2
        deqn = diff(eqn, x)
        
        # Populate data vectors
        x_data  = [i for i in range(GRAPH_WIDTH + 1)]
        y_data  = [-1 * eqn.subs(x, i) + GRAPH_HEIGHT for i in range(GRAPH_WIDTH + 1)]
        dy_data = [deqn.subs(x, i) for i in range(GRAPH_WIDTH + 1)]

    # Update line plot
    line.set_data(x_data, y_data)
    line1.set_data(x_data, dy_data)
    return line,


if __name__ == "__main__":

    # Create and start server
    server = Server(port = SOCK_PORT)
    server.run_async()

    # Draw graph with update function
    ani = FuncAnimation(fig, update, interval = 20)
    plt.show()