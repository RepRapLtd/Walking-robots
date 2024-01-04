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

import open3d as o3d
import numpy as np
import copy
import time

def create_mesh_cylinder(radius, height, resolution=30, color=[0.0, 0.5, 1.0]):
    mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height, resolution=resolution, split=4)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color(color)
    return mesh

def main():
    # Load STL file
    #stl_mesh = o3d.io.read_triangle_mesh("bodyAssembly.stl")
    stl_mesh = o3d.io.read_triangle_mesh("ab.stl")
    stl_mesh.compute_vertex_normals()

    # Create first cylinder
    cylinder = create_mesh_cylinder(0.2, 1.0, color=[0.0, 0.5, 1.0])

    # Initialize Visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # Add geometries to visualizer
    vis.add_geometry(cylinder)
    vis.add_geometry(stl_mesh)

    for frame in range(360):
        angle = frame / 20.0
        R = stl_mesh.get_rotation_matrix_from_xyz((0, angle, 0))

        # Rotate STL mesh
        rotated_mesh = copy.deepcopy(stl_mesh)
        rotated_mesh.rotate(R, center=(0, 0, 0))

        # Clear previous geometries
        vis.clear_geometries()

        # Add updated geometries
        vis.add_geometry(cylinder)
        vis.add_geometry(rotated_mesh)

        vis.poll_events()
        vis.update_renderer()
        time.sleep(0.05)

    vis.destroy_window()

if __name__ == "__main__":
    main()

