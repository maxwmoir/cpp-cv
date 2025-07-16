import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from server import UDPServer
from sympy import *

# Create figure 
fig = plt.figure()
ax = fig.add_subplot(111)

server = UDPServer(port=9999)
server.run_async()
# Initialize line data
line, = ax.plot([], [], lw=2, color='blue')
line1, = ax.plot([], [], lw=2, color='red')

line.set_label('Ball trajectory')
line1.set_label('Trajectory derivative')

# Axis limits
ax.set_xlim(0, 600)
ax.set_ylim(0, 600)

ax.set_title('Ball trajectory')
ax.set_xlabel('x (pixels)')
ax.set_ylabel('y (pixels)')

x = symbols('x')

# Update function
def update(frame):
    x_data, y_data, dy_data = [], [], []

    if len(server.array) > 0:
        L0 = ((x - server.array[2]) * (x - server.array[4])) / ((server.array[0] - server.array[2]) * (server.array[0] - server.array[4]))
        L1 = ((x - server.array[0]) * (x - server.array[4])) / ((server.array[2] - server.array[0]) * (server.array[2] - server.array[4]))
        L2 = ((x - server.array[0]) * (x - server.array[2])) / ((server.array[4] - server.array[0]) * (server.array[4] - server.array[2]))
        eqn= server.array[1] * L0 + server.array[3] * L1 + server.array[5] * L2
        deqn = diff(eqn, x)
        print(eqn)
        print()
        for i in range(601):
            x_data.append(i)
            y_data.append(-1 * eqn.subs(x, i) + 600)
            dy_data.append(deqn.subs(x, i))

    # Limit to last 100 points for a rolling window
    max_points = 600
    x_data[:] = x_data[-max_points:]
    y_data[:] = y_data[-max_points:]
    dy_data[:] = dy_data[-max_points:]

    # Update line plot
    line.set_data(x_data, y_data)
    line1.set_data(x_data, dy_data)
    return line,

# Animate
ani = FuncAnimation(fig, update, interval=20)

plt.show()
