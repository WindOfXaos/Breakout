from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import pygame
import os, inspect

from sys import platform as _platform
if _platform == "win32":
    scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
    scriptDIR  = os.path.dirname(scriptPATH)


mouse_x = 0
viewport = (600,700)
time_interval = 1
lose = False
start = False
bat_s = 0
wall_s = 0
brick_s = 0

def init():
    global bat_s, wall_s, brick_s
    glClearColor (0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, (viewport[0]), 0, (viewport[1]), -2 , 2)
    glMatrixMode (GL_MODELVIEW)
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 1, 512)
    bat_s = pygame.mixer.Sound(os.path.join(scriptDIR,"sfx\\bat.wav"))
    brick_s = pygame.mixer.Sound(os.path.join(scriptDIR,"sfx\\brick.wav"))
    wall_s = pygame.mixer.Sound(os.path.join(scriptDIR,"sfx\\wall.wav"))

def bricklvls(x = 0, y = 0, r = 1, g = 1, b = 1):
        space = 30
        blist = []
        for i in range(0, 13):
            for j in range(0, 50):
                if ((j+1) % 5 == 0):
                    space = 60
                else:
                    space = 30
                bc = Brick(x + (35 + i * 44), y + (450 + j * space), r, g, b)
                blist.append(bc)
        return blist

