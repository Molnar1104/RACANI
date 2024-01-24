import pyglet
from pyglet.gl import *
from pyglet.gl.glu import *
from pywavefront import Wavefront
import math
from math import ceil
from math import floor
import time
import numpy as np

window = pyglet.window.Window(width=960, height=640, resizable = True, caption = "Test 3D objekt")
window.projection = pyglet.window.Projection3D()
batch = pyglet.graphics.Batch()

file_name = "kocka.obj"

aproksimacija = Wavefront(file_name, collect_faces=True)
vertices = aproksimacija.vertices
faces = aproksimacija.mesh_list[0].faces

segments = []
spline = []
tangent_start_points = []
tangent_target_points = []
tangents_start = []
tangents_end = []

for i in range(len(vertices) - 3):
    vektoriSegmenta = []
    knotPoint0 = vertices[i]
    knotPoint1 = vertices[i + 1]
    knotPoint2 = vertices[i + 2]
    knotPoint3 = vertices[i + 3]

    vektoriSegmenta.append(knotPoint0)
    vektoriSegmenta.append(knotPoint1)
    vektoriSegmenta.append(knotPoint2)
    vektoriSegmenta.append(knotPoint3)
    segments.append(vektoriSegmenta)
    # print(knotPoint0[0])
    for j in range(100):
        temp = []
        t = j / 100
        fja1 = (-t**3 + 3*t**2 - 3*t + 1) / 6.0
        fja2 = (3*t**3 - 6*t**2 + 4) /6.0
        fja3 = (-3*t**3 + 3*t**2 + 3*t + 1) / 6.0
        fja4 = t**3 / 6.0
        x_temp = fja1*knotPoint0[0] + fja2*knotPoint1[0] + fja3*knotPoint2[0] + fja4*knotPoint3[0]
        y_temp = fja1*knotPoint0[1] + fja2*knotPoint1[1] + fja3*knotPoint2[1] + fja4*knotPoint3[1]
        z_temp = fja1*knotPoint0[2] + fja2*knotPoint1[2] + fja3*knotPoint2[2] + fja4*knotPoint3[2]
        temp.append(x_temp)
        temp.append(y_temp)
        temp.append(z_temp)

        spline.append(temp)
        tangent_start_points.append(temp)

        fjaDer1 = 0.5 * (-t**2 + 2*t - 1)
        fjaDer2 = 0.5 * (3*t**2 -4*t)
        fjaDer3 = 0.5 * (-3 * t**2 + 2*t + 1)
        fjaDer4 = 0.5 * (t**2)
        temp2 = []
        x_tan = fjaDer1 *knotPoint0[0] + fjaDer2*knotPoint1[0] + fjaDer3*knotPoint2[0] + fjaDer4*knotPoint3[0]
        y_tan = fjaDer1 *knotPoint0[1] + fjaDer2*knotPoint1[1] + fjaDer3*knotPoint2[1] + fjaDer4*knotPoint3[1]
        z_tan = fjaDer1 *knotPoint0[2] + fjaDer2*knotPoint1[2] + fjaDer3*knotPoint2[2] + fjaDer4*knotPoint3[2]
        temp2.append(x_temp + x_tan/3)
        temp2.append(y_temp + y_tan/3)
        temp2.append(z_temp + z_tan/3)
        tangent_target_points.append(temp2)

        if(j % 25 == 0):
            tangents_start.append(temp)
            tangents_end.append(temp2)


eovi = []
for i in range(len(tangent_target_points)):
    
    e = []
    e.append(tangent_target_points[i][0] - tangent_start_points[i][0])
    e.append(tangent_target_points[i][1] - tangent_start_points[i][1])
    e.append(tangent_target_points[i][2] - tangent_start_points[i][2])
    eovi.append(e)

ref_orientation = [0.0, 0.0, 1.0]
pi = 3.14159
def calculate_rotation(eVariable):
    ax = []
    ax.append(ref_orientation[1] * eVariable[2] - eVariable[1] * ref_orientation[2])
    ax.append(eVariable[0] * ref_orientation[2] - ref_orientation[0] * eVariable[2])
    ax.append(ref_orientation[0] * eVariable[1] - ref_orientation[1] * eVariable[0])

    apsS = (ref_orientation[0]**2 + ref_orientation[1]**2 + ref_orientation[2]**2)**0.5
    apsE = (eVariable[0]**2 + eVariable[1]**2 + eVariable[2]**2)**0.5
    se = ref_orientation[0]*eVariable[0] + ref_orientation[1]*eVariable[1] + ref_orientation[2]*eVariable[2]
    angle = math.acos(se / (apsS * apsE))
    angle = (angle*180) / pi
    return (angle, ax[0], ax[1], ax[2])


object_model = pyglet.model.load(file_name)
current_index = -1
vertex_array = np.array(vertices)
object_center = vertex_array.mean(axis = 0)

animation_speed = 0.01
is_paused = False
reverse_direction = False

camera_x, camera_y, camera_z = 0, 0, -4
zoom_level = 1

def update(dt):
    global current_index
    if not is_paused:
        current_index += 1 if not reverse_direction else -1
        current_index %= len(spline)
@window.event
def on_key_press(symbol, modifiers):
    global animation_speed, is_paused, reverse_direction

    if symbol == pyglet.window.key.W:
        animation_speed += 0.01 
    elif symbol == pyglet.window.key.S:
        animation_speed -= 0.01 
    elif symbol == pyglet.window.key.SPACE:
        is_paused = not is_paused  
    elif symbol == pyglet.window.key.R:
        reverse_direction = not reverse_direction 

def draw_axes():
    glBegin(GL_LINES)
    # X os
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(20, 0, 0)

    # Y os
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 20, 0)

    # Z os
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 20)
    glEnd()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global camera_x, camera_y
    if buttons & pyglet.window.mouse.LEFT:
        camera_x += dx * 0.01
        camera_y -= dy * 0.01

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global zoom_level
    zoom_level -= scroll_y * 0.1
    zoom_level = max(0.1, min(zoom_level, 10))


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glTranslatef(camera_x, camera_y, camera_z * zoom_level)
    # draw_axes()


    glColor3f(1, 0, 0) 
    glBegin(GL_LINE_STRIP)
    for point in spline:
        glVertex3f(*point)
    glEnd()

    glColor3f(0, 1, 0) 
    for start, end in zip(tangents_start, tangents_end):
        glBegin(GL_LINES)
        glVertex3f(*start)
        glVertex3f(*end)
        glEnd()

    glColor3f(0.5, 0.5, 1)
    glPushMatrix()
    glTranslatef(*spline[current_index])
    angle, x, y, z = calculate_rotation(eovi[current_index])
    glRotatef(angle, x, y, z)
    glTranslatef(-object_center[0], -object_center[1], -object_center[2])

    object_model.draw()
    glPopMatrix()
pyglet.clock.schedule_interval(update, animation_speed)

pyglet.app.run()
