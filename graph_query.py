import networkx as nx
from visualize import visualize_graph1, visualize_graph2

def get_subgraph(G, source_node, max_depth):
    nodes = set([source_node])
    for _ in range(max_depth):
        nodes |= set(n for node in nodes for n in G.neighbors(node))
    return G.subgraph(nodes)

def demonstrate_traversal_methods(G, method, source, target=None, max_depth=None):
    result = ""
    
    if method == "Depth-First Search (DFS)":
        dfs_tree = list(nx.dfs_preorder_nodes(G, source=source))
        result = f"DFS traversal order: {dfs_tree}... " #[:90]
        
        subgraph = G.subgraph(dfs_tree[:20])
    
        visualize_graph1(subgraph, highlight_nodes=dfs_tree[:20], title="Depth-First Search (DFS) - First 20 Nodes")
        
       
    elif method == "Breadth-First Search (BFS)":
        bfs_tree = list(nx.bfs_tree(G, source=source))
        result = f"BFS traversal order: {bfs_tree}... "
        subgraph = G.subgraph(bfs_tree[:20])
    
        visualize_graph1(subgraph, highlight_nodes=bfs_tree[:20], title="Depth-First Search (DFS) - First 20 Nodes")
    
    elif method == "Shortest Path":
        try:
            shortest_path = nx.shortest_path(G, source=source, target=target)
            result = f"Shortest path from '{source}' to '{target}': {shortest_path}"
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            visualize_graph1(G, highlight_nodes=shortest_path, highlight_edges=path_edges, title="Shortest Path")
        except nx.NetworkXNoPath:
            result = "No path found between the specified nodes."
    
    elif method == "All Simple Paths":
        try:
            all_paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=5))
            result = f"Number of paths found (max length 5): {len(all_paths)}\nExample path: {all_paths[0] if all_paths else 'No paths found'}"
            if all_paths:
                example_path = all_paths[0]
                path_edges = list(zip(example_path, example_path[1:]))
                visualize_graph1(G, highlight_nodes=example_path, highlight_edges=path_edges, title="Example of Simple Path")
        except nx.NetworkXNoPath:
            result = "No paths found between the specified nodes."
    
    elif method == "Descendants and Ancestors":
        descendants = list(nx.descendants(G, source))
        ancestors = list(nx.ancestors(G, source))
        result = f"Descendants of '{source}': {descendants}... \nAncestors of '{source}': {ancestors}"
        visualize_graph1(G, highlight_nodes=descendants + ancestors + [source], title="Descendants and Ancestors")
    
    elif method == "Degree Centrality":
        degree_centrality = nx.degree_centrality(G)
        sorted_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:20]
        result = "Top 20 nodes by degree centrality:\n" + "\n".join([f"  {node}: {centrality:.4f}" for node, centrality in sorted_centrality])
        visualize_graph1(G, highlight_nodes=[node for node, _ in sorted_centrality], title="Top Nodes by Degree Centrality")
    
    elif method == "Subgraph Extraction":
        subgraph = get_subgraph(G, source, max_depth)
        result = f"Extracted subgraph from '{source}' with max depth {max_depth}\nSubgraph nodes: {subgraph.number_of_nodes()}\nSubgraph edges: {subgraph.number_of_edges()}"
        visualize_graph2(subgraph, title=f"Subgraph (max depth: {max_depth})")

    return result


# import networkx as nx

# #sub graph
# def get_subgraph(G, source_node, max_depth):
#     """
#     Extract a subgraph from G starting at source_node and including all nodes
#     up to max_depth levels away.
#     """
#     nodes = set([source_node])
#     for _ in range(max_depth):
#         nodes |= set(n for node in nodes for n in G.neighbors(node))
#     return G.subgraph(nodes)

# def demonstrate_traversal_methods(G):
#     print("\nDemonstrating NetworkX traversal methods:")
    
#     # 1. Depth-First Search (DFS)
#     print("\n1. Depth-First Search (DFS) from :")
#     dfs_tree = list(nx.dfs_preorder_nodes(G, source="module_38"))
#     print(f"DFS traversal order: {dfs_tree[:90]}... (90 nodes)")

#     # 2. Breadth-First Search (BFS)
#     print("\n2. Breadth-First Search (BFS) from Versys Kiyo:")
#     bfs_tree = list(nx.bfs_tree(G, source="Versys Kiyo"))
#     print(f"BFS traversal order: {bfs_tree[:5]}... (showing first 5 nodes)")

