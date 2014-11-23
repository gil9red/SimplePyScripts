# url = http://www.cs.smith.edu/~emendelo/classes/fall12/csc240/code/glPrint.py


# import time
# import random
# import ctypes

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *





# Number of the glut window.
window = 0
width = 0
height = 0


def glSetup(w, h):
    global width, height
    width = w
    height = h

    glClearColor(0.0, 0.0, 0.0, 0.0)  # black background
    glClearDepth(1.0)  # depth cleared to 1
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    # turn on anti aliasasing
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glSetupCam()
    glMatrixMode(GL_MODELVIEW)
    glSetupWorld()


def glResize(w, h):
    global width, height
    width = w
    height = h

    aspectRation = float(width) / float(height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glSetupCam()
    glMatrixMode(GL_MODELVIEW)


# curtime = time.time() - .1


def glSetupCam():
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)


def glSetupWorld():
    # create and initialize objects here
    pass


def glDraw():
    # global curtime
    # lasttime = curtime
    # curtime = time.time();
    # dt = curtime - lasttime
    # use dt to scale speeds expressed in seconds
    # e.g. x = speedX * dt

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # render objects here

    # print text after rendering world so it is on top 

    glut_print(10, 15, GLUT_BITMAP_9_BY_15, "Hello World", 1.0, 1.0, 1.0, 1.0)

    glutSwapBuffers()


# glut_print adapted from http://stackoverflow.com/questions/12837747/print-text-with-glut-and-python
def glut_print(x, y, font, text, r, g, b, a):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, width, height, 0.0)
    glMatrixMode(GL_MODELVIEW)
    blending = False
    if glIsEnabled(GL_BLEND):
        blending = True

    #glEnable(GL_BLEND)
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    if not blending:
        glDisable(GL_BLEND)


ESCAPE = '\033'


def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()


def main():
    global window
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(200, 200)
    # glutInitWindowSize(640, 480)
    # glutInitWindowPosition(0, 0)

    window = glutCreateWindow(b"CSC240 Stub")

    #register calbacks
    glutDisplayFunc(glDraw)
    glutIdleFunc(glDraw)
    glutReshapeFunc(glResize)
    glutKeyboardFunc(keyPressed)


    # Uncomment this line to get full screen.
    #glutFullScreen()


    #setup things up
    glSetup(640, 480)


    #start rendering
    glutMainLoop()


if (__name__ == '__main__'):
    main()