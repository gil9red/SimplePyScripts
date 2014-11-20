from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

WIDTH=640
HEIGHT=640
MAZEROWS=150
MAZECOLS=150

class MazeCell:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.wallNorth=True
        self.wallEast =True
        self.wallSouth=True
        self.wallWest =True
        self.visited  =False

class Maze:
    def __init__(self,dimx,dimy):
        self.numx=dimx
        self.numy=dimy

        assert dimx>0
        assert dimy>0

        # Create a field filled with walls
        self.cells=[]
        for i in range(0,dimx*dimy):
            self.cells.append(MazeCell(i%dimx,i/dimx))


        cellList=[]
        cell = self.cells[random.randint(0,(dimx*dimy)-1)]
        cellList.append(cell)

        while len(cellList) != 0:
            # Take the current cell
            cell = cellList.pop()
            cell.visited=True

            # If a cell is not connected, see if we can connected it to the path
            if cell.wallNorth and cell.wallEast and cell.wallSouth and cell.wallNorth:
                if   cell.x > 0        and self.cells[(cell.x-1)+(cell.y+0)*dimx].visited:
                    cell.wallWest=False
                    self.cells[(cell.x-1)+(cell.y+0)*dimx].wallEast=False
                elif cell.x < (dimx-2) and self.cells[(cell.x+1)+(cell.y+0)*dimx].visited:
                    cell.wallEast=False
                    self.cells[(cell.x+1)+(cell.y+0)*dimx].wallWest=False
                elif cell.y > 0 and self.cells[(cell.x+0)+(cell.y-1)*dimx].visited:
                    cell.wallSouth=False
                    self.cells[(cell.x+0)+(cell.y-1)*dimx].wallNorth=False
                elif cell.y < (dimy-2) and self.cells[(cell.x+0)+(cell.y+1)*dimx].visited:
                    cell.wallNorth=False
                    self.cells[(cell.x+0)+(cell.y+1)*dimx].wallSouth=False


            # Append neighbors if they are not yet in the path.
            num=0
            if cell.x>0        and not self.cells[(cell.x-1)+(cell.y+0)*dimx].visited:
                cellList.append(self.cells[(cell.x-1)+(cell.y+0)*dimx])
                num+=1
            if cell.x<(dimx-1) and not self.cells[(cell.x+1)+(cell.y+0)*dimx].visited:
                cellList.append(self.cells[(cell.x+1)+(cell.y+0)*dimx])
                num+=1
            if cell.y<(dimy-1) and not self.cells[(cell.x+0)+(cell.y+1)*dimx].visited:
                cellList.append(self.cells[(cell.x+0)+(cell.y+1)*dimx])
                num+=1
            if cell.y>0        and not self.cells[(cell.x+0)+(cell.y-1)*dimx].visited:
                cellList.append(self.cells[(cell.x+0)+(cell.y-1)*dimx])
                num+=1

            # We added num items to the queue, we should make a connection with one of those
            if num > 0:
                # Get one of the last num elements
                conn=cellList.pop(-random.randint(1,num))
                conn.visited=True

                # Remove the wall
                if cell.x==conn.x:
                    if cell.y==conn.y+1:
                        cell.wallSouth=False
                        conn.wallNorth=False
                    else:
                        cell.wallNorth=False
                        conn.wallSouth=False
                elif cell.y==conn.y:
                    if cell.x==conn.x+1:
                        cell.wallWest=False
                        conn.wallEast=False
                    else:
                        cell.wallEast=False
                        conn.wallWest=False

                # Push it back on the list since this is our next node 
                cellList.append(conn)

    def draw(self):
        """ Draws the field """
        glBegin(GL_LINES)
        for i in range(0,self.numx*self.numy):
            x=i%self.numx
            y=i/self.numx
            if self.cells[i].wallNorth:
                glVertex2f(   x *WIDTH/self.numx,(y+1)*HEIGHT/self.numy)
                glVertex2f((x+1)*WIDTH/self.numx,(y+1)*HEIGHT/self.numy)
            if self.cells[i].wallEast:
                glVertex2f((x+1)*WIDTH/self.numx,(y+1)*HEIGHT/self.numy)
                glVertex2f((x+1)*WIDTH/self.numx,   y *HEIGHT/self.numy)
            if self.cells[i].wallSouth:
                glVertex2f(    x*WIDTH/self.numx,   y *HEIGHT/self.numy)
                glVertex2f((x+1)*WIDTH/self.numx,   y *HEIGHT/self.numy)
            if self.cells[i].wallWest:
                glVertex2f(   x *WIDTH/self.numx,(y+1)*HEIGHT/self.numy)
                glVertex2f(   x *WIDTH/self.numx,    y*HEIGHT/self.numy)
        glEnd()

maze=Maze(MAZECOLS,MAZEROWS)


def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Start project to -1.0 otherwise the lines are not visible
    gluOrtho2D(-1.0,WIDTH,-1.0,HEIGHT)


def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    maze.draw()
    glFlush()

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(WIDTH,HEIGHT)
    glutCreateWindow("Maze")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()