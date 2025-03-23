import time
import gc

def read_dimacs(in_file):
    """Lê um grafo DIMACS de forma eficiente e evita consumo excessivo de memória."""

    # 🔥 1. Força a liberação de memória antes de começar
    gc.collect()
    graph = {}  # Dicionário para lista de adjacências
    n, m = 0, 0  # Número de nós e arestas

    start_time = time.time()

    for line in in_file:
        if line.startswith("p sp"):
            _, _, n, m = line.split()
            n, m = int(n), int(m)

        elif line.startswith("a"):
            _, u, v, w = line.split()
            u, v, w = int(u), int(v), int(w)

            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))

        # 🔥 2. Libera memória periodicamente para evitar picos
        if len(graph) % 100000 == 0:
            gc.collect()

    end_time = time.time()
    elapsed_time = end_time - start_time

    with open("tempo_leitura.txt", "w") as log_file:
        log_file.write(f"Tempo de leitura do grafo: {elapsed_time:.4f} segundos\n")

    return graph, n, m
