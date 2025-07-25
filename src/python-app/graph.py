"""
Ball trajectory tracker
- graph.py

Created: 
- 10/07/25

Author: 
- Max Moir
"""

# Package Imports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from server import Server
from matplotlib.widgets import Slider

# Constants
GRAPH_WIDTH = 600
GRAPH_HEIGHT = 600
SOCK_PORT = 9999

# Create figure 
fig = plt.figure()
ax = fig.add_subplot()
plt.subplots_adjust(bottom=0.25)

ax.set_title('Flight path tracker')
ax.set_xlim(0, GRAPH_WIDTH)
ax.set_ylim(0, GRAPH_HEIGHT)
ax.set_xlabel('x (pixels)')
ax.set_ylabel('y (pixels)')

line, = ax.plot([], [], lw=2, color='blue')
line1, = ax.plot([], [], lw=2, color='red')
line.set_label('Target trajectory')
ax.legend(loc='upper right')

# Initialise slider
slider_ax = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='lightgoldenrodyellow')
point_slider = Slider(
    ax=slider_ax,
    label='Tangent (x)',
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
    """
    Interpolates a polynomial from three points and returns what the output should be with input x_val.
    
    Args:
        x_val    (float): Input to interpolation function
        points ([float]): Three points to interpolate polynomial 
    """
    L0 = ((x_val - points[2]) * (x_val - points[4])) / ((points[0] - points[2]) * (points[0] - points[4]))
    L1 = ((x_val - points[0]) * (x_val - points[4])) / ((points[2] - points[0]) * (points[2] - points[4]))
    L2 = ((x_val - points[0]) * (x_val - points[2])) / ((points[4] - points[0]) * (points[4] - points[2]))

    return points[1] * L0 + points[3] * L1 + points[5] * L2

def polynomial_slope(x_val, points):
    """
    Gives derivative of interpolated polynomial at a specific x value
    
    Args:
        x_val    (float): Input to interpolation derivative 
        points ([float]): Three points to interpolate polynomial 
    """
    L0 = points[1] * (2 * x_val - points[4] - points[2]) / ((points[0] - points[2]) * (points[0] - points[4]))
    L1 = points[3] * (2 * x_val - points[4] - points[0]) / ((points[2] - points[0]) * (points[2] - points[4]))
    L2 = points[5] * (2 * x_val - points[2] - points[0]) / ((points[4] - points[0]) * (points[4] - points[2]))
    return L0 + L1 + L2


def update(frame):
    """
    Function used to update the graph

    Args:
        frame (int): Given by the library
    """
    # x, y, and tangent data vectors
    x_data = [0] * GRAPH_WIDTH
    y_data = [0] * GRAPH_WIDTH
    t_data = [0] * GRAPH_WIDTH

    points = server.last_packet

    tangent_x = point_slider.val 

    # Interpolate a quadratic for the points using a Lagrangian basis
    if validate_packet(points):
        
        # Find tangent slope and location
        tangent_y = interpolate_polynomial(tangent_x, points) 
        tangent_slope = polynomial_slope(tangent_x, points) 

        # Update legend
        line1.set_label(f'Tangent gradient ({-tangent_slope:.2f})')
        ax.legend(loc='upper right')

        # Populate data vectors
        for c in range(600):
            y = interpolate_polynomial(c, points)

            x_data[c] = c
            y_data[c] = -1 * y + GRAPH_HEIGHT

            y_intercept = GRAPH_HEIGHT - tangent_y + tangent_slope * tangent_x
            t_data[c] = -tangent_slope * c + y_intercept

    # Update line plot
    line.set_data(x_data, y_data)
    line1.set_data(x_data,t_data)
    return line,


if __name__ == "__main__":

    # Create and start server
    server = Server(port = SOCK_PORT)
    server.run_async()

    # Draw graph with update function
    ani = FuncAnimation(fig, update, interval = 0.1)
    plt.show()