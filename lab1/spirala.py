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

spiral_vertices = [(0,0,0), (0,10,5), (10,10,10), (10,0,15), (0,0,20), (0,10,25), (10,10,30), (10,0,35), (0,0,40),(0,10,45),(10,10,50),(10,0,55)]

object_model = pyglet.model.load(file_name)
current_index = -1
vertex_array = np.array(vertices)
object_center = vertex_array.mean(axis = 0)

animation_speed = 0.1
is_paused = False
reverse_direction = False

camera_x, camera_y, camera_z = 1, 1, -50
zoom_level = 1

def update(dt):
    global current_index
    current_index = (current_index + 1) % len(spiral_vertices)

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
    for point in spiral_vertices:
        glVertex3f(*point)
    glEnd()


    glColor3f(0.5, 0.5, 1)
    glPushMatrix()
    glTranslatef(*spiral_vertices[current_index])
    glTranslatef(-object_center[0], -object_center[1], -object_center[2])

    object_model.draw()
    glPopMatrix()
pyglet.clock.schedule_interval(update, animation_speed)

pyglet.app.run()
