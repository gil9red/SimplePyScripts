from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    x=[0.0,640.0,320.0]
    y=[0.0,0.0  ,480.0]

    curx=0
    cury=320
    glVertex2f(curx,cury)
    for i in range(0,500000):
        idx=random.randint(0,2)
        curx=(curx+x[idx])/2.0
        cury=(cury+y[idx])/2.0
        glVertex2f(curx,cury)
    glEnd()
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow(b"Sierpinski")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()