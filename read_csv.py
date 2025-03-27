
from collections import defaultdict
from array import array

def read_dimacs(file_path):
    adj = defaultdict(lambda: array('I'))    # Lista de adjacência eficiente
    weights = defaultdict(lambda: array('I')) # Lista de pesos eficiente
    n = m = 0

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('p sp'):
                _, _, n, m = line.split()
                n, m = int(n), int(m)
            elif line.startswith('a'):
                _, u, v, w = line.split()
                u, v, w = int(u), int(v), int(w)
                adj[u].append(v)
                weights[u].append(w)

    return adj, weights, n, m


def print_graph(adj, weights, output_file):
    with open(output_file, 'w') as f:
        f.write("Grafo lido:\n")
        edge_count = 0
        for node in adj:
            if edge_count >= 5:
                break
            f.write(f"Node {node}: ")
            for i, v in enumerate(adj[node]):
                if edge_count >= 5:
                    break
                f.write(f"(to: {v}, weight: {weights[node][i]}) ")
                edge_count += 1
            f.write("\n")
