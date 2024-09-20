import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generar_matriz(n, aleatorio=True):
    # Matriz de adyacencia inicializada a ceros
    matriz = np.zeros((n, n), dtype=int)
    
    if aleatorio:
        for i in range(n):
            for j in range(n):
                if i != j:  # Evitar bucles (sin conexiones a sí mismo)
                    # Asignar un valor aleatorio entre 0 y 20 a la conexión
                    matriz[i, j] = np.random.randint(0, 21)  
    else:
        print("Introduce los valores de la matriz manualmente seleccionando vertices y conexiones.")
        for i in range(n):
            while True:
                try:
                    num_conexiones = int(input(f"¿Cuantas conexiones tendra el vertice {i + 1}? (0 a {n-1}): "))
                    if 0 <= num_conexiones <= n - 1:
                        break
                    else:
                        print(f"Por favor, ingresa un numero entre 0 y {n-1}.")
                except ValueError:
                    print("Por favor, ingresa un numero válido.")
            
            posibles_conexiones = list(range(n))
            posibles_conexiones.remove(i)  # Evitar conexiones a sí mismo (sin bucles)
            vertices_seleccionados = []  # Lista para almacenar los vertices ya seleccionados

            # Seleccionar los vertices con los que se conecta
            for _ in range(num_conexiones):
                while True:
                    try:
                        vertice_conexion = int(input(f"Selecciona el vertice de destino para el vertice {i + 1} (1 a {n}, excepto {i + 1}){', Vertices prohibidos: ' + str(vertices_seleccionados + [i + 1]) if vertices_seleccionados else ''}: ")) - 1
                        if vertice_conexion in posibles_conexiones:
                            posibles_conexiones.remove(vertice_conexion)  # Evitar elegir el mismo vertice dos veces
                            vertices_seleccionados.append(vertice_conexion + 1)  # Guardar el vertice seleccionado
                            break
                        else:
                            print(f"Vertice no permitido. Ya seleccionado o es el propio vertice {i + 1}.")
                    except ValueError:
                        print("Por favor, ingresa un numero valido.")

                while True:
                    try:
                        peso = int(input(f"Introduce el peso para la conexión {i + 1} -> {vertice_conexion + 1} (peso positivo): "))
                        if peso > 0:
                            matriz[i, vertice_conexion] = peso
                            break
                        else:
                            print("Por favor, ingresa un numero mayor que 0.")
                    except ValueError:
                        print("Por favor, ingresa un numero valido.")
    
    return matriz

def crear_grafo_desde_matriz(matriz):
    n = len(matriz)
    G = nx.DiGraph()  # Crear un grafo dirigido
    for i in range(n):
        for j in range(n):
            if matriz[i, j] > 0:  # Solo agregar arista si hay conexion (peso > 0)
                G.add_edge(i, j, weight=matriz[i, j])  # Añade arista con el peso como atributo 'weight'
    return G

def visualizar_grafo(G):
    pos = nx.spring_layout(G)  # Disposicion de los nodos para la visualizacion
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}  # Etiquetas con los pesos de las aristas

    # Dibujar nodos, aristas y etiquetas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold', arrows=True)
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
                print("Por favor, ingresa un numero entre 8 y 16.")
        except ValueError:
            print("Por favor, ingresa un numero valido.")
    
    modo = input("¿Deseas generar la matriz aleatoriamente? (s/n): ").strip().lower()
    matriz = generar_matriz(n, aleatorio=(modo == 's'))
    
    print("\nMatriz generada:")
    print(matriz)
    
    G = crear_grafo_desde_matriz(matriz)
    visualizar_grafo(G)

if __name__ == "__main__":
    main()
