from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
    glutWireTeapot(40)
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(-99,-99)
    glVertex2f(-99, 99)
    glVertex2f( 99, 99)
    glVertex2f( 99,-99)
    glVertex2f(-99,-99)
    glEnd()
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow(b"Viewport")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(reshapeFun)
    initFun()
    glutMainLoop()