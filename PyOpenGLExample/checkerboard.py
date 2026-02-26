from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Generating a checkerboard

This code generates a checkerboard.
"""


def initFun() -> None:
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 640.0, 0.0, 480.0)


def displayFun() -> None:
    CELL_SIZE = 40

    glClear(GL_COLOR_BUFFER_BIT)

    for i in range(0, 8):
        x1 = i * CELL_SIZE
        x2 = x1 + CELL_SIZE

        for j in range(0, 8):
            y1 = j * CELL_SIZE
            y2 = y1 + CELL_SIZE

            if (i % 2 and not j % 2) or (not i % 2 and j % 2):
                glColor3f(0xFF, 0xFF, 0xFF)  # white
            else:
                glColor3f(0x0, 0x0, 0x0)  # black

            glRecti(x1, y1, x2, y2)

    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(640, 480)
    glutCreateWindow(b"DrawSquares")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()
