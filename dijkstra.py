from KHeap import KHeap
from read_csv import read_dimacs
import sys
import time

from array import array

from array import array


def dijkstra(adj, weights, num_nodes, start, end, k):
    """Encontra o caminho mais curto de start para end usando um heap k-ário."""

    start -= 1  # Convertendo para índice base 0
    end -= 1  # Convertendo para índice base 0

    heap = KHeap(k, num_nodes)
    dist = {}  # Dicionário dinâmico para evitar alocação de memória excessiva
    dist[start] = 0
    heap.push(0, start)

    insert_count = 0
    deletemin_count = 0
    update_count = 0

    while not heap.is_empty():
        current_dist, current_node = heap.pop()
        deletemin_count += 1

        if current_dist > dist.get(current_node, float('inf')):
            continue

        if current_node == end:
            heap.print_operation_counts()
            return current_dist, insert_count, deletemin_count, update_count

        neighbors = adj[current_node]
        weights_list = weights[current_node]

        for i in range(len(neighbors)):
            neighbor = neighbors[i]  # Índice já está em base 0
            new_distance = current_dist + weights_list[i]

            if new_distance < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_distance

                if heap.position[neighbor] != -1:
                    heap.decrease_key(neighbor, new_distance)
                    update_count += 1
                else:
                    heap.push(new_distance, neighbor)
                    insert_count += 1

    heap.print_operation_counts()
    return "inf", insert_count, deletemin_count, update_count


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Uso: ./dijkstra <origem> <destino> < input.gr")

    source = int(sys.argv[1])
    target = int(sys.argv[2])
    file_path = str(sys.argv[3])

    start_time = time.time()

    # Lê o grafo da entrada padrão
    sys.stdin.reconfigure(encoding='utf-8')
    print("Iniciei a leitura do grafo")
    adj, weights, num_nodes, num_edges = read_dimacs(file_path)
    print("Finalizei a leitura do grafo")

    # Executa o algoritmo de Dijkstra com heap k-ário (k=2 para binário)
    result, insert_count, deletemin_count, update_count = dijkstra(adj, weights, num_nodes, source, target, k=2)

    end_time = time.time()

    # Imprime o resultado final
    execution_time = end_time - start_time
    print(f"Resultado: {result}")
    print(f"Tempo de execução: {execution_time:.6f} segundos")
    print(f"Operações insert: {insert_count}")
    print(f"Operações deletemin: {deletemin_count}")
    print(f"Operações update: {update_count}")
