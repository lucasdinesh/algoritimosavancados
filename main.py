from read_csv import read_dimacs
from dijkstra import dijkstra
import sys

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     sys.exit("Uso: ./dijkstra <origem> <destino> < input.gr")

    # source = int(sys.argv[1])
    source = 1
    # target = int(sys.argv[2])
    target = 2

    # Lê o grafo da entrada padrão
    # graph = read_dimacs(sys.stdin)
    with open("USA-road-d.NY.gr", 'r') as file:
        graph, num_nodes, num_edges = read_dimacs(file)

    # Executa o algoritmo de Dijkstra
    result = dijkstra(graph, source, target, 3)

    # Imprime apenas o resultado final
    print(result)