#     # 3. Shortest Path
#     print("\n3. Shortest Path:")
#     try:
#         shortest_path = nx.shortest_path(G, source="Business Group (Etch)", target="part_3115")
#         print(f"Shortest path from 'Business Group (Etch)' to 'Make Part - 1': {shortest_path}")
#     except nx.NetworkXNoPath:
#         print("No path found between the specified nodes.")

#     # 4. All Simple Paths
#     print("\n4. All Simple Paths:")
#     try:
#         all_paths = list(nx.all_simple_paths(G, source="Business Group (Etch)", target="Make Part - 1", cutoff=5))
#         print(f"Number of paths found (max length 5): {len(all_paths)}")
#         if all_paths:
#             print(f"Example path: {all_paths[0]}")
#     except nx.NetworkXNoPath:
#         print("No paths found between the specified nodes.")

#     # 5. Descendants and Ancestors
#     print("\n5. Descendants and Ancestors:")
#     node = "Kiyo Product Family"
#     descendants = list(nx.descendants(G, node))
#     ancestors = list(nx.ancestors(G, node))
#     print(f"Descendants of '{node}': {descendants}... (showing first 5)")
#     print(f"Ancestors of '{node}': {ancestors}")
    
#     def visualize_graph1(list_traversal):

#         # Create a new graph for the descendants
#         H = nx.DiGraph()

#         # Add the descendants as nodes
#         H.add_nodes_from(list_traversal)

#         # Add edges between the descendants based on the original graph
#         for list_of_nodes in list_traversal:
#             for neighbor in G.successors(list_of_nodes):
#                 if neighbor in list_traversal:
#                     H.add_edge(list_of_nodes, neighbor)

#         # Optionally, add the original node to the new graph
#         H.add_node(node)
#         for neighbor in G.successors(node):
#             if neighbor in list_traversal:
#                 H.add_edge(node, neighbor)

#         # Define colors for the nodes
#         node_colors = []
#         for n in H.nodes():
#             if n == node:
#                 node_colors.append('red')  # Selected node
#             elif n in G.successors(node):
#                 node_colors.append('blue')  # Direct successors
#             else:
#                 node_colors.append('green')  # Other descendants

#         # Draw the graph
        
#         pos = nx.spring_layout(H)  # Positions for all nodes
#         plt.figure(figsize=(8,12))
#         nx.draw(H, pos, with_labels=True, node_color=node_colors, node_size=800, font_size=20, font_color='black', edge_color='gray')
#         plt.show()

#     #visualize_graph1(ancestors)
#     #visualize_graph1(descendants)
#     #visualize_graph1(dfs_tree)
#     #visualize_graph1(bfs_tree)
#     #print("Trail shortest path using vg")
#     #visualize_graph1(shortest_path)
#     ##visualize_graph(all_paths)

  
   
#     # Degree Centrality
#     print("\n6. Degree Centrality:")
#     degree_centrality = nx.degree_centrality(G)
#     sorted_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
#     print("Top 5 nodes by degree centrality:")
#     for node, centrality in sorted_centrality:
#         print(f"  {node}: {centrality:.4f}")


#     print("\n7. Subgraph Extraction:")
#     source_node = "Business Group (Etch)"
#     max_depth = 3
#     subgraph = get_subgraph(G, source_node, max_depth)
#     print(f"Extracted subgraph from '{source_node}' with max depth {max_depth}")
#     print(f"Subgraph nodes: {subgraph.number_of_nodes()}")
#     print(f"Subgraph edges: {subgraph.number_of_edges()}")
#     #visualize_graph(subgraph)

#     #edge_bfs n dfs
#     # edgesbfs = list(nx.edge_bfs(G, source="Kiyo Product Family"))
#     # print("\n8. Edge bfs: ", edgesbfs)

#     # edgesdfs = list(nx.edge_dfs(G, source="level_28_94062"))
#     # print("\n9. Edge dfs: ", edgesdfs)

#     indegree_centrality = nx.in_degree_centrality(G)
#     print("\n10. In degree centrality:", indegree_centrality)

#     core_number = nx.core_number(subgraph)
#     print("Core number of Subgraph:", core_number)

# start_time = time.time()

# before_usage = memory_usage()[0]

# demonstrate_traversal_methods(updated_graph)

# end_time = time.time()
# after_usage = memory_usage()[0]

# total_memory = after_usage - before_usage
# print("memory usage in MiB mebibytes (binary system): ", total_memory)
# execution_time = end_time - start_time
# print("execution time in seconds: ",execution_time)


