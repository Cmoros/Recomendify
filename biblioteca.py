from array import array
from collections import deque
from grafo import Grafo
import random

DAMPING_FACTOR = 0.85
TOLERANCIA_PAGERANK = 0.001
TOLERANCIA_PAGERANK_P = 0.95
TOLERANCIA_RANDOM_WALK = 0.001

"""Recibe un grafo, el vertice origen y el vertice destino
Determina el camino mínimo entre el origen y el destino con BFS
Devuelve en forma de lista el camino desde el origen al destino
De no existir un camino, devuelve una lista vacia
Complejidad: O(V + E)
"""
def camino_minimo(grafo:Grafo, origen, destino):
    padres = {}
    padres[origen] = None
    cola = deque()
    cola.append(origen)
    pila = deque()
    while len(cola) > 0:
        vertice = cola.popleft()
        for ady in grafo.adyacentes(vertice):
            if ady not in padres:
                padres[ady] = vertice
                if ady == destino:
                    pila.append(ady)
                    break
                cola.append(ady)
    return reconstruccion_camino(pila, origen, destino, padres)


    """Recibe la pila resultado, el vertice origen y destino, y el dict padres
    Con el dict padres, apila en la pila hasta llegar al vertice origen
    Devuelve el camino en forma de lista
    """
def reconstruccion_camino(pila:deque, origen, destino, padres):
    if len(pila) > 0:
        vertice = destino
        while vertice != origen:
            pila.appendleft(padres[vertice])
            vertice = padres[vertice]
    return list(pila)


    """Recibe un grafo, el vertice origen y la longitud del ciclo
    Determina un ciclo de longitud n que lleve al origen a si mismo sin repetir vertices
    Devuelve una lista con el camino del ciclo
    En caso de no existir el ciclo, devuelve una lista vacia
    """
def ciclo_n(grafo:Grafo, origen, n):
    pila = [origen]
    elementos_pila = set()
    elementos_pila.add(origen)
    for ady in grafo.adyacentes(origen):
        if dfs_ciclo_n(grafo, ady, pila, n, origen, elementos_pila):
            return pila
    return []


    """Recibe el grafo estudiado, el vertice actual, la pila, la cantidad n y el vertice origen al que se quiere encontrar
    Agrega el vertice actual a pila y estudia que, si la pila esta en su tamaño n, si tiene al vertice origen en sus adyacentes
    En caso de que si, se encontró resultado y devuelve True, en caso de que no, realiza dfs a los vertices adyacentes
    que no esten en la pila.
    Al volver de su recursion, si no se encontró ciclo en ningun adyacente, saca al vertice actual de la pila y retorna False
    """
def dfs_ciclo_n(grafo:Grafo, vertice, pila:array, n, origen, elementos_pila:set):
    adyacentes = grafo.adyacentes(vertice)
    pila.append(vertice)
    elementos_pila.add(vertice)
    if len(pila) == n:
        if origen in adyacentes:
            pila.append(origen)
            return True
    else:
        for ady in adyacentes:
            if ady in elementos_pila:
                continue
            if dfs_ciclo_n(grafo, ady, pila, n, origen, elementos_pila):
                return True
    pila.pop()
    elementos_pila.remove(vertice)
    return False


    """Recibe un grafo, el vertice origen y la distancia n
    Con BFS, determina los vertices a distancia n del origen y los cuenta
    Devuelve el contador
    """
def todos_en_rango_n(grafo:Grafo, origen, n):
    if n== 0: return 1
    resultado = 0
    distancia = {}
    cola = deque()
    distancia[origen] = 0
    cola.append(origen)
    while len(cola) > 0:
        vertice = cola.popleft()
        for ady in grafo.adyacentes(vertice):
            if ady not in distancia:
                distancia[ady] = distancia[vertice] + 1 
                if distancia[ady] == n:
                    resultado += 1
                else:
                    cola.append(ady)
    return resultado


    """Recibe un grafo
    Calcula el grado de cada vertice, para un caso de grafo no dirigido
    Devuelve el diccionario con los grados
    """
