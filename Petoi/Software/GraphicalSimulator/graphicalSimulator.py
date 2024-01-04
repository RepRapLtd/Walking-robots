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

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from stl import mesh
#import glm

# Vertex Shader
VERTEX_SHADER = """
#version 330
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
uniform mat4 transform;
out vec3 theColor;

void main()
{
    gl_Position = transform * vec4(position, 1.0f);
    theColor = normal;
}
"""

# Fragment Shader
FRAGMENT_SHADER = """
#version 330
in vec3 theColor;
out vec4 outColor;
void main()
{
    outColor = vec4(theColor, 1.0);
}
"""

def rotation_matrix(dx, dy):
    # Create rotation matrices for X and Y axes
    Rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(dy), -np.sin(dy), 0],
                   [0, np.sin(dy), np.cos(dy), 0],
                   [0, 0, 0, 1]])

    Ry = np.array([[np.cos(dx), 0, np.sin(dx), 0],
                   [0, 1, 0, 0],
                   [-np.sin(dx), 0, np.cos(dx), 0],
                   [0, 0, 0, 1]])

    return np.dot(Rx, Ry)

def correct_winding_order(triangles, normals):
    corrected_triangles = np.array(triangles)
    for i, (triangle, normal) in enumerate(zip(triangles, normals)):
        # Calculate two sides of the triangle
        side1 = triangle[1] - triangle[0]
        side2 = triangle[2] - triangle[0]

        # Cross product of sides
        cross_product = np.cross(side1, side2)

        # Dot product with the normal
        dot_product = np.dot(cross_product, normal)

        # If the dot product is negative, swap the winding order
        if dot_product > 0:
            corrected_triangles[i][1], corrected_triangles[i][2] = corrected_triangles[i][2], corrected_triangles[i][1]

    return corrected_triangles

def load_stl(filename):
    stl_mesh = mesh.Mesh.from_file(filename)
    return stl_mesh.vectors.reshape(-1).astype(np.float32)
    #return correct_winding_order(stl_mesh.vectors, stl_mesh.normals)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Compile shaders
    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
    )

    # Load STL file
    stl_mesh = load_stl("ab.stl")

    # Create Vertex Buffer Object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, stl_mesh.nbytes, stl_mesh, GL_STATIC_DRAW)

    # Vertex Position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Vertex Normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glDisable(GL_CULL_FACE)

    # Mouse rotation variables
    last_pos = None
    left_button_pressed = False
    rotation = np.identity(4, dtype=np.float32)
    transform_loc = glGetUniformLocation(shader, "transform")

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 is the left mouse button
                    left_button_pressed = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # 1 is the left mouse button
                    left_button_pressed = False
            elif event.type == MOUSEMOTION:
                if left_button_pressed:
                    if last_pos:
                        dx, dy = event.rel
                        dx = np.radians(dx * 0.2)
                        dy = np.radians(dy * 0.2)
                        rotation = np.dot(rotation_matrix(dx, dy), rotation)
                last_pos = event.pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader)

        # Update transform uniform
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rotation)

        glDrawArrays(GL_TRIANGLES, 0, len(stl_mesh) // 3)
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

