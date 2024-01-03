# Petoi 3D animation.
#
# Adrian Bowyer & GPT4
# 3 January 2024
#
# RepRap Ltd
# https://reprapltd.com
#
# Licence: GPL
#

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mplot3d
from matplotlib.animation import FuncAnimation
from stl import mesh

# Load your STL file (replace 'your_file.stl' with your file path)
your_mesh = mesh.Mesh.from_file('ab.stl')

def calculate_normals(your_mesh):
    normals = []
    for face in your_mesh.vectors:
        v1 = face[1] - face[0]
        v2 = face[2] - face[0]
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        normals.append(normal)
    return np.array(normals)

def create_cylinder(radius, height, elevation=0, resolution=30):
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, height, resolution)
    U, V = np.meshgrid(u, v)
    X = radius * np.cos(U)
    Y = radius * np.sin(U)
    Z = V + elevation
    return X, Y, Z

def update(frame):
    angle = frame / 2
    ax.cla()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(0, 2)

    # First cylinder (static)
    X, Y, Z = create_cylinder(0.2, 1)
    ax.plot_surface(X, Y, Z, color='blue', alpha=0.6)

    # Rotate the mesh
    transformed_mesh = mesh.Mesh(your_mesh.data.copy())
    transformed_mesh.rotate([0.5, 0.5, 0.5], angle)
    transformed_mesh.translate([0, 0, 1])

    # Calculate normals and simulate lighting
    normals = calculate_normals(transformed_mesh)
    light_direction = np.array([0, 0, 1])  # Change as needed
    intensities = np.dot(normals, light_direction)

    # Create a color array based on intensities
    colors = plt.cm.viridis((intensities - intensities.min()) / (intensities.max() - intensities.min()))

    # Create and add the collection to the plot with matching edge colors
    poly3d = mplot3d.art3d.Poly3DCollection(transformed_mesh.vectors, facecolors=colors, edgecolors=colors)
    ax.add_collection3d(poly3d)

    # Remove the axes and make panes transparent
    ax.set_axis_off()
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 360), interval=25)
plt.show()
