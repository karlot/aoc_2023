import sys
import networkx as nx

def main(filename):
    """
    # Results:
    Part1: 555856
    Part2: -
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        # grid = tuple([tuple([c for c in line]) for line in lines])

    # Some switches when running only single part
    run_part1 = True
    # run_part2 = True

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        graph = nx.Graph()
        for line in lines:
            node_a, connections = line.split(": ")
            connected_nodes = connections.split()
            for node_b in connected_nodes:
                graph.add_edge(node_a, node_b)
        
        graph.remove_edges_from(nx.minimum_edge_cut(graph))
        a, b = nx.connected_components(graph)

        print(f"Part1: {len(a) * len(b)}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    # if run_part2:
    #     print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
