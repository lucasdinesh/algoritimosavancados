from KHeap import KHeap
from read_csv import read_dimacs
import sys
import time

def dijkstra(adj, weights, num_nodes, start, end, k):
    """Encontra o caminho mais curto de start para end usando um heap k-ário."""
    heap = KHeap(k, num_nodes)
    dist = {}  # Usa dicionário para alocação dinâmica
    dist[start] = 0

    insert_count = 0
    deletemin_count = 0
    update_count = 0

    heap.push(0, start)  # Insere o nó inicial com prioridade 0

    while not heap.is_empty():
        current_dist, current_node = heap.pop()  # Remove o nó com menor prioridade
        deletemin_count += 1

        # Pula se já encontramos um caminho melhor para esse nó
        if current_dist > dist.get(current_node, float('inf')):
            continue

        # Retorna o resultado se chegarmos ao destino
        if current_node == end:
            heap.print_operation_counts()
            return current_dist, insert_count, deletemin_count, update_count

        # Itera sobre vizinhos do nó atual
        for i, neighbor in enumerate(adj[current_node]):
            new_distance = current_dist + weights[current_node][i]

            if new_distance < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_distance  # Atualiza a distância

                # Lida com a posição no heap
                if isinstance(heap.position, dict):  # Implementação esparsa
                    if neighbor in heap.position:
                        heap.decrease_key(neighbor, new_distance)
                        update_count += 1
                    else:
                        heap.push(new_distance, neighbor)
                        insert_count += 1
                else:  # Implementação densa (numpy array)
                    if heap.position[neighbor] != -1:  # Já no heap
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
