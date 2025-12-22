import search
import time

def run_experiment(origin, destination, algorithm_name, search_func, problem_instance=None):
    """
    Ejecuta un experimento y formatea la salida para la tabla.
    """
    if problem_instance is None:
        # Creamos el problema: ir desde 'origin' hasta 'Bucharest' (por defecto en el mapa)
        problem = search.GPSProblem(origin, destination, search.romania)
    else:
        problem = problem_instance

    start_time = time.time()
    
    # Ejecutamos la búsqueda (que ahora devuelve 3 valores)
    result_node, generated, visited = search_func(problem)
    
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000 # ms

    if result_node:
        path_nodes = result_node.path()
        path_nodes.reverse() # path() devuelve desde meta a raíz, lo invertimos
        path_str = " -> ".join([node.state for node in path_nodes])
        cost = result_node.path_cost
    else:
        path_str = "No solution"
        cost = 0

    return {
        "Origin": origin,
        "Algorithm": algorithm_name,
        "Generated": generated,
        "Visited": visited,
        "Path": path_str,
        "Cost": cost,
        "Time(ms)": f"{elapsed_time:.4f}"
    }

def print_header():
    print(f"{'Origin':<12} | {'Algorithm':<20} | {'Gen':<5} | {'Vis':<5} | {'Cost':<5} | {'Path'}")
    print("-" * 100)

def print_row(data):
    print(f"{data['Origin']:<12} | {data['Algorithm']:<20} | {data['Generated']:<5} | {data['Visited']:<5} | {data['Cost']:<5} | {data['Path']}")

# --- CONFIGURACIÓN DEL EXPERIMENTO ---

# Ciudades de origen para probar (según la tabla del PDF)
city_map = {
    'Oradea': 'O',
    'Arad': 'A',
    'Neamt': 'N',
    'Zerind': 'Z',
    'Bucharest': 'B'
}

# Ciudades de origen para probar (usando las claves del grafo: O, A, N, Z)
cities_to_test = ['O', 'A', 'N', 'Z'] 
destination = 'B' # 'B' es Bucharest

print("\n=== PRÁCTICA 2: RESULTADOS DE BÚSQUEDA ===\n")
print_header()

for city_key in cities_to_test:
    # Para mostrar el nombre completo en la tabla si quieres, o usa la clave directamente
    display_name = [name for name, key in city_map.items() if key == city_key][0]
    
    # 1. Anchura (BFS)
    data = run_experiment(display_name, destination, "Anchura (BFS)", search.breadth_first_graph_search, 
                          problem_instance=search.GPSProblem(city_key, destination, search.romania))
    print_row(data)

    # 2. Profundidad (DFS)
    data = run_experiment(display_name, destination, "Profundidad (DFS)", search.depth_first_graph_search,
                          problem_instance=search.GPSProblem(city_key, destination, search.romania))
    print_row(data)

    # 3. Ramificación y Acotación
    data = run_experiment(display_name, destination, "Ramif. y Acot.", search.branch_and_bound_graph_search,
                          problem_instance=search.GPSProblem(city_key, destination, search.romania))
    print_row(data)

    # 4. A*
    data = run_experiment(display_name, destination, "A* (R&A con Sub.)", search.astar_search,
                          problem_instance=search.GPSProblem(city_key, destination, search.romania))
    print_row(data)
    
    print("-" * 100)

print("\nNOTA: 'Gen' = Nodos Generados, 'Vis' = Nodos Visitados (Expandidos)")