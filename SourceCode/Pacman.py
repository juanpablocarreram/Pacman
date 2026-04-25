from Entidad import Entidad
import numpy as np
import math
class Pacman(Entidad):
    def __init__(self,mapa, mc, x_pxmc, y_pxmc,x_inicial, y_inicial,x_mc,y_mc):
        super().__init__(mapa, mc, x_pxmc, y_pxmc,x_inicial, y_inicial,x_mc,y_mc)
        self.esquina_futura = (136,303)
        self.esquina_reciente = (178,303)
        self.esquina_respaldo = (178,303)
    def performObjectCollisionLogic(self):
        esquinaActual = self.esquinaActual()
        if esquinaActual != -1:
            self.esquina_respaldo = self.esquina_reciente
            self.esquina_reciente = (self.x,self.y)
            if self.direccionFutura == [1,0] and (esquinaActual == 10 or esquinaActual == 12 or esquinaActual == 21 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 26 or esquinaActual == 28):
                self.update(self.direccionFutura)
                self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
            elif self.direccionFutura == [-1,0] and (esquinaActual == 11 or esquinaActual == 13 or esquinaActual == 21 or esquinaActual ==22 or esquinaActual == 23 or esquinaActual == 25 or esquinaActual == 27 or esquinaActual == 28):
                self.update(self.direccionFutura)
                self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
            elif self.direccionFutura == [0,1] and (esquinaActual == 10 or esquinaActual == 11 or esquinaActual == 21 or esquinaActual == 22 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 29):
                self.update(self.direccionFutura)
                self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
            elif self.direccionFutura == [0,-1] and (esquinaActual == 12 or esquinaActual == 13 or esquinaActual == 22 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 29):
                self.update(self.direccionFutura)
                self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
            else:
                if self.direccion == [1,0] and (esquinaActual == 10 or esquinaActual == 12 or esquinaActual == 21 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 26 or esquinaActual == 28):
                    self.update(self.direccion)
                    self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
                elif self.direccion == [-1,0] and (esquinaActual == 11 or esquinaActual == 13 or esquinaActual == 21 or esquinaActual ==22 or esquinaActual == 23 or esquinaActual == 25 or esquinaActual == 27 or esquinaActual == 28):
                    self.update(self.direccion)
                    self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
                elif self.direccion == [0,1] and (esquinaActual == 10 or esquinaActual == 11 or esquinaActual == 21 or esquinaActual == 22 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 29):
                    self.update(self.direccion)
                    self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
                elif self.direccion == [0,-1] and (esquinaActual == 12 or esquinaActual == 13 or esquinaActual == 22 or esquinaActual == 23 or esquinaActual == 24 or esquinaActual == 25 or esquinaActual == 29):
                    self.update(self.direccion)
                    self.esquina_futura  = (self.xMC[self.XPxToMC[self.x] + self.direccionFutura[0]], self.yMC[self.YPxToMC[self.y] + self.direccionFutura[1]])
                else:
                    self.update([0,0])
                    self.esquina_futura = self.esquina_respaldo
    def update(self, dir):
        self.direccion = [dir[0],dir[1]]
        self.angulo_direccion = math.atan2(self.direccion[1], self.direccion[0]) * 180 / math.pi
        if self.angulo_direccion < 0:
            self.angulo_direccion += 360

    