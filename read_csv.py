from collections import defaultdict
import gc


def read_dimacs_with_gc(in_file):
    graph = defaultdict(list)
    line = in_file.readline().strip()
    while not line.startswith("p sp"):
        line = in_file.readline().strip()

    parts = line.split()
    n, m = int(parts[2]), int(parts[3])

    for _ in range(m):
        line = in_file.readline().strip()
        if line.startswith("a "):
            parts = line.split()
            u, v, w = int(parts[1]), int(parts[2]), int(parts[3])

            if v not in [adj[0] for adj in graph[u]]:
                graph[u].append((v, w))
            if u not in [adj[0] for adj in graph[v]]:
                graph[v].append((u, w))

        # Liberando memória manualmente a cada certo número de iterações
        if _ % 100000 == 0:  # Ajuste conforme necessário
            gc.collect()

    return graph, n, m
