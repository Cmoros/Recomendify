#!/usr/bin/python3
from grafo import Grafo
import sys
import biblioteca

LEN_ARGV = 2
RUTA_ARCHIVO = 1

ARCHIVO_USUARIO = 1
ARCHIVO_CANCION = 2
ARCHIVO_AUTOR = 3
ARCHIVO_PLAYLIST = 5

STDIN_ORDEN = 0
STDIN_CAMINO_ORIGEN = 1
STDIN_MAS_IMPORTANTES_CANTIDAD = 1
STDIN_RECOMENDACION_TIPO = 1
STDIN_RECOMENDACION_CANTIDAD = 2
STDIN_RECOMENDACION_DATO = 3
STDIN_CICLO_RANGO_CANTIDAD = 1
STDIN_CICLO_RANGO_ORIGEN = 2

"""Recibe el nombre el archivo
Crea el grafo de usuarios y canciones, de cada linea del archivo
Agrega al grafo cada usuario y cancion, y une usuario con cancion de tener una playlist con esa cancion
El peso de cada union sera el nombre de la playlist
Devuelve de grafo de usuarios y canciones
"""
def creacion_grafo_usuarios_canciones(nombre_archivo):
    grafo_u_c = Grafo(False)
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        archivo.readline()
        for line in archivo:
            line=line.split("\t")
            usuario = line[ARCHIVO_USUARIO]
            cancion = line[ARCHIVO_CANCION] + " - " + line[ARCHIVO_AUTOR]
            playlist = line[ARCHIVO_PLAYLIST]
            grafo_u_c.agregar_vertice(usuario, "usuario")
            grafo_u_c.agregar_vertice(cancion, "cancion")
            grafo_u_c.agregar_arista(usuario, cancion, playlist)
    return grafo_u_c


    """Recibe la linea introducida por stdin separada en un array y el grafo
    Obtiene a partir de la linea el origen y el destino deseado
    Verifica si se ingresaron 2 canciones como origen y destino
    De ser canciones, llama a la funcion camino_mas_corto.
    Devuelve ya sea el resultado de la verificacion, como el camino (si hay)
    """
def comando_camino(linea_separada, grafo_u_c:Grafo):
    origen = linea_separada[STDIN_CAMINO_ORIGEN]
    i = STDIN_CAMINO_ORIGEN + 1
    while linea_separada[i] != ">>>>":
        origen += " " + linea_separada[i]
        i += 1
    i += 1
    destino = linea_separada[i]
    i += 1
    while i < len(linea_separada):
        destino += " " + linea_separada[i]
        i += 1
    if grafo_u_c.tipo_vertice(origen) != "cancion" or grafo_u_c.tipo_vertice(destino) != "cancion":
        return "Tanto el origen como el destino deben ser canciones"
    else:
        return camino_mas_corto(grafo_u_c, origen, destino)


    """Recibe la linea introducida por stdin separada en un array y el grafo
    Obtiene a partir de la linea el tipo de recomendacion (ya sea canciones o usuarios)
    la cantidad de recomendaciones y las canciones de referencia para hacer la recomendacion
    Llama a la funcion de recomendacion y devuelve el listado de canciones
    """
def comando_recomendacion(linea_separada, grafo_u_c:Grafo):
    tipo = linea_separada[STDIN_RECOMENDACION_TIPO]
    cantidad = int(linea_separada[STDIN_RECOMENDACION_CANTIDAD])
    listado = set()
    dato = linea_separada[STDIN_RECOMENDACION_DATO]
    i = STDIN_RECOMENDACION_DATO + 1
    while i < len(linea_separada):
        if linea_separada[i] == ">>>>":
            listado.add(dato)
            dato = linea_separada[i+1]
            i += 1
            
        else:
            dato += " " + linea_separada[i]
        i += 1
    listado.add(dato)
    return recomendacion(grafo_u_c, tipo, cantidad, listado)


    """Recibe la linea introducida por stdin separada en un array
    Para los ultimos casos, de ciclo y rango, obtiene de la linea la cancion origen
    y la cantidad (que puede ser interpretado como la distancia o la longitud del ciclo)
    Devuelve la cantidad y el origen
    """
def separacion_cantidad_origen(linea_separada):
    cantidad = int(linea_separada[STDIN_CICLO_RANGO_CANTIDAD])
    origen = linea_separada[STDIN_CICLO_RANGO_ORIGEN]
    for i in range(STDIN_CICLO_RANGO_ORIGEN + 1, len(linea_separada)):
        origen += " " + linea_separada[i]
    return cantidad, origen


    """Recibe el grafo de usuarios y canciones, la cancion de la cual se va a partir y la cancion destino
    Crea el camino con biblioteca.camino_minimo y concatena en resultado el camino
    Devuelve el resultado
    """
def camino_mas_corto(grafo:Grafo, origen, destino):
    camino = biblioteca.camino_minimo(grafo, origen, destino)
    if len(camino)>0:
        j = 0
        resultado = origen
        while j < len(camino)-1:
            resultado += " --> aparece en playlist --> " + grafo.peso_arista(camino[j],camino[j+1])
            resultado += " --> de --> " + camino[j+1] + " --> tiene una playlist --> " + grafo.peso_arista(camino[j+1],camino[j+2])
            resultado += " --> donde aparece --> " + camino[j+2]
            j += 2
    else:
        resultado = "No se encontro recorrido"
    return resultado


    """Recibe el grafo de usuarios y canciones, el ranking(que puede estar vacio) y la cantidad de canciones
    De estar vacio, se crea el ranking con biblioteca.pagerank, se ordena y se concatenan
    las canciones al ranking. Segun la cantidad de canciones, se concatenan en resultado las canciones
    Devuelve el resultado
    """
