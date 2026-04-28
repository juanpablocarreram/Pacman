import numpy as np
import random
import heapq
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
        27: [[-1,0]],
        28: [[1,0],[-1,0]],
        29:[[0,1],[0,-1]]
        }   
xMC = [22,50,92,136,178,221,262,308,350,378]
yMC = [20,72,109,150,187,225,264,303,342,382]
class Ghost(Entidad):
    def __init__(self,mapa, mc, x_px_to_mc, y_px_to_mc,x_inicial, y_inicial,x_mc, y_mc, pacman):
        super().__init__(mapa, mc, x_px_to_mc, y_px_to_mc,x_inicial, y_inicial, x_mc, y_mc)
        self.angulo_direccion = 0
        self.pacman = pacman

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
    
    def calcular_manhattan(self,esquina1,esquina2):
        return abs(esquina1[0] - esquina2[0]) + abs(esquina1[1] - esquina2[1])
    
    """ Algoritmo de A* en mapa Pacman con esquinas como nodos"""
    def a_estrella(self,nodoOrigen,nodoObjetivo):
        """ Se verifica que el nodo origen y el nodo objetivo sean validos (que se encuentren en una esquina) """
        if (self.XPxToMC[nodoOrigen[0]] != -1 and self.YPxToMC[nodoOrigen[1]] != -1) and (self.XPxToMC[nodoObjetivo[0]] != -1 and self.YPxToMC[nodoObjetivo[1]] != -1):
            open_list = []
            closed_list = set()
            caracteristicas_nodos = {}
            manhattan_primero = self.calcular_manhattan((nodoOrigen[0],nodoOrigen[1]), nodoObjetivo)
            heapq.heappush(open_list,(manhattan_primero, nodoOrigen[0], nodoOrigen[1]))
            caracteristicas_nodos[(nodoOrigen[0],nodoOrigen[1])] = {"g":0, "h": manhattan_primero, "f": manhattan_primero, "padre":None}
            while open_list:
                nodo_actual = heapq.heappop(open_list)
                """ Si el nodo actual tiene un valor de f mayor al valor de f almacenado significa que ya se encontro un camino mas corto hacia ese nodo y se ignora """
                if caracteristicas_nodos[(nodo_actual[1], nodo_actual[2])]["f"] < nodo_actual[0]:
                    continue
                """ Si el nodo actual es el objetivo se reconstruye el camino y se actualiza el movimiento del fantasma """
                if (nodo_actual[1], nodo_actual[2]) == nodoObjetivo:
                    nodo_actual = (nodo_actual[1], nodo_actual[2])
                    camino = []
                    while nodo_actual is not None:
                        camino.append((nodo_actual[0], nodo_actual[1]))
                        nodo_actual = caracteristicas_nodos[(nodo_actual[0], nodo_actual[1])]["padre"]
                    camino.reverse()
                    return camino
                """ Se agrega el nodo con menor f a la lista cerrada """
                closed_list.add((nodo_actual[1], nodo_actual[2]))
                esquinas_vecinas = self.calcular_esquinas_vecinas((nodo_actual[1], nodo_actual[2]))
                """ Se calculan las caracteristicas de los nodos vecinos del nodo con menor f"""
                for esquina_vecina in esquinas_vecinas:
                    """ Si el nodo vecino ya fue evaluado se ignora """
                    if esquina_vecina in closed_list:
                        continue
                    g = caracteristicas_nodos[(nodo_actual[1], nodo_actual[2])]["g"] + 1
                    h = self.calcular_manhattan(esquina_vecina, nodoObjetivo)
                    f = g + h
                    """ Si no esta en la lista abierta o se encuentra un camino mas corto se actualizan las caractersticas del nodo """
                    if esquina_vecina not in caracteristicas_nodos or g < caracteristicas_nodos[esquina_vecina]["g"]:
                        caracteristicas_nodos[esquina_vecina] = {"g": g, "h": h, "f": f, "padre": (nodo_actual[1], nodo_actual[2])}
                        heapq.heappush(open_list, (f, esquina_vecina[0], esquina_vecina[1]))
                        
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
        esquinas_posibles = self.calcular_esquinas_vecinas((self.x,self.y))
        if len(esquinas_posibles) > 0:
            distancia_minima = (abs(esquinas_posibles[0][0] - self.pacman.x) ** 2 + abs(esquinas_posibles[0][1] - self.pacman.y) ** 2) ** 0.5
            indice_esquina_mas_cercana = 0
            for i in range(1, len(esquinas_posibles)):
                distancia = (abs(esquinas_posibles[i][0] - self.pacman.x) ** 2 + abs(esquinas_posibles[i][1] - self.pacman.y) ** 2) ** 0.5
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    indice_esquina_mas_cercana = i
            movimiento = [0,0]
            if self.x < esquinas_posibles[indice_esquina_mas_cercana][0]:
                movimiento[0] = 1
            elif self.x > esquinas_posibles[indice_esquina_mas_cercana][0]:
                movimiento[0] = -1
            if self.y < esquinas_posibles[indice_esquina_mas_cercana][1]:
                movimiento[1] = 1
            elif self.y > esquinas_posibles[indice_esquina_mas_cercana][1]:
                movimiento[1] = -1
            self.update(movimiento)

    """ Movimiento del fantasma utilizando el algoritmo de A* """
    def movimiento_fantasma_a_estrella(self, nodoObjetivo, partner_ghost=None, partner_weight=0.8):
        if self.esquinaActual() != -1:
            if self.x == nodoObjetivo[0] and self.y == nodoObjetivo[1]:
                self.movimiento_fantasma_heuristico()
                return
            camino = self.a_estrella((self.x,self.y), nodoObjetivo)
            if camino is not None and len(camino) > 1:
                siguiente_esquina = camino[1]
                reverse_dir = [-self.direccion[0], -self.direccion[1]] if self.direccion != [0,0] else None
                if partner_ghost is not None:
                    esquinas_posibles = self.calcular_esquinas_vecinas((self.x, self.y))
                    valid_esquinas = []
                    for esquina in esquinas_posibles:
                        movimiento_candidato = [0, 0]
                        if self.x < esquina[0]:
                            movimiento_candidato[0] = 1
                        elif self.x > esquina[0]:
                            movimiento_candidato[0] = -1
                        if self.y < esquina[1]:
                            movimiento_candidato[1] = 1
                        elif self.y > esquina[1]:
                            movimiento_candidato[1] = -1
                        if reverse_dir is not None and movimiento_candidato == reverse_dir:
                            continue
                        valid_esquinas.append(esquina)
                    if valid_esquinas:
                        mejor_score = -float('inf')
                        mejor_esquina = siguiente_esquina if (reverse_dir is None or [int(self.x < siguiente_esquina[0]) - int(self.x > siguiente_esquina[0]), int(self.y < siguiente_esquina[1]) - int(self.y > siguiente_esquina[1])] != reverse_dir) else valid_esquinas[0]
                        for esquina in valid_esquinas:
                            distancia_pacman = ((esquina[0] - self.pacman.x) ** 2 + (esquina[1] - self.pacman.y) ** 2) ** 0.5
                            distancia_partner = ((esquina[0] - partner_ghost.x) ** 2 + (esquina[1] - partner_ghost.y) ** 2) ** 0.5
                            path_bonus = 2 if esquina == siguiente_esquina else 0
                            score = -distancia_pacman + partner_weight * distancia_partner + path_bonus
                            if score > mejor_score:
                                mejor_score = score
                                mejor_esquina = esquina
                        siguiente_esquina = mejor_esquina
                else:
                    movimiento_siguiente = [0,0]
                    if self.x < siguiente_esquina[0]:
                        movimiento_siguiente[0] = 1
                    elif self.x > siguiente_esquina[0]:
                        movimiento_siguiente[0] = -1
                    if self.y < siguiente_esquina[1]:
                        movimiento_siguiente[1] = 1
                    elif self.y > siguiente_esquina[1]:
                        movimiento_siguiente[1] = -1
                    if reverse_dir is not None and movimiento_siguiente == reverse_dir:
                        esquinas_posibles = self.calcular_esquinas_vecinas((self.x, self.y))
                        alternativa = None
                        for esquina in esquinas_posibles:
                            movimiento_candidato = [0, 0]
                            if self.x < esquina[0]:
                                movimiento_candidato[0] = 1
                            elif self.x > esquina[0]:
                                movimiento_candidato[0] = -1
                            if self.y < esquina[1]:
                                movimiento_candidato[1] = 1
                            elif self.y > esquina[1]:
                                movimiento_candidato[1] = -1
                            if movimiento_candidato == reverse_dir:
                                continue
                            if alternativa is None or self.calcular_manhattan(esquina, nodoObjetivo) < self.calcular_manhattan(alternativa, nodoObjetivo):
                                alternativa = esquina
                        if alternativa is not None:
                            siguiente_esquina = alternativa
                movimiento = [0,0]
                if self.x < siguiente_esquina[0]:
                    movimiento[0] = 1
                elif self.x > siguiente_esquina[0]:
                    movimiento[0] = -1
                if self.y < siguiente_esquina[1]:
                    movimiento[1] = 1
                elif self.y > siguiente_esquina[1]:
                    movimiento[1] = -1
                self.update(movimiento)
            else:
                self.movimiento_fantasma_heuristico()
    def update(self, dir):
        self.direccion = [dir[0],dir[1]]