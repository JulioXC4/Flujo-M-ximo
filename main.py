""" import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo dirigido
G = nx.DiGraph()

# Añadir nodos y aristas con capacidades
G.add_edge('A', 'B', capacity=10)
G.add_edge('A', 'C', capacity=15)
G.add_edge('B', 'D', capacity=10)
G.add_edge('C', 'D', capacity=10)
G.add_edge('C', 'E', capacity=5)
G.add_edge('D', 'E', capacity=10)

# Definir la fuente (origen) y el sumidero (destino)
source = 'A'
sink = 'E'

# Calcular el flujo máximo usando el algoritmo de Ford-Fulkerson (implementado en NetworkX)
flow_value, flow_dict = nx.maximum_flow(G, source, sink)

# Mostrar el flujo máximo
print(f"El flujo máximo desde {source} hasta {sink} es: {flow_value}")

# Dibujar el grafo con los flujos
pos = nx.spring_layout(G)
edge_labels = {(u, v): f"{d['capacity']} | {flow_dict[u][v]}" for u, v, d in G.edges(data=True)}

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.6, edge_color='black')

plt.title(f"Flujo máximo: {flow_value} de {source} a {sink}")
plt.show()
 """
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def generar_matriz(n, aleatorio=True):
    if aleatorio:
        matriz = np.random.randint(1, 21, size=(n, n))
    else:
        matriz = np.zeros((n, n), dtype=int)
        print("Introduce los valores de la matriz (valores enteros positivos):")
        for i in range(n):
            for j in range(n):
                while True:
                    try:
                        valor = int(input(f"Elemento [{i+1},{j+1}]: "))
                        if valor > 0:
                            matriz[i, j] = valor
                            break
                        else:
                            print("Por favor, ingresa un número entero positivo.")
                    except ValueError:
                        print("Por favor, ingresa un número válido.")
    return matriz

def crear_grafo_desde_matriz(matriz):
    n = len(matriz)
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if matriz[i, j] > 0:
                G.add_edge(i, j, capacity=matriz[i, j])
    return G

def visualizar_grafo(G, flow_dict=None):
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['capacity']}" for u, v, d in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.6, edge_color='black')
    
    if flow_dict:
        flow_labels = {(u, v): f"{flow_dict[u][v]}" for u, v in flow_dict.items() if flow_dict[u][v] > 0}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=flow_labels, font_color='red', font_size=12)
    
    plt.show()

def calcular_flujo_maximo(G, source, sink):
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)
    print(f"\nEl flujo máximo desde {source} hasta {sink} es: {flow_value}")
    visualizar_grafo(G, flow_dict)

def main():
    while True:
        try:
            n = int(input("Ingresa el tamaño de la matriz (entre 8 y 16): "))
            if 8 <= n <= 16:
                break
            else:
                print("Por favor, ingresa un número entre 8 y 16.")
        except ValueError:
            print("Por favor, ingresa un número válido.")
    
    modo = input("¿Deseas generar la matriz aleatoriamente? (s/n): ").strip().lower()
    matriz = generar_matriz(n, aleatorio=(modo == 's'))
    
    print("\nMatriz generada:")
    print(matriz)
    
    G = crear_grafo_desde_matriz(matriz)
    visualizar_grafo(G)
    
    while True:
        try:
            source = int(input(f"Selecciona el nodo fuente (0 a {n-1}): "))
            sink = int(input(f"Selecciona el nodo sumidero (0 a {n-1}): "))
            if 0 <= source < n and 0 <= sink < n and source != sink:
                break
            else:
                print(f"Por favor, selecciona nodos válidos (entre 0 y {n-1}) y que no sean iguales.")
        except ValueError:
            print("Por favor, ingresa números válidos.")
    
    calcular_flujo_maximo(G, source, sink)

if __name__ == "__main__":
    main()