def canciones_mas_importantes(grafo:Grafo, pagerank_canciones, cantidad):
    if len(pagerank_canciones) == 0:
        pagerank = biblioteca.pagerank(grafo)
        pagerank = sorted(pagerank, key = pagerank.get, reverse=True)
        for vertice in pagerank:
            if grafo.tipo_vertice(vertice) == "cancion":
                pagerank_canciones.append(vertice)
    resultado = pagerank_canciones[0]
    for i in range(1,cantidad):
        resultado += "; " + pagerank_canciones[i]
    return resultado


    """Recibe el grafo de usuarios y canciones, el tipo de recomendacion,
    la cantidad de recomendaciones y el listado de canciones a partir del que se crearan las recomendaciones
    Se calcula el pagerank con biblioteca.pagerank_personalizado y se
    concatena el resultado desde el pagerank segun el tipo y la cantidad
    Devuelve el resultado
    """
def recomendacion(grafo_u_c:Grafo, tipo, cantidad, listado:set):
    pagerank = biblioteca.pagerank_personalizado(grafo_u_c, listado)
    pagerank_ordenado = sorted(pagerank, key = pagerank.get, reverse = True)
    if tipo == "canciones":
        tipo = "cancion"
    else:
        tipo = "usuario"
    i = 0
    while grafo_u_c.tipo_vertice(pagerank_ordenado[i]) != tipo or pagerank_ordenado[i] in listado:
        i += 1
    resultado = pagerank_ordenado[i]
    cantidad -= 1
    i += 1
    while cantidad > 0 and i < len(pagerank_ordenado):
        if grafo_u_c.tipo_vertice(pagerank_ordenado[i]) == tipo and pagerank_ordenado[i] not in listado:
            resultado += "; " + pagerank_ordenado[i]
            cantidad -= 1
        i += 1
    return resultado


    """ Recibe el nombre el archivo
    Crea el grafo de canciones, a partir de cada linea del archivo agrega canciones al grafo
    Une cada cancion con el resto de su playlist
    Devuelve el grafo de canciones
    """
def creacion_grafo_canciones(nombre_archivo):
    grafo_canciones = Grafo(False)
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        archivo.readline()
        diccionario = {}
        for line in archivo:
            line = line.split("\t")
            cancion = line[ARCHIVO_CANCION] + " - " + line[ARCHIVO_AUTOR]
            usuario = line[ARCHIVO_USUARIO]
            grafo_canciones.agregar_vertice(cancion)
            if usuario not in diccionario:
                diccionario[usuario] = set()
            diccionario[usuario].add(cancion)
    for usuario in diccionario:
        lista = list(diccionario[usuario])
        for i in range (len(lista)-1):
            cancion1 = lista[i]
            for j in range(i+1, len(lista)):
                cancion2 = lista[j]
                grafo_canciones.agregar_arista(cancion1, cancion2)
    return grafo_canciones


    """Recibe el grafo, la cancion origen y el largo del ciclo
    Recurre a biblioteca.ciclo_n para encontrar el ciclo deseado
    Concatena el listado de canciones en el ciclo y devuelve el resultado
    """
def ciclo_de_n_canciones(grafo:Grafo, origen, largo):
    listado = biblioteca.ciclo_n(grafo, origen, largo)
    if len(listado) == 0:
        resultado = "No se encontro recorrido"
    else:
        resultado = listado[0]
        for i in range(1,len(listado)):
            resultado += " --> " + listado[i]
    return resultado


    """Funcion que engloba todas las funciones y trata con el parametro de entrada externo
    A partir de la creacion del grafo_u_c y posterior grafo_canciones, espera comandos por 
    entrada estandar, los separa correctamente el comando y sus demas parametros, que sirve
    para los argumentos de las funciones que devuelven los resultados
    e imprime un resultado por pantalla
    """
def main():
    if len(sys.argv) != LEN_ARGV:
        return
    nombre_archivo = sys.argv[RUTA_ARCHIVO]
    grafo_u_c = creacion_grafo_usuarios_canciones(nombre_archivo)
    grafo_canciones = False
    pagerank_canciones = []
    
    for line in sys.stdin:
        linea_separada = line.split()
        if linea_separada[STDIN_ORDEN] == "camino":
            resultado = comando_camino(linea_separada, grafo_u_c)
        elif linea_separada[STDIN_ORDEN] == "mas_importantes":
            cantidad = int(linea_separada[STDIN_MAS_IMPORTANTES_CANTIDAD])
            resultado = canciones_mas_importantes(grafo_u_c, pagerank_canciones, cantidad)
        elif linea_separada[STDIN_ORDEN] == "recomendacion":
            resultado = comando_recomendacion(linea_separada, grafo_u_c)
        else: 
            if not grafo_canciones:
                grafo_canciones = creacion_grafo_canciones(nombre_archivo)
            cantidad, origen = separacion_cantidad_origen(linea_separada)
            if linea_separada[STDIN_ORDEN] == "ciclo":
                resultado = ciclo_de_n_canciones(grafo_canciones, origen, cantidad)
            elif linea_separada[STDIN_ORDEN] == "rango":
                resultado = biblioteca.todos_en_rango_n(grafo_canciones, origen, cantidad)
            else:
                resultado = "Comando invalido"
        print(resultado)

if __name__ == "__main__":
    main()