def calculo_grado_salida(grafo:Grafo):
    grado = {}
    for vertice in grafo.obtener_vertices():
        grado[vertice] = len(grafo.adyacentes(vertice))
    return grado


    """Recibe un grafo
    Calcula el pagerank de cada vertice, realizando iteraciones, en las que modifica
    cada valor del vertiece segun su valor anterior, el DUMPING FACTOR, y su grado,
    hasta que el cambio cada uno sea menor a la tolerancia
    Devuelve el pagerank
    """
def pagerank(grafo:Grafo):
    pagerank = {}
    anterior = {}
    vertices = grafo.obtener_vertices()
    V = len(vertices)
    grado = calculo_grado_salida(grafo)
    for vertice in vertices:
        anterior[vertice] = 1/V
        pagerank[vertice] = 0
    cambios_totales = 0
    while cambios_totales < V:
        cambios_totales = 0
        for vertice in vertices:
            pagerank[vertice] += (1 - DAMPING_FACTOR)/V
            for ady in grafo.adyacentes(vertice):
                pagerank[ady] += DAMPING_FACTOR * anterior[vertice] / grado[vertice]
        for vertice in vertices:
            cambio = pagerank[vertice] - anterior[vertice]
            anterior[vertice] = pagerank[vertice]
            pagerank[vertice] = 0
            if abs(cambio) < TOLERANCIA_PAGERANK:
                cambios_totales += 1
    return anterior


    """Recibe un grafo y un listado de sus vertices
    Calcula un pagerank personalizado a partir del grafo:
    *Realiza una cantidad de iteraciones equivalente al doble de la cantidad de origenes, y en cada iteracion
    realiza un randomwalk a partir de algun vertice aleatorio de los origenes y actualiza el pagerank segun el valor actual de transmision y del grado
    de cada vertice visitados en el randomwalk
    En caso de que el cambio de cada elemento visitado en todas las iteraciones en comparacion con su valor anterior, sea mayor a la tolerancia,
    se termina el ciclo, caso contrario, se comienza de nuevo en *
    Devuelve el pagerank
    """
def pagerank_personalizado(grafo:Grafo, origenes:set):
    pagerank = {}
    grado = calculo_grado_salida(grafo)
    cambios_descartables = -1
    primera_iteracion = True
    valores_anteriores = {}
    lista_de_origenes = list(origenes)
    
    while cambios_descartables < len(valores_anteriores):
        valores_anteriores = {}
        cambios_descartables = 0
        for i in range(len(origenes)*2):
            vertice = random.choice(lista_de_origenes)
            if grado[vertice] == 0: continue
            random_walk(grafo, vertice, pagerank, grado, 1, valores_anteriores)
        if not primera_iteracion:
            for vertice in valores_anteriores:
                if valores_anteriores[vertice] / pagerank[vertice] > TOLERANCIA_PAGERANK_P:
                    cambios_descartables += 1
        else:
            primera_iteracion = False
    return pagerank


    """Randomwalk implementado de forma recursiva, recibe el grado, el vertice visitado actualmente,
    el pagerank, el diccionario de grados, la cantidad transmitida por la recursion anterior, y un diccionario con los valores modificados
    En cada recursion, se actualiza el valor del pagerank del vertice actual y se retransmite al siguiente
    adyacente aleatorio el valor correposdiente a la transmision anterior con su grado y hace el llamado recursivo
    En caso de que la transmision sea considerada "despreciable" se termina la recursion
    """
def random_walk(grafo:Grafo, vertice, pagerank, grado, transmision, valores_anteriores):
    rand = random.randint(0, grado[vertice]-1)
    ady = grafo.adyacentes(vertice)[rand]
    proxima_transmision = transmision/grado[vertice]
    if ady not in pagerank:
        pagerank[ady] = 0
    valores_anteriores[ady] = pagerank[ady]
    pagerank[ady] = pagerank[ady] + proxima_transmision
    if proxima_transmision < TOLERANCIA_RANDOM_WALK: 
        return
    random_walk(grafo, ady, pagerank, grado, proxima_transmision, valores_anteriores)