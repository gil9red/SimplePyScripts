from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

points=[]

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)
    

def displayFun():
    global points
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_LINE_STRIP)
    glColor3f(0,0,0)
    for p in points:
        glVertex2i(p.x,p.y)
    glEnd()
    glFlush()

def mouseFun(button,state,x,y):
    global points
    if button==GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        p = Point(x,480-y)
        points.append(p)
    if button==GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if len(points) != 0:
            points=points[:-1]
    glutPostRedisplay()
        
if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(640,480)
    glutCreateWindow(b"Polyline")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutMouseFunc(mouseFun)
    initFun()
    glutMainLoop()