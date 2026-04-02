import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import os
import numpy as np
import pandas as pd

class Pacman:
    def __init__(self,mapa, mc, x_mc, y_mc):
        #Matriz de control que almacena los IDs de las intersecciones
        self.MC = mc
        #Vectores que almacenan las coordenadas 
        self.XPxToMC = x_mc
        self.YPxToMC = y_mc
        #se resplanda el mapa en terminos de pixeles
        self.mapa = mapa
        #si el pacman se encuentra en estado inicial del juego
        self.start = 1  
        self.x = 156
        self.y = 303
        self.angulo_direccion = 180
        self.direccion = [-1,0]
        self.direccionFutura = [-1,0]
        self.velocidad = 1
        
    def loadTextures(self, texturas, id):
        self.texturas = texturas
        self.Id = id
    """ Funcion para detectar la esquina en la cual se encuentra pacman (-1 si no se encuentra en una esquina)"""
    def esquinaActual(self):
        if self.XPxToMC[self.x] != -1 and self.YPxToMC[self.y] != -1:
            return self.MC[self.YPxToMC[self.y]][self.XPxToMC[self.x]]
        return -1
    """Funcion para detectar colisiones con paredes y mover al pacman en la direccion dada por el usuario"""
    def performObjectCollisionLogic(self):
        esquinaActual = self.esquinaActual()
        if esquinaActual != -1 and esquinaActual != 0:
            if self.direccionFutura == [1,0] and (esquinaActual == 10 or esquinaActual == 12 or esquinaActual == 21 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 26 or esquinaActual == 28):
                self.update(self.direccionFutura)
            elif self.direccionFutura == [-1,0] and (esquinaActual == 11 or esquinaActual == 13 or esquinaActual == 21 or esquinaActual ==22 or esquinaActual == 23 or esquinaActual == 25 or esquinaActual == 27 or esquinaActual == 28):
                self.update(self.direccionFutura)
            elif self.direccionFutura == [0,1] and (esquinaActual == 10 or esquinaActual == 11 or esquinaActual == 21 or esquinaActual == 22 or esquinaActual == 24 or esquinaActual == 25):
                self.update(self.direccionFutura)
            elif self.direccionFutura == [0,-1] and (esquinaActual == 12 or esquinaActual == 13 or esquinaActual == 22 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25):
                self.update(self.direccionFutura)
            else:
                if self.direccion == [1,0] and (esquinaActual == 10 or esquinaActual == 12 or esquinaActual == 21 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 26 or esquinaActual == 28):
                    self.update(self.direccion)
                elif self.direccion == [-1,0] and (esquinaActual == 11 or esquinaActual == 13 or esquinaActual == 21 or esquinaActual ==22 or esquinaActual == 23 or esquinaActual == 25 or esquinaActual == 27 or esquinaActual == 28):
                    self.update(self.direccion)
                elif self.direccion == [0,1] and (esquinaActual == 10 or esquinaActual == 11 or esquinaActual == 21 or esquinaActual == 22 or esquinaActual == 24 or esquinaActual == 25):
                    self.update(self.direccion)
                elif self.direccion == [0,-1] and (esquinaActual == 12 or esquinaActual == 13 or esquinaActual == 22 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25):
                    self.update(self.direccion)
                else:
                    self.update([0,0])
    """ Funcion para actualizar la direccion en base a entradas del usuario y a la posicion actual del pacman"""
    def update(self, dir):
        #Si el pacman se encuentra en estado inicial del juego, se le asigna una direccion de movimiento
        if self.start == 1:
            self.direccion = [-1,0]
            self.direccionFutura = [-1,0]
            self.angulo_direccion = 180
            self.start = 0
        else:
            #Si el pacman no se encuentra en estado inicial del juego, se le asigna la direccion de movimiento dada por el usuario
            self.direccion = [dir[0],dir[1]]
            self.angulo_direccion = math.atan2(self.direccion[1], self.direccion[0]) * 180 / math.pi
            if self.angulo_direccion < 0:
                self.angulo_direccion += 360
    """ Funcion para renderizar (dibujar) el pacman """
    def draw(self):
        self.x += self.direccion[0] * self.velocidad
        self.y += self.direccion[1] * self.velocidad
        #Se dibuja el pacman en la posicion dada por la matriz de control
        glPushMatrix()
        glTranslatef(self.x, self.y,0)
        glRotatef(self.angulo_direccion, 0, 0, 1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texturas[self.Id])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-12, -12)
        glTexCoord2f(1, 0)
        glVertex2f(12, -12)
        glTexCoord2f(1, 1)
        glVertex2f(12, 12)
        glTexCoord2f(0, 1)
        glVertex2f(-12, 12)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


  