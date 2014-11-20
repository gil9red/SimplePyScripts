from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math 

N=25
RADIUS=95


def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-100,100,-100,100)

def reshapeFun(w,h):
    if w > h:
        glViewport((w-h)/2,0,h,h)
    else:
        glViewport(0,(h-w)/2,w,w)

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,0.0,1.0)
    xpts=[]
    ypts=[]
    for i in range(0,N):
        xpts.append(RADIUS*math.sin(2.0*math.pi*i/N))
        ypts.append(RADIUS*math.cos(2.0*math.pi*i/N))
    
    glBegin(GL_LINE_STRIP)
    for i in range(0,N):
        for j in range(i,N):
            glVertex2f(xpts[i],ypts[i])
            glVertex2f(xpts[j],ypts[j])
    glEnd()
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(400,400)
    glutCreateWindow(b"Rosette")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(reshapeFun)
    initFun()
    glutMainLoop()