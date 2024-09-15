import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generar_matriz(n, aleatorio=True):
    matriz = np.zeros((n, n), dtype=int)
    if aleatorio:
        for i in range(n):
            # Determinar al azar cuántas conexiones tendrá el nodo (1 o 2)
            num_conexiones = np.random.choice([1, 2], p=[0.7, 0.3])  # Mayor probabilidad de tener 1 conexión
            posibles_conexiones = list(range(n))
            posibles_conexiones.remove(i)  # Evitar bucles (sin conexiones a sí mismo)
            conexiones = np.random.choice(posibles_conexiones, size=num_conexiones, replace=False)
            for j in conexiones:
                matriz[i, j] = np.random.randint(1, 21)  # Asignar un valor aleatorio entre 1 y 20 a la conexión
    else:
        print("Introduce los valores de la matriz (valores enteros positivos, sin bucles):")
        for i in range(n):
            for j in range(n):
                if i != j:  # Evitar bucles (diagonal con ceros)
                    while True:
                        try:
                            valor = int(input(f"Elemento [{i+1},{j+1}]: "))
                            if valor >= 0:
                                matriz[i, j] = valor
                                break
                            else:
                                print("Por favor, ingresa un número entero no negativo.")
                        except ValueError:
                            print("Por favor, ingresa un número válido.")
    return matriz

def crear_grafo_desde_matriz(matriz):
    n = len(matriz)
    G = nx.DiGraph()  # Grafo dirigido
    for i in range(n):
        for j in range(n):
            if matriz[i, j] > 0:  # Solo agrega arista si el valor es mayor que 0
                G.add_edge(i, j, weight=matriz[i, j])  # Añade el peso como atributo 'weight'
    return G

def visualizar_grafo(G):
    pos = nx.spring_layout(G)  # Posicionamiento del grafo
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}  # Etiquetas de peso

    # Dibujar nodos y aristas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold', arrows=True)
    
    # Dibujar etiquetas de las aristas (peso)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.6, edge_color='black', arrows=True)
    
    plt.show()

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

if __name__ == "__main__":
    main()
