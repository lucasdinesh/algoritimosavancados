import psutil
from array import array

def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss  # Em bytes

def read_dimacs(file_path):
    adj = []      # Lista de adjacências usando array('I')
    weights = []  # Lista de pesos usando array('I')
    n = m = 0

    # Mostra a memória usada antes de iniciar a leitura
    memory_before = get_memory_usage()
    print(f"Memória antes de ler o grafo: {memory_before / (1024 ** 2):.2f} MB")

    # Primeira leitura para descobrir o número de vértices
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('p sp'):
                _, _, n, m = line.split()
                n, m = int(n), int(m)
                adj = [array('I') for _ in range(n)]  # Inicializa arrays vazios para adjacências
                weights = [array('I') for _ in range(n)]  # Inicializa arrays vazios para pesos
                break  # Não precisa continuar procurando

    # Segunda leitura para processar as arestas
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('a'):
                _, u, v, w = line.split()
                u, v, w = int(u) - 1, int(v) - 1, int(w)  # Convertendo para índice base 0
                adj[u].append(v)
                weights[u].append(w)

    # Mostra a memória usada depois de carregar o grafo
    memory_after = get_memory_usage()
    print(f"Memória depois de ler o grafo: {memory_after / (1024 ** 2):.2f} MB")
    print(f"Uso de memória durante a leitura do grafo: {(memory_after - memory_before) / (1024 ** 2):.2f} MB")

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
