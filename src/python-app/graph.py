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

# Local imports
from server import UDPServer

# Initialise symbols
x = symbols('x')

# Create figure 
fig = plt.figure()
ax = fig.add_subplot(111)

# Format graph 
ax.set_title('Ball trajectory')
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)
ax.set_xlabel('x (pixels)')
ax.set_ylabel('y (pixels)')

line, = ax.plot([], [], lw=2, color='blue')
line1, = ax.plot([], [], lw=2, color='red')
line.set_label('Ball trajectory')
line1.set_label('Trajectory derivative')

# Update function
def update(frame):
    x_data, y_data, dy_data = [], [], []

    if len(server.array) > 0:
        L0 = ((x - server.array[2]) * (x - server.array[4])) / ((server.array[0] - server.array[2]) * (server.array[0] - server.array[4]))
        L1 = ((x - server.array[0]) * (x - server.array[4])) / ((server.array[2] - server.array[0]) * (server.array[2] - server.array[4]))
        L2 = ((x - server.array[0]) * (x - server.array[2])) / ((server.array[4] - server.array[0]) * (server.array[4] - server.array[2]))

        eqn = server.array[1] * L0 + server.array[3] * L1 + server.array[5] * L2
        deqn = diff(eqn, x)

        for i in range(601):
            x_data.append(i)
            y_data.append(-1 * eqn.subs(x, i) + 600)
            dy_data.append(deqn.subs(x, i))

    max_points = 600
    x_data[:] = x_data[-max_points:]
    y_data[:] = y_data[-max_points:]
    dy_data[:] = dy_data[-max_points:]

    # Update line plot
    line.set_data(x_data, y_data)
    line1.set_data(x_data, dy_data)
    return line,


if __name__ == "__main__":

    # Create and start server
    server = UDPServer(port=9999)
    server.run_async()

    # Draw graph with update function
    ani = FuncAnimation(fig, update, interval=20)
    plt.show()