from KHeap import KHeap
from read_csv import read_dimacs
import sys
import time


def dijkstra(graph, start, end, k):
    """Encontra o caminho mais curto de start para end usando um heap k-ário."""
    heap = KHeap(k)
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    insert_count = 0
    deletemin_count = 0
    update_count = 0

    heap.push(0, start)  # (custo, nó)

    while not heap.is_empty():
        current_dist, current_node = heap.pop()
        deletemin_count += 1

        # Se chegamos ao nó de destino, retornamos a menor distância
        if current_node == end:
            return current_dist, insert_count, deletemin_count, update_count

        # Se a distância já foi processada, continue
        if current_dist > dist[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < dist[neighbor]:  # Encontrou um caminho melhor
                dist[neighbor] = distance
                heap.push(distance, neighbor)
                heap.decrease_key(neighbor, distance)
                update_count += 1

                insert_count += 1
    return "inf", insert_count, deletemin_count, update_count



if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Uso: ./dijkstra <origem> <destino> < input.gr")

    source = int(sys.argv[1])
    target = int(sys.argv[2])

    start_time = time.time()

    # Lê o grafo da entrada padrão
    graph, num_nodes, num_edges = read_dimacs(sys.stdin)

    # Executa o algoritmo de Dijkstra (corrigido com k=3)
    result, insert_count, deletemin_count, update_count = dijkstra(graph, source, target, k=3)

    end_time = time.time()

    # Imprime apenas o resultado final
    execution_time = end_time - start_time
    print(f"Resultado: {result}")
    print(f"Tempo de execução: {execution_time:.6f} segundos")
    print(f"Operações insert: {insert_count}")
    print(f"Operações deletemin: {deletemin_count}")
    print(f"Operações update: {update_count}")
