import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from tkinter import Tk, simpledialog, messagebox

class GraphVisualization:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph)
        self.G = nx.DiGraph()
        self.source = None
        self.sink = None
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
        self.G.clear()
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
        self.draw_graph()

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

    def add_edges_manually(self, vertex_count):
        self.graph = np.zeros((vertex_count, vertex_count))
        self.n = vertex_count
        root = Tk()
        root.withdraw()
        while True:
            source = simpledialog.askinteger("Agregar arista", f"Ingrese el nodo de origen (0-{vertex_count-1}) (o -1 para terminar):")
            if source == -1 or source is None:
                break
            target = simpledialog.askinteger("Agregar arista", f"Ingrese el nodo de destino (0-{vertex_count-1}):")
            if target is None or target == -1:
                break
            capacity = simpledialog.askinteger("Agregar arista", "Ingrese la capacidad de la arista (1-20):", minvalue=1, maxvalue=20)
            if capacity is None:
                break
            self.graph[source][target] = capacity
        root.destroy()
        self.build_graph()
        self.init_visualization()

    def select_source_sink(self):
        root = Tk()
        root.withdraw()
        while True:
            source = simpledialog.askinteger("Nodo de Inicio", f"Seleccione el nodo fuente (0 - {self.n - 1}):")
            sink = simpledialog.askinteger("Nodo Final", f"Seleccione el nodo sumidero (0 - {self.n - 1}):")
            if source is None or sink is None:
                break
            if source == sink:
                messagebox.showerror("Error", "El nodo fuente y sumidero no pueden ser el mismo.")
                continue
            elif self.graph[source][sink] > 0:
                messagebox.showerror("Error", "El nodo fuente y sumidero no pueden estar conectados directamente.")
                continue
            self.source = source
            self.sink = sink
            break
        root.destroy()

    def delete_graph(self, event):
        root = Tk()
        root.withdraw()
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas borrar el grafo actual?"):
            self.graph = np.zeros((self.n, self.n))
            self.build_graph()
            self.init_visualization()
        root.destroy()

    def add_vertex(self, event):
        self.n += 1
        self.graph = np.pad(self.graph, ((0, 1), (0, 1)), 'constant', constant_values=0)
        self.build_graph()
        self.init_visualization()

def show_menu():
    root = Tk()
    root.withdraw()
    vertex_count = simpledialog.askinteger("Cantidad de vértices", "Ingrese el número de vértices (mínimo 2):", minvalue=2)
    if vertex_count is None:
        exit()
    return vertex_count

vertex_count = show_menu()
graph_vis = GraphVisualization(np.zeros((vertex_count, vertex_count)))

def add_edges(event):
    graph_vis.add_edges_manually(vertex_count)

def start_ford_fulkerson(event):
    if graph_vis.source is None or graph_vis.sink is None:
        graph_vis.select_source_sink()
    if graph_vis.source is not None and graph_vis.sink is not None:
        graph_vis.ford_fulkerson_step_by_step()

def show_graph(event):
    graph_vis.init_visualization()

ax_button_add = plt.axes([0.15, 0.05, 0.15, 0.075], figure=graph_vis.fig)
button_add = Button(ax_button_add, 'Agregar Conexiones')
button_add.on_clicked(add_edges)

ax_button_show = plt.axes([0.35, 0.05, 0.15, 0.075], figure=graph_vis.fig)
button_show = Button(ax_button_show, 'Mostrar Grafo')
button_show.on_clicked(show_graph)

ax_button_delete = plt.axes([0.55, 0.05, 0.15, 0.075], figure=graph_vis.fig)
button_delete = Button(ax_button_delete, 'Borrar Grafo')
button_delete.on_clicked(graph_vis.delete_graph)

ax_button_add_vertex = plt.axes([0.75, 0.05, 0.15, 0.075], figure=graph_vis.fig)
button_add_vertex = Button(ax_button_add_vertex, 'Agregar Vértice')
button_add_vertex.on_clicked(graph_vis.add_vertex)

ax_button_start = plt.axes([0.95, 0.05, 0.15, 0.075], figure=graph_vis.fig)
button_start = Button(ax_button_start, 'Iniciar Algoritmo')
button_start.on_clicked(start_ford_fulkerson)

graph_vis.init_visualization()
plt.show()
