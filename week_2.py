from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_LINES) #memulai garis
    glColor3ub(255,0,255)
    glVertex2f (0.1, 0.0)
    glColor3ub(0,255,255)
    glVertex2f (-0.1, 0.0)
    glColor3ub(255,0,255)
    glVertex2f (0.0, 0.1)
    glColor3ub(0,255,255)
    glVertex2f (0.0, -0.1)
    glEnd()
    glFlush()
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(400,400)
glutInitWindowPosition(100,100)
glutCreateWindow("Informatika")
glutDisplayFunc(display)
glClearColor(1.0,1.0,1.0,1.0)
glutMainLoop()