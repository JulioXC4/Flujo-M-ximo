import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

# Paso 1: Crear la matriz de adyacencia para un grafo de 4x4
np.random.seed(42)  # Fijar semilla para reproducibilidad
capacity_matrix = np.random.randint(1, 10, size=(4, 4))  # Matriz aleatoria de capacidades entre 1 y 9
capacity_matrix[np.tril_indices(4)] = 0  # No permitimos flujo en la diagonal ni debajo de ella (grafo dirigido)

print("Matriz de capacidades:\n", capacity_matrix)

# Crear el grafo a partir de la matriz de capacidades
G = nx.DiGraph()

for i in range(4):
    for j in range(4):
        if capacity_matrix[i, j] > 0:
            G.add_edge(i, j, capacity=capacity_matrix[i, j], flow=0)  # Flujo inicial en cero

# Posición de los nodos para visualización
pos = nx.spring_layout(G)

# Función auxiliar para realizar DFS en el grafo residual y encontrar un camino de aumento
def dfs_find_path(residual_G, source, sink, path, visited):
    if source == sink:
        return path
    visited.add(source)
    
    for neighbor in residual_G[source]:
        capacity = residual_G[source][neighbor]['capacity']
        if neighbor not in visited and capacity > 0:
            result = dfs_find_path(residual_G, neighbor, sink, path + [(source, neighbor)], visited)
            if result:
                return result
    return None

# Implementación del algoritmo de Ford-Fulkerson usando DFS
class FordFulkersonVisualizer:
    def __init__(self, G, source, sink):
        self.G = G
        self.source = source
        self.sink = sink
        self.residual_G = G.copy()  # Grafo residual
        self.max_flow = 0
        self.iteration = 0
        self.paths = []
        self.path_flows = []
        self.current_index = 0
        self.generate_paths()
        
        # Inicializar la visualización
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)
        
        # Botón para avanzar a la siguiente iteración
        self.ax_forward = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.btn_forward = Button(self.ax_forward, 'Forward')
        self.btn_forward.on_clicked(self.next_iteration)
        
        # Dibujar la primera iteración
        self.plot_flow_graph()
        
    def generate_paths(self):
        # Generar todos los caminos de aumento y actualizaciones de flujo
        while True:
            visited = set()
            path = dfs_find_path(self.residual_G, self.source, self.sink, [], visited)
            if path is None:
                break  # No hay más caminos aumentantes, terminamos el algoritmo
            
            # Encontrar la capacidad mínima en el camino aumentante
            path_flow = min(self.residual_G[u][v]['capacity'] for u, v in path)
            self.max_flow += path_flow
            self.paths.append(path)
            self.path_flows.append(path_flow)
            
            # Actualizar las capacidades residuales y los flujos en el grafo original y residual
            for u, v in path:
                self.G[u][v]['flow'] += path_flow  # Aumentar el flujo en el grafo original
                self.residual_G[u][v]['capacity'] -= path_flow  # Reducir la capacidad residual
                if self.residual_G[u][v]['capacity'] == 0:
                    self.residual_G.remove_edge(u, v)  # Eliminar la arista si está saturada
        
    def plot_flow_graph(self):
        self.ax.clear()
        path = self.paths[self.current_index] if self.current_index < len(self.paths) else []
        path_flow = self.path_flows[self.current_index] if self.current_index < len(self.path_flows) else 0
        edge_colors = []
        edge_labels = {}
        
        for u, v in self.G.edges():
            capacity = self.G[u][v]['capacity']
            flow = self.G[u][v]['flow']
            edge_labels[(u, v)] = f'{capacity}, {flow}'  # Mostrar capacidad y flujo como "capacidad, flujo"
            
            if (u, v) in path:
                edge_colors.append('green')  # Resaltar el camino aumentante en verde
            elif flow == capacity:
                edge_colors.append('red')  # Resaltar las aristas saturadas en rojo
            else:
                edge_colors.append('black')
        
        # Colorear nodos: fuente y sumidero
        node_colors = ['lightblue'] * len(self.G.nodes())
        node_colors[self.source] = 'yellow'  # Nodo fuente en amarillo
        node_colors[self.sink] = 'orange'   # Nodo sumidero en naranja
        
        # Dibujar el grafo
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=10, font_weight='bold', 
                edge_color=edge_colors, width=2, arrows=True, ax=self.ax)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax)
        
        title = f"Iteración {self.current_index + 1}: Flujo aumentante = {path_flow} (Flujo máximo acumulado = {self.max_flow})"
        self.ax.set_title(title)
        self.fig.canvas.draw()
    
    def next_iteration(self, event):
        if self.current_index < len(self.paths) - 1:
            self.current_index += 1
            self.plot_flow_graph()

# Función para pedir los nodos de inicio y fin
def elegir_nodos():
    while True:
        try:
            source = int(input("Elige el nodo de inicio (0 a 3): "))
            sink = int(input("Elige el nodo de fin (0 a 3): "))
            if 0 <= source <= 3 and 0 <= sink <= 3 and source != sink:
                return source, sink
            else:
                print("Error: el nodo de inicio y fin deben ser diferentes y estar entre 0 y 3.")
        except ValueError:
            print("Error: por favor, ingresa un número válido.")

# Elegir nodos de inicio y fin
source, sink = elegir_nodos()

# Crear el visualizador y ejecutar Ford-Fulkerson
ff_visualizer = FordFulkersonVisualizer(G, source, sink)
plt.show()

print(f"Flujo máximo desde el nodo {source} al nodo {sink}: {ff_visualizer.max_flow}")

