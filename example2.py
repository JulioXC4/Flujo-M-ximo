import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Clase para crear el grafo y manejar el algoritmo Ford-Fulkerson
class GraphVisualization:
    def __init__(self, graph, source, sink):
        self.graph = graph
        self.n = len(graph)
        self.G = nx.DiGraph()
        self.source = source
        self.sink = sink
        self.pos = None
        self.flow = 0
        self.max_flow = 0
        self.parent = [-1] * self.n
        self.build_graph()
        self.paths = []
        self.current_path = None
        self.current_flow = 0
        self.init_visualization()

    # Construir el grafo a partir de la matriz de adyacencia
    def build_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.graph[i][j] > 0:
                    self.G.add_edge(i, j, capacity=self.graph[i][j], flow=0)

    # Realiza BFS para encontrar un camino con capacidad residual
    def bfs(self, s, t, parent):
        visited = [False] * self.n
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v in range(self.n):
                if visited[v] == False and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True

        return False

    # Método principal para ejecutar el algoritmo Ford-Fulkerson paso a paso
    def ford_fulkerson_step_by_step(self):
        self.paths = []

        while self.bfs(self.source, self.sink, self.parent):
            path_flow = float("Inf")
            s = self.sink
            path = []
            
            while s != self.source:
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                path.insert(0, (self.parent[s], s))  # Guardar el camino
                s = self.parent[s]
            
            self.paths.append((path, path_flow))
            self.flow += path_flow

            # Actualizar las capacidades residuales
            v = self.sink
            while v != self.source:
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = self.parent[v]

        self.max_flow = self.flow
        self.current_path = None  # Reiniciar el camino actual

    # Visualización inicial del grafo
    def init_visualization(self):
        plt.clf()  # Limpiar la figura
        self.pos = nx.spring_layout(self.G)  # Layout para la visualización
        plt.title("Red de flujo (Ford-Fulkerson)")
        self.draw_graph()

    # Dibujar el grafo y mostrar capacidades y flujos
    def draw_graph(self):
        edge_colors = []
        edge_labels = {}

        for u, v, d in self.G.edges(data=True):
            # Si no hay camino actual, coloreamos todas las aristas en negro
            if self.current_path is not None and (u, v) in self.current_path:
                edge_colors.append("green")  # Camino actual
            elif d['flow'] == d['capacity']:
                edge_colors.append("red")  # Arista saturada
            else:
                edge_colors.append("black")  # Arista normal

            edge_labels[(u, v)] = f"{d['flow']}/{d['capacity']}"

        # Colorear el nodo fuente y sumidero
        node_colors = ['blue' if node == self.source else 'red' if node == self.sink else 'gray' for node in self.G.nodes()]

        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=10, font_color='white')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels)

        plt.draw()
    # Avanzar al siguiente paso del flujo
    def next_step(self, event):
        if not self.paths:
            print(f"Flujo máximo: {self.max_flow}")
            plt.title(f"Flujo máximo: {self.max_flow}")
            return

        path, path_flow = self.paths.pop(0)
        self.current_path = path
        self.current_flow = path_flow

        # Actualizar el grafo de NetworkX
        for u, v in path:
            self.G[u][v]['flow'] += path_flow
            if self.G.has_edge(v, u):
                self.G[v][u]['flow'] -= path_flow

        self.draw_graph()

# Crear el grafo y ejecutar la visualización
graph = [[0, 16, 13, 0, 0, 0],
         [0, 0, 10, 12, 0, 0],
         [0, 4, 0, 0, 14, 0],
         [0, 0, 9, 0, 0, 20],
         [0, 0, 0, 7, 0, 4],
         [0, 0, 0, 0, 0, 0]]

source = 0
sink = 5

# Crear instancia del grafo
graph_vis = GraphVisualization(graph, source, sink)

# Ejecutar el algoritmo Ford-Fulkerson paso a paso
graph_vis.ford_fulkerson_step_by_step()

# Configurar el botón para avanzar paso a paso
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

# Crear botón
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
button = Button(ax_button, 'Siguiente')
button.on_clicked(graph_vis.next_step)

# Mostrar visualización inicial
graph_vis.init_visualization()
plt.show()