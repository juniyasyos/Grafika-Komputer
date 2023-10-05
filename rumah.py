from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
w,h= 1000,1000
def tiitk():
    glColor(0,0,100)
    glBegin(GL_POLYGON)
    glVertex2f(400.0,200.0)#A
    glVertex2f(400.0,0.0) #B
    glVertex2f(600.0,0.0)#D
    glVertex2f(600.0,200.0)#C
    glEnd()
    # glColor(0,255,255)
    glBegin(GL_TRIANGLES)
    glVertex2f(400.0,200.0)#A
    glColor(0,255,255)
    glVertex2f(600.0,200.0)#C
    glColor(100,255,255)
    glVertex2f(494.0,400.0) #E
    # glColor(10,255,255)
    glEnd()
    # glColor(0,255,0)
    glBegin(GL_POLYGON)
    glVertex2f(494.0,400.0) #E
    glVertex2f(1000.0,400.0)#F
    glVertex2f(1090.0,200.0)#G
    glVertex2f(600.0,200.0)#C
    glEnd()
    # glColor(25,25,25)
    glBegin(GL_POLYGON)
    glVertex2f(600.0,200.0)#C
    glVertex2f(1090.0,200.0)#G
    glVertex2f(1098.7,0.0)
    glVertex2f(600.0,0.0)#D
    glEnd()
def iterate():
    glViewport(100, 220, 500, 500)#ngatur sumbu x dan y objectnya terhadap layar (sumbu koordinat)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    # glColor3f(1.0, 0.0, 3.0)
    tiitk()
    glutSwapBuffers()
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w,h)
glutInitWindowPosition(10, 10)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()