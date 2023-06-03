import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


"""
Generating a random maze

This code will generate a random maze, the main property of this maze is that
every cell is connected with each other cell. The working of the algorithm remind
a bit of the working of the algorithm of Dijkstra. But this implementation is not
perfect. For example a wall needs to be removed twice, and the efficiency of the
algorithm could've been done better. At this point it works as follows:
  * pick a random cell and put it on the queue
  * as long as the queue is not empty
    * get a cell from the queue, mark this cell as visited
    * if this cell has four walls, it means it has a neighbor which belongs to the
      path, find it and remove the wall
    * add the unvisited neighbors of this cell to the path
    * if neighbors were added, pick a random neighbor and remove the wall between
      this cell and the current cell, make sure this cell will be popped from the
      queue

A shortcoming here is that a cell which is already in the queue, but has not yet
been visited will be pushed on the queue again. So although a cell can a occur n
times in the queue, it will be processed only once.


http://www.de-brauwer.be/wiki/wikka.php?wakka=PyOpenGLMaze
"""

WIDTH = 640
HEIGHT = 640
MAZEROWS = 150
MAZECOLS = 150


class MazeCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall_north = True
        self.wall_east = True
        self.wall_south = True
        self.wall_west = True
        self.visited = False


class Maze:
    def __init__(self, dimx, dimy):
        self.numx = dimx
        self.numy = dimy

        assert dimx > 0
        assert dimy > 0

        # Create a field filled with walls
        self.cells = []
        for i in range(0, dimx * dimy):
            self.cells.append(MazeCell(i % dimx, i // dimx))

        cell_list = []
        cell = self.cells[random.randint(0, (dimx * dimy) - 1)]
        cell_list.append(cell)

        while len(cell_list) != 0:
            # Take the current cell
            cell = cell_list.pop()
            cell.visited = True

            # If a cell is not connected, see if we can connected it to the path
            if (
                cell.wall_north
                and cell.wall_east
                and cell.wall_south
                and cell.wall_north
            ):
                if (
                    cell.x > 0
                    and self.cells[(cell.x - 1) + (cell.y + 0) * dimx].visited
                ):
                    cell.wall_west = False
                    self.cells[(cell.x - 1) + (cell.y + 0) * dimx].wall_east = False
                elif (
                    cell.x < (dimx - 2)
                    and self.cells[(cell.x + 1) + (cell.y + 0) * dimx].visited
                ):
                    cell.wall_east = False
                    self.cells[(cell.x + 1) + (cell.y + 0) * dimx].wall_west = False
                elif (
                    cell.y > 0
                    and self.cells[(cell.x + 0) + (cell.y - 1) * dimx].visited
                ):
                    cell.wall_south = False
                    self.cells[(cell.x + 0) + (cell.y - 1) * dimx].wall_north = False
                elif (
                    cell.y < (dimy - 2)
                    and self.cells[(cell.x + 0) + (cell.y + 1) * dimx].visited
                ):
                    cell.wall_north = False
                    self.cells[(cell.x + 0) + (cell.y + 1) * dimx].wall_south = False

            # Append neighbors if they are not yet in the path.
            num = 0
            if (
                cell.x > 0
                and not self.cells[(cell.x - 1) + (cell.y + 0) * dimx].visited
            ):
                cell_list.append(self.cells[(cell.x - 1) + (cell.y + 0) * dimx])
                num += 1
            if (
                cell.x < (dimx - 1)
                and not self.cells[(cell.x + 1) + (cell.y + 0) * dimx].visited
            ):
                cell_list.append(self.cells[(cell.x + 1) + (cell.y + 0) * dimx])
                num += 1
            if (
                cell.y < (dimy - 1)
                and not self.cells[(cell.x + 0) + (cell.y + 1) * dimx].visited
            ):
                cell_list.append(self.cells[(cell.x + 0) + (cell.y + 1) * dimx])
                num += 1
            if (
                cell.y > 0
                and not self.cells[(cell.x + 0) + (cell.y - 1) * dimx].visited
            ):
                cell_list.append(self.cells[(cell.x + 0) + (cell.y - 1) * dimx])
                num += 1

            # We added num items to the queue, we should make a connection with one of those
            if num > 0:
                # Get one of the last num elements
                conn = cell_list.pop(-random.randint(1, num))
                conn.visited = True

                # Remove the wall
                if cell.x == conn.x:
                    if cell.y == conn.y + 1:
                        cell.wall_south = False
                        conn.wall_north = False
                    else:
                        cell.wall_north = False
                        conn.wall_south = False

                elif cell.y == conn.y:
                    if cell.x == conn.x + 1:
                        cell.wall_west = False
                        conn.wall_east = False
                    else:
                        cell.wall_east = False
                        conn.wall_west = False

                # Push it back on the list since this is our next node
                cell_list.append(conn)

    def draw(self):
        """Draws the field"""
        glBegin(GL_LINES)
        for i in range(0, self.numx * self.numy):
            x = i % self.numx
            y = i / self.numx

            if self.cells[i].wall_north:
                glVertex2f(x * WIDTH / self.numx, (y + 1) * HEIGHT / self.numy)
                glVertex2f((x + 1) * WIDTH / self.numx, (y + 1) * HEIGHT / self.numy)

            if self.cells[i].wall_east:
                glVertex2f((x + 1) * WIDTH / self.numx, (y + 1) * HEIGHT / self.numy)
                glVertex2f((x + 1) * WIDTH / self.numx, y * HEIGHT / self.numy)

            if self.cells[i].wall_south:
                glVertex2f(x * WIDTH / self.numx, y * HEIGHT / self.numy)
                glVertex2f((x + 1) * WIDTH / self.numx, y * HEIGHT / self.numy)

            if self.cells[i].wall_west:
                glVertex2f(x * WIDTH / self.numx, (y + 1) * HEIGHT / self.numy)
                glVertex2f(x * WIDTH / self.numx, y * HEIGHT / self.numy)

        glEnd()


maze = Maze(MAZECOLS, MAZEROWS)


def init_fun():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Start project to -1.0 otherwise the lines are not visible
    gluOrtho2D(-1.0, WIDTH, -1.0, HEIGHT)


def display_fun():
    glClear(GL_COLOR_BUFFER_BIT)
    maze.draw()
    glFlush()


if __name__ == "__main__":
    glutInit()
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Maze")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(display_fun)
    init_fun()
    glutMainLoop()
