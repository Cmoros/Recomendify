class Grafo:
    def __init__(self, dirigido):
        self.vertices = {}
        self.aristas = {}
        self.dirigido = dirigido

    def agregar_vertice(self, v, tipo = 1):
        if not self.vertices.get(v, False):
            self.vertices[v] = tipo
            self.aristas[v] = {}

    def borrar_vertice(self, v):
        self.vertices.pop(v)
        if (not self.dirigido):
            vertices_adyacentes = list(self.aristas[v].keys())
            for vertice in vertices_adyacentes:
                self.aristas[vertice].pop(v)
        else:
            for vertice in self.aristas:
                if self.aristas[vertice].get(v, False):
                    self.aristas[vertice].pop(v)
        self.aristas.pop(v)
    
    def agregar_arista(self, v1, v2, peso = 1):
        self.aristas[v1][v2] = peso
        if (not self.dirigido):
            self.aristas[v2][v1] = peso
            
    def borrar_arista(self, v1, v2):
        self.aristas[v1].pop(v2)
        if not self.dirigido:
            self.aristas[v2].pop(v1)

    def estan_unidos(self, v1, v2):
        return v2 in self.aristas[v1]
    
    def peso_arista(self, v1, v2):
        return self.aristas[v1].get(v2, None)

    def obtener_vertices(self):
        return list(self.vertices.keys())
    
    def adyacentes(self, v1):
        return list(self.aristas[v1].keys())
    
    def tipo_vertice(self, v1):
        return self.vertices[v1]