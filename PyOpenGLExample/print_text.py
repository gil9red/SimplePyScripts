# url: http://www.cs.smith.edu/~emendelo/classes/fall12/csc240/code/glPrint.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


width = 0
height = 0


def glSetup(w, h) -> None:
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


def glResize(w, h) -> None:
    global width, height
    width = w
    height = h

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glSetupCam()
    glMatrixMode(GL_MODELVIEW)


def glSetupCam() -> None:
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)


def glDraw() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # render objects here

    # print text after rendering world so it is on top

    glut_print(10, 15, GLUT_BITMAP_9_BY_15, "Hello World", 1.0, 1.0, 1.0, 1.0)

    glutSwapBuffers()


# glut_print adapted from http://stackoverflow.com/questions/12837747/print-text-with-glut-and-python
def glut_print(x, y, font, text, r, g, b, a) -> None:
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, width, height, 0.0)
    glMatrixMode(GL_MODELVIEW)
    blending = False
    if glIsEnabled(GL_BLEND):
        blending = True

    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    if not blending:
        glDisable(GL_BLEND)


def keyPressed(*args) -> None:
    ESCAPE = b"\x1b"
    if args[0] == ESCAPE:
        sys.exit()


if __name__ == "__main__":
    glutInit()

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(200, 200)

    glutCreateWindow(b"CSC240 Stub")

    # register calbacks
    glutDisplayFunc(glDraw)
    glutIdleFunc(glDraw)
    glutReshapeFunc(glResize)
    glutKeyboardFunc(keyPressed)

    # setup things up
    glSetup(640, 480)

    # start rendering
    glutMainLoop()
