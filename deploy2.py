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
        self.step_state = 0  # Controlar la etapa de visualización (0: exploración, 1: visualización completa)
        self.remaining_path = []  # Para visualizar paso a paso las aristas del camino
        self.fig, self.ax = plt.subplots()  # Crear figura y ejes aquí
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
                # Verifica si hay capacidad residual
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True

        return False

    # Método principal para ejecutar el algoritmo Ford-Fulkerson paso a paso
    def ford_fulkerson_step_by_step(self):
        self.paths = []

        # Mientras exista un camino con capacidad residual
        while self.bfs(self.source, self.sink, self.parent):
            path_flow = float("Inf")
            s = self.sink
            path = []
            
            # Encontrar el flujo máximo en el camino encontrado por BFS
            while s != self.source:
                path_flow = min(path_flow, self.graph[self.parent[s]][s])
                path.insert(0, (self.parent[s], s))  # Guardar el camino
                s = self.parent[s]

            # Actualizar la lista de caminos y flujo total
            self.paths.append((path, path_flow))
            self.flow += path_flow

            # Actualizar las capacidades residuales
            v = self.sink
            while v != self.source:
                u = self.parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow  # Añadir capacidad en la dirección opuesta (grafo residual)
                v = self.parent[v]

        self.max_flow = self.flow
        self.current_path = None  # Reiniciar el camino actual

    # Visualización inicial del grafo
    def init_visualization(self):
        self.ax.clear()  # Limpiar el gráfico en lugar de crear uno nuevo
        self.pos = nx.spring_layout(self.G, k=5.5)  # Aumentar el valor de k para más dispersión
        plt.title("Red de flujo (Ford-Fulkerson)")
        self.draw_graph()

    # Dibujar el grafo y mostrar capacidades y flujos
    def draw_graph(self, current_edge=None):
        edge_colors = []
        edge_labels = {}

        for u, v, d in self.G.edges(data=True):
            if self.current_path is not None and (u, v) in self.current_path:
                edge_colors.append("blue")  # Camino completo
            elif (u, v) in self.remaining_path:
                edge_colors.append("green")  # Camino actual parcial
            elif d['flow'] == d['capacity']:
                edge_colors.append("red")  # Arista saturada
            else:
                edge_colors.append("black")  # Arista normal

            edge_labels[(u, v)] = f"{d['flow']}/{d['capacity']}"

        # Colorear el nodo fuente y sumidero
        node_colors = ['blue' if node == self.source else 'red' if node == self.sink else 'gray' for node in self.G.nodes()]

        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=700, font_size=10, font_color='white', ax=self.ax)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Mostrar el flujo máximo si hemos terminado
        if not self.paths and self.max_flow == 0:
            self.ax.set_title("No existe conexión entre el nodo de inicio y el final")
        elif not self.paths and self.max_flow > 0 and self.remaining_path == []:
            self.ax.set_title(f"Flujo máximo: {self.max_flow}")
            plt.suptitle("")  # Limpiar el subtítulo después de terminar todo
        elif current_edge:  # Si estamos en medio de una iteración, mostrar el camino actual
            self.ax.set_title(f"Red de flujo (Ford-Fulkerson)")
            plt.suptitle(f"Camino actual: {current_edge[0]} -> {current_edge[1]}")
        else:
            plt.suptitle("Enviando flujo")  # Limpiar el subtítulo cuando no hay un camino activo

        self.fig.canvas.draw_idle()  # Actualizar la figura

    # Avanzar al siguiente paso del flujo
    def next_step(self, event):
        # Si no quedan caminos ni aristas en el camino actual, mostramos el flujo máximo
        if not self.paths and not self.remaining_path:
            # En caso de que haya un camino pendiente pero no se haya actualizado el flujo, lo hacemos aquí
            if self.current_path is not None:
                for u, v in self.current_path:
                    self.G[u][v]['flow'] += self.current_flow
                    if self.G.has_edge(v, u):
                        self.G[v][u]['flow'] -= self.current_flow
                print(f"Flujo enviado en este camino: {self.current_flow}")
                self.current_path = None
                self.remaining_path = []
                self.step_state = 0
                self.draw_graph()

            print(f"Flujo máximo: {self.max_flow}")
            self.ax.set_title(f"Flujo máximo: {self.max_flow}")
            plt.suptitle("")  # Limpiar el subtítulo solo después de la última actualización
            return

        if self.step_state == 0:
            if not self.remaining_path:  # Comenzar con un nuevo camino
                path, path_flow = self.paths.pop(0)
                self.current_path = path
                self.current_flow = path_flow
                self.remaining_path = path.copy()  # Guardar copia del camino actual
                print(f"Camino utilizado: {' -> '.join(str(u) for u, _ in path)}")

            # Dibujar el siguiente paso del camino
            if self.remaining_path:
                current_edge = self.remaining_path.pop(0)  # Quitar una arista del camino actual
                self.draw_graph(current_edge)  # Mostrar la arista actual
                if not self.remaining_path:  # Si el camino está completo, pasamos a la siguiente etapa
                    self.step_state = 1
            else:
                self.draw_graph()

        elif self.step_state == 1:  # Actualizar el flujo y mostrar el camino final
            # Actualizar el grafo de NetworkX con el flujo del camino completo
            for u, v in self.current_path:
                self.G[u][v]['flow'] += self.current_flow
                if self.G.has_edge(v, u):
                    self.G[v][u]['flow'] -= self.current_flow

            print(f"Flujo enviado en este camino: {self.current_flow}")
            self.step_state = 0  # Volver al estado de exploración
            self.current_path = None
            self.remaining_path = []
            self.draw_graph()

# Definir tamaño de la matriz, fuente y sumidero
matrix_size = 8
source = 0
sink = matrix_size - 1

# Generar una matriz de adyacencia aleatoria de 16x16 con conexiones limitadas
np.random.seed(55)  # Para tener resultados reproducibles (opcional)

# Generamos una matriz de adyacencia aleatoria, pero con pocas conexiones (probabilidad del 30%)
graph = np.random.randint(0, 21, size=(matrix_size, matrix_size))  # Capacidades aleatorias entre 0 y 20
np.fill_diagonal(graph, 0)  # No permitir bucles en el grafo

# Asegurar que el grafo sea dirigido y unidireccional
for i in range(matrix_size):
    for j in range(i+1, matrix_size):  # Solo revisar la mitad superior de la matriz
        if np.random.rand() < 0.5:  # 50% de probabilidad de eliminar una dirección
            graph[j][i] = 0  # Eliminar la conexión de j -> i
        else:
            graph[i][j] = 0  # Eliminar la conexión de i -> j

# Asegurar que no haya conexión directa entre el nodo de inicio y el nodo de fin
graph[source][sink] = 0

# Crear instancia del grafo
graph_vis = GraphVisualization(graph, source, sink)

# Ejecutar el algoritmo Ford-Fulkerson paso a paso
graph_vis.ford_fulkerson_step_by_step()

# Crear botón en la misma figura
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075], figure=graph_vis.fig)
button = Button(ax_button, 'Siguiente')
button.on_clicked(graph_vis.next_step)

# Mostrar visualización inicial
graph_vis.init_visualization()
plt.show()
