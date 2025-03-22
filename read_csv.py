def read_dimacs(in_file):
    # Initialize variables for number of nodes and edges
    n, m = 0, 0
    graph = {}

    # Read the lines until we find the 'p sp' line
    line = in_file.readline().strip()
    while not line.startswith("p sp"):
        line = in_file.readline().strip()

    # Parse the 'p sp' line to get the number of nodes and edges
    parts = line.split()
    n, m = int(parts[2]), int(parts[3])

    # Initialize the graph as a dictionary of lists (for adjacency list representation)
    graph = {i: [] for i in range(1, n + 1)}

    # Read the edges
    for _ in range(m):
        line = in_file.readline().strip()
        if line.startswith("a "):
            parts = line.split()
            u, v, w = int(parts[1]), int(parts[2]), int(parts[3])
            # Process the arc (u, v) with weight w
            # Add the edge only in one direction (u -> v), not (v -> u)
            if v not in [adj[0] for adj in graph[u]]:  # Avoid duplicates
                graph[u].append((v, w))
            if u not in [adj[0] for adj in graph[v]]:  # Avoid duplicates
                graph[v].append((u, w))  # For undirected graph, add the reverse edge

    return graph, n, m


def write_graph_to_file(graph, num_nodes, num_edges, output_file):
    with open(output_file, 'w') as out_file:
        out_file.write(f"Number of nodes: {num_nodes}\n")
        out_file.write(f"Number of edges: {num_edges}\n\n")

        for vertex, adjacents in graph.items():
            adj_list_str = ", ".join([f"(to: {v}, weight: {w})" for v, w in adjacents])
            out_file.write(f"node {vertex}: {adj_list_str}\n")


# Example usage:
input_filename = 'USA-road-d.NY.gr'  # Replace with the path to your .gr file
output_filename = 'output_graph.txt'  # Replace with the desired output file path

# Read the graph from the input file
with open(input_filename, 'r') as file:
    graph, num_nodes, num_edges = read_dimacs(file)

# Write the graph to the output file
write_graph_to_file(graph, num_nodes, num_edges, output_filename)

print(f"Graph has been written to {output_filename}")
