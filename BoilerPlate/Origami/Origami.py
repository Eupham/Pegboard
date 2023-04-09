#This does not make a square or origami yet
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# Define the spherical coordinates for the four vertices of the square
r = 1.0
phi = np.pi/2
theta = np.linspace(np.pi/4, 3*np.pi/4, 4)
vertices = np.zeros((4, 3))
vertices[:, 0] = r * np.sin(theta) * np.cos(phi)
vertices[:, 1] = r * np.sin(theta) * np.sin(phi)
vertices[:, 2] = r * np.cos(theta)


# Define a color to fill the square
color = 'b'

# Create the Poly3DCollection object
square = Poly3DCollection([vertices], alpha=0.25, facecolor=color)

# Plot the square
fig = plt.figure(figsize=(8,8)) # increase size of figure
ax = fig.add_subplot(111, projection='3d')
ax.add_collection(square)

# Add labels to the vertices
for i, vertex in enumerate(vertices):
    ax.text(vertex[0], vertex[1], vertex[2], f'P{i+1}', ha='center', va='center', color='k')

# Use spherical markers for the vertices
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='k', marker='o')

# Set limits and labels
ax.set_xlim([-1.1, 1.1])
ax.set_ylim([-1.1, 1.1])
ax.set_zlim([-1.1, 1.1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add a table showing the addresses of the vertices
rows = ['Vertex', 'X', 'Y', 'Z']
data = [[f'P{i+1}'] + list(vertices[i]) for i in range(4)]
table = ax.table(cellText=data, colLabels=rows, loc='top')
table.auto_set_column_width(col=list(range(4)))
table.auto_set_font_size(True)

fig.subplots_adjust(top=0.8) # adjust plot margins

plt.show()
