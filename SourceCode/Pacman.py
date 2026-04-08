from Entidad import Entidad
import numpy as np
import math
class Pacman(Entidad):
    def __init__(self,mapa, mc, x_mc, y_mc,x_inicial, y_inicial):
        super().__init__(mapa, mc, x_mc, y_mc,x_inicial, y_inicial)
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
    def update(self, dir):
        self.direccion = [dir[0],dir[1]]
        self.angulo_direccion = math.atan2(self.direccion[1], self.direccion[0]) * 180 / math.pi
        if self.angulo_direccion < 0:
            self.angulo_direccion += 360