from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
w,h= 1000,1000
def tiitk():
    glColor3f(0.0, 255, 255)
    glPointSize(19)
    glBegin(GL_POINTS)
    glVertex2f(200.0,0.0) #A
    glVertex2f(200.0,400.0) #B
    glVertex2f(600.0,400.0) #C
    glVertex2f(600.0,0.0) #D
    glVertex2f(400.0,563.0) #E
    glVertex2f(796.0,561.0)#F
    glVertex2f(800.0,200) #G
    glVertex2f(400.0,200.0) #H
    glEnd()
def line ():
    glColor3f(0, 255, 0)
    glBegin(GL_LINES)
    glVertex2f(200.0,0.0) #Titik A & B 
    glVertex2f(200.0,400.0)

    glVertex2f(200.0,400.0) #B & C
    glVertex2f(600.0,400.0)

    glVertex2f(600.0,400.0) #C & D
    glVertex2f(600.0,0.0)
    
    glVertex2f(600.0,0.0) #D &A
    glVertex2f(200.0,0.0)

    glVertex2f(200.0,0.0) #A & H
    glVertex2f(400.0,200.0) 

    #H & G
    glVertex2f(400.0,200.0)
    glVertex2f(800.0,200)
    #G & D
    glVertex2f(800.0,200)
    glVertex2f(600.0,0.0)
   
    #H & E
    glVertex2f(400.0,200.0)
    glVertex2f(400.0,563.0)

    #E & F
    glVertex2f(400.0,563.0)
    glVertex2f(796.0,561.0)
    
    # F & G
    glVertex2f(796.0,561.0)
    glVertex2f(800.0,200)

    glVertex2f(400.0,563.0) #E
    glVertex2f(200.0,400.0) #B
    glVertex2f(796.0,561.0)#F
    glVertex2f(600.0,400.0) #C
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
    line()
    glutSwapBuffers()
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w,h)
glutInitWindowPosition(10, 10)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()