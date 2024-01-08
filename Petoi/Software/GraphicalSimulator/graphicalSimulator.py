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

actor_to_filename = {}  # Global dictionary to map actors to filenames

def get_stl_file_from_actor(actor):
    # Retrieve the filename associated with this actor
    return actor_to_filename.get(actor, None)

class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)
        self.selectedActor = None
        self.transform = vtk.vtkTransform()

    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # Get the new actor
        self.selectedActor = picker.GetActor()
        print(get_stl_file_from_actor(self.selectedActor))

        # Forward events
        self.OnLeftButtonDown()
        return

    def mouseMoveEvent(self, obj, event):
        if self.selectedActor:
            mousePos = self.GetInteractor().GetEventPosition()
            # Implement the logic for how the mouse movement translates to actor transformation
            # For example, simple translation:
            self.transform.Translate(mousePos[0] * 0.01, mousePos[1] * 0.01, 0)
            self.selectedActor.SetUserTransform(self.transform)

        # Forward events
        self.OnMouseMove()
        return


def create_stl_actor(file_name, translation, rotation):
    # Create a reader for a specific STL file
    reader = vtk.vtkSTLReader()
    reader.SetFileName(file_name)

    # Create a mapper for the STL file
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor for the STL file
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a transform and apply translation and rotation
    transform = vtk.vtkTransform()
    transform.Translate(translation)
    transform.RotateWXYZ(rotation[0], rotation[1], rotation[2], rotation[3])  # Angle, x, y, z

    actor.SetUserTransform(transform)
    global actor_to_filename
    actor_to_filename[actor] = file_name
    return actor


def main():
    # STL files to display
    stl_files = [
        ("legTop.stl", (10, 0, 0), (45, 1, 0, 0)),            # Example: Translate by (10, 0, 0) and rotate 45 degrees around x-axis
        ("legBottom.stl", (0, 20, 0), (30, 0, 1, 0)),      # Translate and rotate another file
        ("bodyAssembly.stl", (0, 0, 30), (60, 0, 0, 1))    # And so on for each file
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

    # Add actors for each STL file to the scene
    for file_name, translation, rotation in stl_files:
        actor = create_stl_actor(file_name, translation, rotation)
        renderer.AddActor(actor)


    # Set the background color
    renderer.SetBackground(1, 1, 1)

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()

if __name__ == "__main__":
    main()
