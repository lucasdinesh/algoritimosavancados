from KHeap import KHeap
# from read_csv import read_dimacs_with_gc as read_dimacs
from read_csv import read_dimacs
import sys
import time
import numpy as np


def dijkstra(graph, num_nodes, start, end, k):
    """Finds the shortest path from start to end using a k-ary heap."""
    heap = KHeap(k, num_nodes)
    dist = np.full(num_nodes, float('inf'), dtype=np.float64)  # Initialize distances to infinity
    dist[start] = 0

    insert_count = 0
    deletemin_count = 0
    update_count = 0

    heap.push(0, start)  # Push the starting node with priority 0

    while not heap.is_empty():
        current_dist, current_node = heap.pop()  # Remove the minimum-priority node
        deletemin_count += 1

        # Skip if a better path was already found for this node
        if current_dist > dist[current_node]:
            continue

        # Return result if we've reached the destination node
        if current_node == end:
            heap.print_operation_counts()  # Print internal operation counts
            return current_dist, insert_count, deletemin_count, update_count

        for neighbor, weight in graph[current_node]:
            # Skip invalid neighbors
            if neighbor < 0 or neighbor >= num_nodes:
                continue

            new_distance = current_dist + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance

                # Handle sparse or dense position arrays
                if isinstance(heap.position, dict):  # Sparse case
                    if neighbor in heap.position:
                        heap.decrease_key(neighbor, new_distance)
                        update_count += 1
                    else:
                        heap.push(new_distance, neighbor)
                        insert_count += 1
                else:  # Dense case (numpy array)
                    if heap.position[neighbor] != -1:  # Already in the heap
                        heap.decrease_key(neighbor, new_distance)
                        update_count += 1
                    else:
                        heap.push(new_distance, neighbor)
                        insert_count += 1

    heap.print_operation_counts()
    return "inf", insert_count, deletemin_count, update_count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Uso: ./dijkstra <origem> <destino> < input.gr")

    source = int(sys.argv[1])
    target = int(sys.argv[2])

    start_time = time.time()

    # Lê o grafo da entrada padrão
    sys.stdin.reconfigure(encoding='utf-8')
    print("iniciei a leitura do grafo")
    graph, num_nodes, num_edges = read_dimacs(sys.stdin)
    print("finalizei a leitura do grafo")
    # Executa o algoritmo de Dijkstra com heap k-ário (k=2 para binário)
    result, insert_count, deletemin_count, update_count = dijkstra(graph, num_nodes, source, target, k=2)

    end_time = time.time()

    # Imprime o resultado final
    execution_time = end_time - start_time
    print(f"Resultado: {result}")
    print(f"Tempo de execução: {execution_time:.6f} segundos")
    print(f"Operações insert: {insert_count}")
    print(f"Operações deletemin: {deletemin_count}")
    print(f"Operações update: {update_count}")
