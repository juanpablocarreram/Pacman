import numpy as np
import random
from Entidad import Entidad
class Ghost(Entidad):
    def __init__(self,mapa, mc, x_mc, y_mc,x_inicial, y_inicial):
        super().__init__(mapa, mc, x_mc, y_mc,x_inicial, y_inicial)
        self.angulo_direccion = 0
    def performObjectCollisionLogic(self):
        esquinaActual = self.esquinaActual()
        if esquinaActual != -1 and esquinaActual != 0:
            posiblesDirecciones = []
            while len(posiblesDirecciones) <= 0:
                if (esquinaActual == 10 or esquinaActual == 12 or esquinaActual == 21 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 26 or esquinaActual == 28):
                    if self.direccion != [-1,0]:
                        posiblesDirecciones.append([1,0])
                if (esquinaActual == 11 or esquinaActual == 13 or esquinaActual == 21 or esquinaActual ==22 or esquinaActual == 23 or esquinaActual == 25 or esquinaActual == 27 or esquinaActual == 28):
                    if self.direccion != [1,0]:
                        posiblesDirecciones.append([-1,0])
                if (esquinaActual == 10 or esquinaActual == 11 or esquinaActual == 21 or esquinaActual == 22 or esquinaActual == 24 or esquinaActual == 25):
                    if self.direccion != [0,-1]:
                        posiblesDirecciones.append([0,1])
                if (esquinaActual == 12 or esquinaActual == 13 or esquinaActual == 22 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25):
                    if self.direccion != [0,1]:
                        posiblesDirecciones.append([0,-1])
                if len(posiblesDirecciones) <= 0:
                    self.direccion = [0,0]
                else:
                    self.update(random.choice(posiblesDirecciones))
    def update(self, dir):
        self.direccion = [dir[0],dir[1]]