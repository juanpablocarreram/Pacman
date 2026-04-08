import pygame
from Pacman import Pacman
from Ghost import Ghost
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import os
import numpy as np
import pandas as pd

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
#from Pacman import Pacman
#from Ghost import Ghost

screen_width = 800
screen_height = 800

#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
#Dimension del plano
DimBoard = 400

#Arreglo para el manejo de texturas
textures = []
#Nombre de los archivos a usar
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
img_map = os.path.join(BASE_PATH, 'mapa.bmp')
img_pacman = os.path.join(BASE_PATH, 'pacman.bmp')
img_ghost1 = os.path.join(BASE_PATH, 'fantasma1.bmp')
img_ghost2 = os.path.join(BASE_PATH, 'fantasma2.bmp')
img_ghost3 = os.path.join(BASE_PATH, 'fantasma3.bmp')
img_ghost4 = os.path.join(BASE_PATH, 'fantasma4.bmp')


file_csv = os.path.join(BASE_PATH, 'mapa.csv')
matrix = np.array(pd.io.parsers.read_csv(file_csv, header=None)).astype("int")

#Matriz de Control para mapeo entre pixeles <-> coord donde se localizan esquinas
MC = [
    [10,0,21,0,11,10,0,21,0,11],
    [24,0,25,21,23,23,21,25,0,22],
    [12,0,22,12,11,10,13,24,0,13],
    [0,0,0,10,23,23,11,0,0,0],
    [26,0,25,22,0,0,24,25,0,27],
    [0,0,0,24,0,0,22,0,0,0],
    [10,0,25,23,11,10,23,25,0,11],
    [12,11,24,21,23,23,21,22,10,13],
    [10,23,13,12,11,10,13,12,23,11],
    [12,28,28,28,23,23,28,28,28,13]
]

xMC = [22,50,92,136,178,221,262,308,350,378]

XPxToMC = np.full(400, -1, dtype=int)
for i in range(len(xMC)):
    XPxToMC[xMC[i]] = i
""" XPxToMC[22] = 0
XPxToMC[50] = 1
XPxToMC[92] = 2
XPxToMC[136] = 3
XPxToMC[178] = 4
XPxToMC[221] = 5
XPxToMC[262] = 6
XPxToMC[308] = 7
XPxToMC[350] = 8
XPxToMC[378] = 9 """
 
yMC = [20,72,109,150,187,225,264,303,342,382]
#YPxToMC = np.zeros((361,), dtype=int)
YPxToMC = np.full(400, -1, dtype=int)
for i in range(len(xMC)):
    YPxToMC[yMC[i]] = i
""" YPxToMC[20] = 0
YPxToMC[72] = 1
YPxToMC[109] = 2
YPxToMC[150] = 3
YPxToMC[187] = 4
YPxToMC[225] = 5
YPxToMC[264] = 6
YPxToMC[303] = 7
YPxToMC[342] = 8
YPxToMC[382] = 9 """

#pathfinding variables
path = []
grid = []

#pacman
player = Pacman(matrix, MC, XPxToMC, YPxToMC,156,303)
#fantasmas
ghosts = []
for i in range(4):
    """ Falta ver que coordenadas le pondremos a los fantasmas"""
    random_x = np.random.choice(xMC)
    random_y = np.random.choice(yMC)
    while MC[YPxToMC[random_y]][XPxToMC[random_x]] == 0:
        random_x = np.random.choice(xMC)
        random_y = np.random.choice(yMC)
    ghosts.append(Ghost(matrix, MC, XPxToMC, YPxToMC, random_x, random_y))

pygame.init()

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image,"RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D) 
    
def Init():
    screen = pygame.display.set_mode(
        (400, 400), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,400,400,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    #textures[0]: plano
    Texturas(img_map)
    #textures[1]: pacman
    Texturas(img_pacman)
    #textures[2]: fantasma1
    Texturas(img_ghost1)
    #textures[3]: fantasma2
    Texturas(img_ghost2)
    #textures[4]: fantasma3
    Texturas(img_ghost3)
    #textures[5]: fantasma4
    Texturas(img_ghost4)
    #se pasan las texturas a los objetos
    player.loadTextures(textures,1)
    ghosts[0].loadTextures(textures,2)
    ghosts[1].loadTextures(textures,3)
    ghosts[2].loadTextures(textures,4)
    ghosts[3].loadTextures(textures,5)
    
def PlanoTexturizado():
    #Activate textures
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    #front face
    glBindTexture(GL_TEXTURE_2D, textures[0])    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2d(0, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex2d(0, DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex2d(DimBoard, DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex2d(DimBoard, 0)
    glEnd()              
    glDisable(GL_TEXTURE_2D)
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()
    PlanoTexturizado()
    player.draw()
    for g in ghosts:
        g.draw()
    
done = False
Init()
clock = pygame.time.Clock()
direccionPacman = [0, 0]
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
    """ Check for key presses and update Pacman's direction """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        direccionPacman = [-1, 0]
        if player.direccion == [1,0]:
            player.update(direccionPacman)
        player.direccionFutura = direccionPacman
    elif keys[pygame.K_RIGHT]:
        direccionPacman = [1, 0]
        if player.direccion == [-1,0]:
            player.update(direccionPacman)
        player.direccionFutura = direccionPacman
    elif keys[pygame.K_UP]:
        direccionPacman = [0, -1]
        if player.direccion == [0,1]:
            player.update(direccionPacman)
        player.direccionFutura = direccionPacman
    elif keys[pygame.K_DOWN]:
        direccionPacman = [0, 1]
        if player.direccion == [0,-1]:
            player.update(direccionPacman)
        player.direccionFutura = direccionPacman
    player.performObjectCollisionLogic()
    for g in ghosts:
        g.performObjectCollisionLogic()
    display()
    pygame.display.flip()
    clock.tick(80)
pygame.quit()
    

