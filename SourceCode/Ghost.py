import numpy as np
import random
from Entidad import Entidad
mapa_numeros = {
        10: [[1, 0], [0, 1]],
        11: [[-1, 0], [0, 1]],
        12: [[1, 0], [0, -1]],
        13: [[-1, 0], [0, -1]],
        21: [[1, 0], [-1,0], [0, 1]],
        22: [[-1, 0], [0,-1], [0, 1]],
        23: [[1, 0], [-1,0], [0, -1]],
        24: [[1, 0], [0,-1], [0, 1]],
        25: [[1, 0], [-1,0], [0,-1], [0, 1]],
        26: [[1, 0]],
        27: [[-1,0]]
        }   
xMC = [22,50,92,136,178,221,262,308,350,378]
yMC = [20,72,109,150,187,225,264,303,342,382]
class Ghost(Entidad):
    def __init__(self,mapa, mc, x_px_to_mc, y_px_to_mc,x_inicial, y_inicial,x_mc, y_mc, pacman):
        super().__init__(mapa, mc, x_px_to_mc, y_px_to_mc,x_inicial, y_inicial)
        self.xMC = x_mc
        self.yMC = y_mc
        self.angulo_direccion = 0
        self.pacman = pacman

    def movimiento_fantasma_aleatorio(self):
        actual = self.esquinaActual()
        listamovimiento = mapa_numeros.get(actual)
        listamovimientovalido = []
        if listamovimiento is not None:
            for movimiento in listamovimiento:
                if(self.direccion != [-movimiento[0],-movimiento[1]] or actual==26 or actual==27):
                    listamovimientovalido.append(movimiento)
            self.update(random.choice(listamovimientovalido))

    def movimiento_fantasma_heuristico(self):
        indice_Y_fantasma = self.YPxToMC[self.y]
        indice_X_fantasma = self.XPxToMC[self.x]
        indice_Y_pacman = self.YPxToMC[self.pacman.y]
        indice_X_pacman = self.XPxToMC[self.pacman.x]
        actual = self.esquinaActual()
        listamovimiento = mapa_numeros.get(actual)
        listadecasillasposibles = []
        listamovimientovalido = []
        if listamovimiento is not None:
            for movimiento in listamovimiento:
                if(self.direccion != [-movimiento[0],-movimiento[1]] or actual==26 or actual==27):
                    listadecasillasposibles.append(self.MC[indice_Y_fantasma + movimiento[1]][indice_X_fantasma + movimiento[0]])
                    listamovimientovalido.append(movimiento)
            siguientemovimiento = min(listamovimientovalido, key=lambda m: np.hypot((xMC[indice_X_fantasma + m[0]]) - self.pacman.x, (yMC[indice_Y_fantasma + m[1]]) - self.pacman.y))
            self.update(siguientemovimiento)

    def calcular_esquinas_vecinas(self,esquina):
        esquinas_vecinas = []
        indice_x = self.XPxToMC[esquina[0]]
        indice_y = self.YPxToMC[esquina[1]]
        if(indice_x != -1 and indice_y != -1):
            movimientos = mapa_numeros.get(self.MC[indice_y][indice_x])
        else:
            return esquinas_vecinas
        if movimientos is not None:
            for movimiento in movimientos:
                esquinas_vecinas.append((self.xMC[indice_x + movimiento[0]], self.yMC[indice_y + movimiento[1]]))
        return esquinas_vecinas
    """ Metodo a implementar para movimiento cooperativo entre fantasmas  """
    def movimiento_fantasma_a_estrella(self,nodoObjetivo):
        pass
    def update(self, dir):
        self.direccion = [dir[0],dir[1]]