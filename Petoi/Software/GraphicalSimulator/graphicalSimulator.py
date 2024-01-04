# Petoi 3D animation.
#
# Adrian Bowyer & GPT4
# 3 January 2024
#
# RepRap Ltd
# https://reprapltd.com
#
# Licence: GPL
# See: https://www.reddit.com/r/pygame/comments/ybnftb/render_stl_files_using_numpy_in_pygame_i_post/
#

from stl import mesh
import pygame
import numpy

def rotation_matrix(dx, dy):
    Rx = numpy.array([[1, 0, 0, 0],
                   [0, numpy.cos(dy), -numpy.sin(dy), 0],
                   [0, numpy.sin(dy), numpy.cos(dy), 0],
                   [0, 0, 0, 1]])

    Ry = numpy.array([[numpy.cos(dx), 0, numpy.sin(dx), 0],
                   [0, 1, 0, 0],
                   [-numpy.sin(dx), 0, numpy.cos(dx), 0],
                   [0, 0, 0, 1]])

    return numpy.dot(Rx, Ry)


def project3d_to_2d( vertex ):

    scale = 25
    vertex = vertex * scale

    x, y, z = vertex

    r = pygame.math.Vector2(
        x - y + 350,
        x + y - z + 350
    )

    return r


def is_clockwise(points):
    v = 0
    for a, b in zip( points, points[1:] + [points[0]] ):
        v += ( b[0] - a[0] ) * ( b[1] + a[1] )
    return v > 0


def surface_normal( surface ):

    surface = numpy.array( surface )
    n = numpy.array( ( 0.0,) * 3 )

    for i, a in enumerate( surface ):
        b = surface [ ( i + 1 ) % len( surface ), : ]
        n[0] += ( a[1] - b[1] ) * ( a[2] + b[2] )
        n[1] += ( a[2] - b[2] ) * ( a[0] + b[0] )
        n[2] += ( a[0] - b[0] ) * ( a[1] + b[1] )

    norm = numpy.linalg.norm(n)
    if norm==0: raise ValueError('zero norm')
    return n / norm


def lerp_color( factor, color_a, color_b ):
    color_a = numpy.array(color_a)
    color_b = numpy.array(color_b)
    vector = color_b - color_a
    r = color_a + vector * factor
    return r


def sort(face):
    vertex1 = ( face[0], face[1], face[2] )
    vertex2 = ( face[3], face[4], face[5] )
    vertex3 = ( face[6], face[7], face[8] )

    m = (
        ( vertex1[0] + vertex2[0] + vertex3[0] / 3 ),
        ( vertex1[1] + vertex2[1] + vertex3[1] / 3 ),
        ( vertex1[2] + vertex2[2] + vertex3[2] / 3 ),
    )

    return m[0] + m[1] + m[2]*2


def rotate( mesh, rot, axis ):

    for face in mesh:

        vertex1 = pygame.math.Vector3( (face[0], face[1], face[2]) )
        vertex2 = pygame.math.Vector3( (face[3], face[4], face[5]) )
        vertex3 = pygame.math.Vector3( (face[6], face[7], face[8]) )

        vertex1 = getattr( vertex1, 'rotate_{0}_rad'.format( axis ) )( rot )
        vertex2 = getattr( vertex2, 'rotate_{0}_rad'.format( axis ) )( rot )
        vertex3 = getattr( vertex3, 'rotate_{0}_rad'.format( axis ) )( rot )

        yield ( vertex1[0], vertex1[1], vertex1[2],
                vertex2[0], vertex2[1], vertex2[2],
                vertex3[0], vertex3[1], vertex3[2], )


def render( faces, z_rot, colors, ray ):

    screen.fill( 0x112233 )

    for face in sorted( rotate( faces, z_rot, 'z' ), key = sort ):

        vertex1 = ( face[0], face[1], face[2] )
        vertex2 = ( face[3], face[4], face[5] )
        vertex3 = ( face[6], face[7], face[8] )

        polygon = [
            project3d_to_2d( pygame.math.Vector3( vertex ) )
            for vertex in [ vertex1, vertex2, vertex3 ]
        ]

        if is_clockwise( polygon ): continue

        n = surface_normal( [ vertex1, vertex2, vertex3 ] )

        pygame.draw.polygon(
            surface = screen,
            color = lerp_color( ( n.dot( ray ) + 1 ) / 2, *colors ),
            points = polygon,
        )

    _quit = False
    while not _quit:
        for event in  pygame.event.get():

            if event.type == pygame.QUIT:
                _quit = True

            elif event.type == pygame.KEYDOWN:
                # press any key to quit
                _quit = True


        clock.tick( FPS )
        pygame.display.update()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( ( 700, 700 ) )
    clock = pygame.time.Clock()

    FPS = 60

    # test change this value to rotate the teapot ( it is in radians )
    z_rot = -1.1

    # test change these color to modify colors on teapot.
    # (one of the color is the shadow color)
    color_a = ( 0,   0,  0 )
    color_b = ( 200, 100, 0 )

    # the shadow is based on this vector. test change it.
    ray = pygame.math.Vector3( 0, -0.4, 0 ).normalize()

    # you can download the teapot stl file at: https://en.wikipedia.org/wiki/STL_(file_format)
    # remember to rename to to teapot.stl
    faces = mesh.Mesh.from_file( 'ab.stl' )
    # of course you can find other stl files to test but you might have to scale and
    # offset the projection to get a good view of it. see project3d_to_2d.
    last_pos = None
    rotation = numpy.identity(4)

# Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Check if left button is held
                    if last_pos:
                        dx, dy = event.rel
                        dx = numpy.radians(dx * 0.1)
                        dy = numpy.radians(dy * 0.1)
                        rotation = numpy.dot(rotation_matrix(dx, dy), rotation)
                    last_pos = event.pos
                else:
                    last_pos = None

    # Apply rotation to the model
    faces_array = numpy.array(faces.vectors)
    rotated_faces = numpy.dot(faces_array.reshape(-1, 3), rotation[:3, :3].T).reshape(-1, 3, 3)


    render( faces, z_rot = z_rot, colors = ( color_a, color_b ), ray = ray )

    # NOTE: you can also write your own projection.
    #       implement it in project3d_to_2d (you might have to modify sort method after that)

    pygame.quit()
