import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

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
        self.step_state = 0
        self.remaining_path = []
        self.fig, self.ax = plt.subplots()
        self.init_visualization()

    def build_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.graph[i][j] > 0:
                    self.G.add_edge(i, j, capacity=self.graph[i][j], flow=0)

    def bfs(self, s, t, parent):
        visited = [False] * self.n
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)

            for v in range(self.n):
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True

        return False

    def ford_fulkerson_step_by_step(self):
        self.paths = []

        while self.bfs(self.source, self.sink, self.parent):
            path_flow = float("Inf")
            s = self.sink
            path = []

            while s != self.source:
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                path.insert(0, (self.parent[s], s))
                s = self.parent[s]

            self.paths.append((path, path_flow))
            self.flow += path_flow

            v = self.sink
            while v != self.source:
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = self.parent[v]

        self.max_flow = self.flow
        self.current_path = None

    def init_visualization(self):
        self.ax.clear()
        self.pos = nx.spring_layout(self.G, k=5.5)
        plt.title("Red de flujo (Ford-Fulkerson)")
        self.draw_graph()

    def draw_graph(self, current_edge=None):
        edge_colors = []
        edge_labels = {}

        for u, v, d in self.G.edges(data=True):
            if self.current_path is not None and (u, v) in self.current_path:
                edge_colors.append("blue")
            elif (u, v) in self.remaining_path:
                edge_colors.append("green")
            elif d['flow'] == d['capacity']:
                edge_colors.append("red")
            else:
                edge_colors.append("black")

            edge_labels[(u, v)] = f"{d['flow']}/{d['capacity']}"

        node_colors = ['blue' if node == self.source else 'red' if node == self.sink else 'gray' for node in self.G.nodes()]

        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=10, font_color='white', ax=self.ax)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        if not self.paths and self.max_flow == 0:
            self.ax.set_title("No existe conexión entre el nodo de inicio y el final")
        elif not self.paths and self.max_flow > 0 and self.remaining_path == []:
            self.ax.set_title(f"Flujo máximo: {self.max_flow}")
            plt.suptitle("")
        elif current_edge:
            self.ax.set_title(f"Red de flujo (Ford-Fulkerson)")
            plt.suptitle(f"Camino actual: {current_edge[0]} -> {current_edge[1]}")
        else:
            plt.suptitle("Enviando flujo")

        self.fig.canvas.draw_idle()

    def next_step(self, event):
        if not self.paths and not self.remaining_path:
            if self.current_path is not None:
                for u, v in self.current_path:
                    self.G[u][v]['flow'] += self.current_flow
                    if self.G.has_edge(v, u):
                        self.G[v][u]['flow'] -= self.current_flow
                self.current_path = None
                self.remaining_path = []
                self.step_state = 0
                self.draw_graph()

            self.ax.set_title(f"Flujo máximo: {self.max_flow}")
            plt.suptitle("")
            return

        if self.step_state == 0:
            if not self.remaining_path:
                path, path_flow = self.paths.pop(0)
                self.current_path = path
                self.current_flow = path_flow
                self.remaining_path = path.copy()

            if self.remaining_path:
                current_edge = self.remaining_path.pop(0)
                self.draw_graph(current_edge)

                if not self.remaining_path:
                    self.step_state = 1
            else:
                self.draw_graph()

        elif self.step_state == 1:
            for u, v in self.current_path:
                self.G[u][v]['flow'] += self.current_flow
                if self.G.has_edge(v, u):
                    self.G[v][u]['flow'] -= self.current_flow

            self.step_state = 0
            self.current_path = None
            self.remaining_path = []
            self.draw_graph()

matrix_size = int(input("Elige el tamaño de la matriz (8-16): "))
source = 0
sink = matrix_size - 1

while matrix_size < 8 or matrix_size > 16:
    print("Tamaño no válido. Debe estar entre 8 y 16.")
    matrix_size = int(input("Elige el tamaño de la matriz (8-16): "))

# Preguntar si se desea una matriz generada manualmente o aleatoriamente
manual = input("¿Deseas agregar las conexiones manualmente? (si/no): ").strip().lower() == "si"

if manual:
    graph = np.zeros((matrix_size, matrix_size), dtype=int)
    print("Ingresa las conexiones y capacidades (deja vacío para terminar):")
    available_nodes = [i for i in range(matrix_size)]  # Incluir todos los nodos
    print(f"Puedes conectar entre los nodos disponibles: {available_nodes}")
    while True:
        u = input("Nodo de inicio: ")
        if u == "":
            break
        v = input("Nodo de destino: ")
        if v == "":
            break
        u, v = int(u), int(v)

        # Validar que la conexión no sea directa entre fuente y sumidero, y que los nodos sean válidos
        if (u == source and v == sink) or u < 0 or u >= matrix_size or v < 0 or v >= matrix_size:
            print("Conexión no permitida. Intenta otra vez.")
            continue

        capacity = int(input(f"Capacidad de nodo {u} a nodo {v}: "))
        graph[u][v] = capacity

else:
    # Generar matriz aleatoria con algunas conexiones
    np.random.seed(42)
    graph = np.random.randint(0, 21, size=(matrix_size, matrix_size))
    np.fill_diagonal(graph, 0)  # No permitir bucles en el grafo
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size):
            if np.random.rand() < 0.5:
                graph[j][i] = 0
            else:
                graph[i][j] = 0
    graph[source][sink] = 0  # No permitir conexión directa entre el nodo de inicio y fin

graph_vis = GraphVisualization(graph, source, sink)
graph_vis.ford_fulkerson_step_by_step()

ax_button = plt.axes([0.4, 0.05, 0.2, 0.075], figure=graph_vis.fig)
button = Button(ax_button, 'Siguiente')
button.on_clicked(graph_vis.next_step)

graph_vis.init_visualization()
plt.show()