class player:
    def __init__(self, left, bottom, right , top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def update(self):
            self.left = mouse_x-30 
            self.right = mouse_x+30
            glLoadIdentity()
            glColor(0, 0, 1)
            glBegin(GL_QUADS) 
            glVertex(self.left,self.bottom,0)
            glVertex(self.right,self.bottom,0) 
            glVertex(self.right,self.top,0) 
            glVertex(self.left,self.top,0) 
            glEnd()

class Brick:
    def __init__(self, x, y, r, g, b):
        self.width = 20
        self.height = 9
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    def update(self):
        glLoadIdentity()
        self.colorsections()
        glColor(self.r, self.g, self.b)
        glBegin(GL_QUADS) 
        glVertex(self.x-self.width,self.y-self.height,0)
        glVertex(self.x+self.width,self.y-self.height,0) 
        glVertex(self.x+self.width,self.y+self.height,0) 
        glVertex(self.x-self.width,self.y+self.height,0)
        glEnd()

    def hit(self):
        if (g.bl.y-g.bl.radius <= self.y + self.height and g.bl.y-g.bl.radius >= self.y - self.height) or (g.bl.y+g.bl.radius >= self.y - self.height and g.bl.y+g.bl.radius <= self.y + self.height):
            if (g.bl.x-g.bl.radius <= self.x + self.width):
                if (g.bl.x+g.bl.radius >= self.x - self.width):
                    return True

    def shift(self):
        self.y = self.y - 20
    
    def colorsections(self):
        l1,l2,l3,l4,l5,l6=700, 600, 500, 400, 300, 60
        if self.y <= l1 and self.y >= l2:
            self.r = 0
            self.g = 0
            self.b = 1
        elif self.y < l2 and self.y >= l3: 
            self.r = 1
            self.g = (128/255)
            self.b = 0
        elif self.y < l3 and self.y >= l4: 
            self.r = 0
            self.g = 1
            self.b = 0
        elif self.y < l4 and self.y >= l5: 
            self.r = 1
            self.g = 1
            self.b = 0
        elif self.y < l5 and self.y >= l6: 
            self.r = 1
            self.g = 1
            self.b = 1
        elif self.y < l6:
            self.x=1500

class ball:
    def __init__(self, x, y):
        self.dir_x = 10
        self.dir_y = 10  
        self.x = random.randrange(1,viewport[0]-50)
        self.y = y
        self.radius = 3.5
        self.speed = 0.8
        self.r = 0
        self.g = 0
        self.b = 0
        self.PC_score = 0

    def update(self):
        self.colorsections()
        glColor(self.r,self.g,self.b)
        self.x = self.x + self.dir_x*self.speed
        self.y = self.y + self.dir_y*self.speed
        glLoadIdentity()
        glTranslate(self.x,self.y,-1)
        gluDisk(gluNewQuadric(),0, self.radius, 50, 50)
        self.walls()
        self.playercol()

    def walls(self):
        if self.x+self.radius > (viewport[0]-10) or self.x-self.radius < 10:
            self.dir_x = -self.dir_x
            wall_s.play()
        if self.y+self.radius > (viewport[1]-10) or self.y-self.radius < (g.p.top-35):
            self.dir_y = -self.dir_y
            self.PC_score += 1
            wall_s.play()

    def playercol(self):
        if (self.y-self.radius <= g.p.top) and (self.x-self.radius <= g.p.right) and (self.x+self.radius >= g.p.left):
            self.dir_y = abs(self.dir_y)
            bat_s.play()
    
    def lose(self):
        if (self.y - self.radius <= 0):
            return True

    def colorsections(self):
        l1,l2,l3,l4,l5=700, 600, 500, 400, 300
        if self.y <= l1 and self.y >= l2:
            self.r = 0
            self.g = 0
            self.b = 1
        elif self.y < l2 and self.y >= l3: 
            self.r = 1
            self.g = (128/255)
            self.b = 0
        elif self.y < l3 and self.y >= l4: 
            self.r = 0
            self.g = 1
            self.b = 0
        elif self.y < l4 and self.y >= l5: 
            self.r = 1
            self.g = 1
            self.b = 0
        elif self.y < l5: 
            self.r = 1
            self.g = 1
            self.b = 1

    def bounce(self):
        self.dir_y = -self.dir_y
        brick_s.play()

class borders:
    def __init__(self):
        wid = 10
        self.line_1 = [0,0, 0,30, wid,30, wid,0, 1,1,1]
        self.line_1_dash = [(viewport[0]-wid),0, (viewport[0]-wid),30, viewport[0],30, viewport[0],0, 1,1,1]
        self.line_2 = [0,30, 0,45, wid,45, wid,30, 0,0,1]
        self.line_2_dash = [(viewport[0]-wid),30, (viewport[0]-wid),45, viewport[0],45, viewport[0],30, 0,0,1]
        self.line_3 = [0,45, 0,300, wid,300 ,wid,45, 1,1,1]
        self.line_3_dash = [(viewport[0]-wid),45, (viewport[0]-wid),300, viewport[0],300 ,viewport[0],45, 1,1,1]
        self.line_4 = [0,300, 0,400, wid,400, wid,300, 1,1,0]
        self.line_4_dash = [(viewport[0]-wid),300, (viewport[0]-wid),400, viewport[0],400, viewport[0],300, 1,1,0]
        self.line_5 = [0,400, 0,500, wid,500, wid,400, 0,1,0]
        self.line_5_dash = [(viewport[0]-wid),400, (viewport[0]-wid),500, viewport[0],500, viewport[0],400, 0,1,0]
        self.line_6 = [0,500, 0,600, wid,600, wid,500 ,1,(128/255),0]
        self.line_6_dash = [(viewport[0]-wid),500, (viewport[0]-wid),600, viewport[0],600, viewport[0],500, 1,(128/255),0]
        self.line_7 = [0,600, 0,viewport[1], wid,viewport[1], wid,600 ,0,0,1]
        self.line_7_dash = [(viewport[0]-wid),600, (viewport[0]-wid),viewport[1], viewport[0],viewport[1], viewport[0],600, 0,0,1]
        self.top_line = [wid,viewport[1],(viewport[0]-wid),viewport[1],(viewport[0]-wid),(viewport[1]-wid),wid,(viewport[1]-wid), 0,0,1]

        self.lines = [self.line_1, self.line_1_dash,
                      self.line_2, self.line_2_dash,
                      self.line_3, self.line_3_dash,
                      self.line_4, self.line_4_dash,
                      self.line_5, self.line_5_dash,
                      self.line_6, self.line_6_dash,
                      self.line_7, self.line_7_dash,
                      self.top_line]

    def update(self):
        glLoadIdentity()
        for l in self.lines:
            glColor(l[8],l[9],l[10])
            glBegin(GL_QUADS) 
            glVertex(l[0],l[1],0)
            glVertex(l[2],l[3],0) 
            glVertex(l[4],l[5],0) 
            glVertex(l[6],l[7],0)
            glEnd()

class Game:
    def __init__(self):
        self.shift_counter = 0
        self.dl = False
        self.el = 0
        self.bl = ball(100,100)
        self.p = player(0,30,2,45)
        self.blist = bricklvls(0, 0, 1, 1, 0)
        self.br = borders()
        self.player_score = 0

    def update(self): 
        global lose
        self.br.update()
        self.p.update()
        self.bl.update()
        for i in range(len(self.blist)):
            if (self.shift_counter == 100): 
                self.blist[i].shift()
                if (i == len(self.blist) - 1):
                    self.shift_counter = 0
            self.blist[i].update()
            if self.blist[i].hit(): self.dl, self.el = True, i
        if self.dl:
            self.bl.bounce()
            self.blist.pop(self.el)
            self.dl = False
            self.player_score += 1
        self.shift_counter += 1

def MouseMotion(x, y):
	global mouse_x
	mouse_x=x
    
def keyboard(key, x, y):
        global lose,start
        if key == b"e": 
                sys.exit(0)
        if key == b"r":
                lose = False
        if key == b"s":
                start = True

def Timer(v): 	
	Display() 	
	glutTimerFunc(time_interval,Timer,1)

def Text(string, x, y, size = 1, r = 1, g = 1, b = 1):
        glLineWidth(2)
        glColor(r,g,b)
        glLoadIdentity() 
        glTranslate(x,y,0)
        glScale(0.13*size,0.13*size,1*size)
        string = string.encode()
        for c in string:
                glutStrokeCharacter(GLUT_STROKE_ROMAN , c ) 

g = Game()

def Display():
    global g, lose,start
    glClear(GL_COLOR_BUFFER_BIT)
    glColor(1,1,1)
    if start:
        g.update()
        Text("PC: " + str(g.bl.PC_score), (viewport[0]/2), 10, 1)
        Text("Player: " + str(g.player_score), (viewport[0]/2)-250, 10, 1)
    else:
        Text("BREAKOUT", (viewport[0]/2) - 170, (viewport[1]/2) + 70, 4)
        Text("Press S to start", (viewport[0]/2) - 80, (viewport[1]/2)-20, 1, 0, 1)
    glutSwapBuffers()

def main():
   glutInit()
   glutInitDisplayMode ( GLUT_DOUBLE | GLUT_RGB)
   glutInitWindowSize (viewport[0], viewport[1])
   glutInitWindowPosition (0, 0)
   glutCreateWindow (b"Breakout")
   glutDisplayFunc(Display)
   glutTimerFunc(time_interval,Timer,1)
   glutKeyboardFunc(keyboard)
   glutPassiveMotionFunc(MouseMotion)
   init() 
   glutMainLoop()

main()