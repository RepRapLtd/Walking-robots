# Petoi 3D animation.
#
# Adrian Bowyer & GPT4
# 3 January 2024
#
# RepRap Ltd
# https://reprapltd.com
#
# Licence: GPL
# See: https://github.com/amine0110/STL-Visualization
#

import vtk
import numpy as np
from scipy.spatial.transform import Rotation as R

bodies = []

def getBodyFromActor(actor):
    global bodies
    for body in bodies:
        if body.actor == actor:
            return body
    return None

def get_rotation_components(vtk_transform):
    # Extract the 4x4 matrix from the vtkTransform
    vtk_matrix = vtk_transform.GetMatrix()

    # Manually convert the VTK matrix to a NumPy array
    matrix_np = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            matrix_np[i, j] = vtk_matrix.GetElement(i, j)

    # Extract the rotation part of the matrix
    rotation_matrix_np = matrix_np[:3, :3]

    # Convert rotation matrix to a quaternion using scipy
    rotation = R.from_matrix(rotation_matrix_np)
    quaternion = rotation.as_quat()  # Returns (x, y, z, w)

    # Reorder quaternion to (w, x, y, z)
    w, x, y, z = quaternion[3], quaternion[0], quaternion[1], quaternion[2]

    return w, x, y, z



class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("LeftButtonUpEvent", self.leftButtonUpEvent)
        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)
        self.body = None

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # Get the new actor
        self.body = getBodyFromActor(picker.GetActor())
        if self.body != None:
            print(self.body.name)
        else:
            print("None")

        # Forward events
        self.OnLeftButtonDown()
        return

    def leftButtonUpEvent(self, obj, event):
        self.body = None
        self.OnLeftButtonUp()
        return

    def mouseMoveEvent(self, obj, event):
        if self.body:
            mousePos = self.GetInteractor().GetEventPosition()
            # Implement the logic for how the mouse movement translates to actor transformation
            # For example, simple translation:
            self.body.rotate([mousePos[0] * 0.01, 1, 0, 0])
            self.body.actor.SetUserTransform(self.body.transform)

        # Forward events
        self.OnMouseMove()
        return

class Body:
    def __init__(self, name):
        self.name = name
        self.translation = [0,0,0]
        self.rotation = [0,1,0,0]
        self.transform = vtk.vtkTransform()

        # Create a reader for a specific STL file
        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.name)

        # Create a mapper for the STL file
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor for the STL file
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        # Create a transform and apply translation and rotation
        self.transform = vtk.vtkTransform()
        self.applyTransform()


    def applyTransform(self):
        self.transform.RotateWXYZ(self.rotation[0], self.rotation[1], self.rotation[2], self.rotation[3])  # Angle, x, y, z
        self.transform.Translate(self.translation)
        self.actor.SetUserTransform(self.transform)


    def translate(self, translation):
        for i in range(3):
            self.translation[i] = self.translation[i] + translation[i]
        self.applyTransform()

    def rotate(self, rotation):
        oldTranslation = [self.translation[0], self.translation[1], self.translation[2]]
        self.translate([-self.translation[0], -self.translation[1], -self.translation[2]])
        newRotation = vtk.vtkTransform()
        newRotation.RotateWXYZ(rotation[0], rotation[1], rotation[2], rotation[3])
        t3 = vtk.vtkTransform()
        t3.PostMultiply()
        t3.Concatenate(newRotation)
        t3.Concatenate(self.transform)
        self.transfom = t3
        self.rotation = get_rotation_components(t3)
        self.translate(oldTranslation)



# Function to create an axis line (origin to unit vector point)
def create_axis_line(renderer, axis_color, point2):
    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(0, 0, 0)
    lineSource.SetPoint2(point2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(axis_color)

    renderer.AddActor(actor)


def main():
    global bodies
    # STL files to display
    names = [
        "legTop.stl",         # Example: Translate by (10, 0, 0) and rotate 45 degrees around x-axis
        "legBottom.stl",      # Translate and rotate another file
        "bodyAssembly.stl"   # And so on for each file
    ]

    # A renderer and render window
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)

    # An interactor
    # An interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Set the custom interactor style
    customStyle = MouseInteractorHighLightActor()
    customStyle.SetDefaultRenderer(renderer)
    renderWindowInteractor.SetInteractorStyle(customStyle)


    create_axis_line(renderer, (1, 0, 0), (50, 0, 0))  # Red for X
    create_axis_line(renderer, (0, 1, 0), (0, 50, 0))  # Green for Y
    create_axis_line(renderer, (0, 0, 1), (0, 0, 50))  # Blue for Z

    # Add actors for each STL file to the scene

    for name in names:
        body = Body(name)
        bodies.append(body)
        renderer.AddActor(body.actor)


    # Set the background color
    renderer.SetBackground(0.1, 0.1, 0.1)

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
