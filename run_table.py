import search
import time   # <-- AÑADIDO

# -------------------------------------------------
# Divide la ruta en varias líneas sin romper columnas
# -------------------------------------------------
def split_route(path_nodes, max_width=30):
    nodes = [f"<Node {n.state}>" for n in path_nodes]
    lines = []
    current = ""

    for n in nodes:
        if len(current) + len(n) + 2 <= max_width:
            current = n if not current else current + ", " + n
        else:
            lines.append(current)
            current = n

    if current:
        lines.append(current)

    formatted = ["Ruta: [" + lines[0]]
    for l in lines[1:-1]:
        formatted.append("      " + l)
    if len(lines) > 1:
        formatted.append("      " + lines[-1] + "]")
    else:
        formatted[0] += "]"

    return formatted

# -------------------------------------------------
# Ejecuta un algoritmo
# -------------------------------------------------
def run_experiment(origin, destination, search_func):
    problem = search.GPSProblem(origin, destination, search.romania)
    result_node, generated, visited = search_func(problem)

    if result_node:
        path_nodes = result_node.path()
        path_nodes.reverse()           # ORIGEN → DESTINO
        ruta_lines = split_route(path_nodes)
        costo = result_node.path_cost
    else:
        ruta_lines = ["Ruta: No solution"]
        costo = 0

    return {
        "Generados": f"Generados: {generated}",
        "Visitados": f"Visitados: {visited}",
        "Costo": f"Costo total: {costo}",
        "Ruta": ruta_lines
    }

# -------------------------------------------------
# Convierte datos en líneas de celda
# -------------------------------------------------
def cell(data):
    lines = [
        data["Generados"],
        data["Visitados"],
        data["Costo"]
    ]
    lines.extend(data["Ruta"])
    return lines

# -------------------------------------------------
# Encabezado
# -------------------------------------------------
def print_header():
    print("=" * 170)
    print(
        f"{'ID':<3} | {'Origen':<10} | {'Destino':<10} | "
        f"{'Amplitud':<35} | {'Profundidad':<35} | "
        f"{'Ramificación y Acotación':<35} | {'R&A con Subestimación':<35}"
    )
    print("=" * 170)

# -------------------------------------------------
# Imprime una fila completa sin romper la tabla
# -------------------------------------------------
def print_row(id, origen, destino, bfs, dfs, bb, astar):
    cols = [cell(bfs), cell(dfs), cell(bb), cell(astar)]
    max_lines = max(len(c) for c in cols)

    for c in cols:
        while len(c) < max_lines:
            c.append("")

    for i in range(max_lines):
        if i == 0:
            print(
                f"{id:<3} | {origen:<10} | {destino:<10} | "
                f"{cols[0][i]:<35} | {cols[1][i]:<35} | "
                f"{cols[2][i]:<35} | {cols[3][i]:<35}"
            )
        else:
            print(
                f"{'':<3} | {'':<10} | {'':<10} | "
                f"{cols[0][i]:<35} | {cols[1][i]:<35} | "
                f"{cols[2][i]:<35} | {cols[3][i]:<35}"
            )
    print("-" * 170)

# -------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------
start_time = time.time()

city_map = {
    'Oradea': 'O',
    'Arad': 'A',
    'Neamt': 'N',
    'Zerind': 'Z'
}

destination = 'B'
id = 1

print("\n=== PRÁCTICA 2: RESULTADOS DE BÚSQUEDA ===\n")
print_header()

for city_name, city_key in city_map.items():
    bfs = run_experiment(city_key, destination, search.breadth_first_graph_search)
    dfs = run_experiment(city_key, destination, search.depth_first_graph_search)
    bb  = run_experiment(city_key, destination, search.branch_and_bound_graph_search)
    ast = run_experiment(city_key, destination, search.astar_search)

    print_row(id, city_name, "Bucharest", bfs, dfs, bb, ast)
    id += 1

end_time = time.time()   #
print(f"\nTiempo total de búsqueda: {end_time - start_time:.4f} segundos")
