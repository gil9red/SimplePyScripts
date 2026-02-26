from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

"""
Wireframe scene

This sample code renders a scene composed out of wireframe objects.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLWireframe
"""


def axis(length) -> None:
    """Draws an axis (basicly a line with a cone on top)"""
    glPushMatrix()
    glBegin(GL_LINES)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, length)
    glEnd()
    glTranslated(0, 0, length)
    glutWireCone(0.04, 0.2, 12, 9)
    glPopMatrix()


def three_axis(length) -> None:
    """Draws an X, Y and Z-axis"""

    glPushMatrix()
    # Z-axis
    glColor3f(1.0, 0.0, 0.0)
    axis(length)
    # X-axis
    glRotated(90, 0, 1.0, 0)
    glColor3f(0.0, 1.0, 0.0)
    axis(length)
    # Y-axis
    glRotated(-90, 1.0, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    axis(length)
    glPopMatrix()


def display_fun() -> None:
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2.0 * 64 / 48.0, 2.0 * 64 / 48.0, -1.5, 1.5, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glClear(GL_COLOR_BUFFER_BIT)
    three_axis(0.5)

    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslated(0.5, 0.5, 0.5)
    glutWireCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.0, 1.0, 0)
    glutWireSphere(0.25, 10, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.0, 1.0, 0)
    glutWireSphere(0.25, 10, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.0, 0, 1.0)
    glutWireCone(0.2, 0.5, 10, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1.0, 1.0, 1.0)
    glutWireTeapot(0.2)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0, 1, 0)
    glRotated(90, 1, 0, 0)
    glutWireTorus(0.1, 0.3, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslated(1, 0, 0)
    glScaled(0.15, 0.15, 0.15)
    glutWireDodecahedron()
    glPopMatrix()

    glPushMatrix()
    glTranslated(0, 1, 1)
    glutWireCube(0.25)
    glPopMatrix()

    glPushMatrix()
    glTranslated(0, 0, 1)
    qobj = gluNewQuadric()
    gluQuadricDrawStyle(qobj, GLU_LINE)
    gluCylinder(qobj, 0.2, 0.2, 0.4, 8, 8)
    glPopMatrix()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"3D")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glutDisplayFunc(display_fun)
    glutMainLoop()
