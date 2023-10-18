
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
w,h= 500,500
# def square():
#     glBegin(GL_TRIANGLES)
#     glVertex2f(100, 100)
#     glVertex2f(200, 100)
#     glVertex2f(200, 200)
#     glVertex2f(100, 200)
#     glVertex2f(300, 400)
#     glVertex2f(400, 400)
#     # glVertex2f(400, 300)
#     # glVertex2f(300, 300)
#     glEnd()
# def line(): 
#     glScalef(10.0,3.0,3.0)
#     glBegin(GL_LINE_STRIP)
#     glVertex2f(22.0,80.0)
#     glVertex2f(22.0,60.0)
#     glVertex2f(40.0,80.0)
#     glVertex2f(40.0,60.0)
#     glEnd()
# def polygon():
#     glScale(5,5,5)
#     glBegin(GL_POLYGON) #bedasarkan titik nya,quads 
#     glVertex2f(3.54,9.58)#c
#     glVertex2f(5.0,11.0)#a
#     glVertex2f(11.0,11.0)#b
#     glVertex2f(12.0,9.0)#f
#     glVertex2f(11.0,8.0)#e
#     glVertex2f(5.0,8.0)#d
#     glEnd()
# def point () : 
#     glColor(0,0,10)
#     glPointSize(3)
#     glBegin(GL_POINTS)
#     glVertex2f(20.2,40.0)
#     glEnd()
# def segitiga (): 
#     glColor(100,200,100)
#     glBegin(GL_TRIANGLE_STRIP)
#     glVertex2f(15.0,40.0)
#     glVertex2f(25.0,45.00)
#     glVertex2f(23.0,30.0)
#     glEnd()
# def bangun () : 
#     # glScale(5,5,3)
#     glBegin(GL_POLYGON)
#     glVertex2f(5.36,6.34) #A
#     glVertex2f(10.22,6.32) #B
#     glVertex2f(10.62,3.98) #c
#     glVertex2f(6.0,4.0)
#     glEnd()
#praktik buat plak
# def bangun2():
#     glScale(2,2,2)
#     glBegin(GL_POLYGON)
#     glVertex2f(7.0,7.0) #A
#     glVertex2f(6.0,6.0) #B
#     glVertex2f(6.0,4.0) #D
#     glVertex2f(8.0,4.0)#E 
#     glVertex2f(8.0,6.0)
#     glEnd()
# def titik(): 
#     glPointSize(15)
#     glColor3f(40.0,255.0,255.0)
#     glBegin(GL_POINTS)
#     # glVertex2f(40.0,50.0)
#     # glVertex2f(50.0,50.0)
#     # glVertex2f(50.0,60.0)
#     # glVertex2f(-70.0,-110.0)
#     glVertex2f(70.0,110.0)
#     # glVertex2f(700.0,700.0)
#     glEnd()
# def line (): 
#     # glLineWidth(5)
#     glBegin(GL_LINES)
#     glVertex2f(40.0,50.0)
#     glVertex2f(100.0,120.0)
#     glVertex2f(150.0,180.0)
#     glVertex2f(400.0,400.0)
#     glEnd()
def persegi(): 
    glBegin(GL_QUAD_STRIP)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()
def iterate():
    glViewport(0,0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500.0, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 3.0)
    persegi()
    # square()
    # line()
    # point()
    # bangun()
    # bangun2()
    # segitiga()
    # polygon()
    # titik()
    # line()
    glutSwapBuffers()
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)    
glutMainLoop()