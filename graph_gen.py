import json
import networkx as nx
import random


def create_base_schema_graph(json_data):
    data = json.loads(json_data)
    G = nx.DiGraph()

    def add_nodes_recursively(node, parent=None, level=0):
        node_id = node['name']
        G.add_node(node_id, level=level, node_type=get_node_type(level))
        
        if parent:
            G.add_edge(parent, node_id)
        
        if 'connected_to' in node:
            G.add_edge(node_id, node['connected_to'])
        
        if 'children' in node:
            for child in node['children']:
                add_nodes_recursively(child, node_id, level + 1)

    add_nodes_recursively(data['Business Group'])
    
    return G

def get_node_type(level):
    node_types = {
        0: "business_group",
        1: "product_family",
        2: "product_offering",
        3: "module",
        4: "part"
    }
    
    return node_types.get(level, f"level_{level}")

def custom_kernel(degree, probability_distribution):
    if degree == 0:
        return probability_distribution[0]
    elif degree < 3:
        return probability_distribution[1]
    elif degree < 5:
        return probability_distribution[2]
    else:
        return probability_distribution[3]

def add_nodes_to_multiple_levels(G, level_node_dict, connections_per_node=1, jump_probability=0, probability_distribution=[1.0, 0.8, 0.6, 0.4]):
    root_node = [n for n in G.nodes() if G.in_degree(n) == 0][0]  # Assume the root is the only node with in_degree 0
    
    # Determine the starting level
    start_level = max(data.get('level', 0) for _, data in G.nodes(data=True)) + 1

    for level_number, num_nodes in level_node_dict.items():
        # Adjust the level number to start from the next available level
        adjusted_level = start_level + level_number - min(level_node_dict.keys())
        
        # Generate new nodes
        new_nodes = nx.gn_graph(num_nodes, kernel=lambda x: custom_kernel(x, probability_distribution))
        
        # Add new nodes to the main graph
        node_mapping = {}
        for node in new_nodes.nodes():
            new_node_name = f"level_{adjusted_level}_{len(G.nodes())}"
            G.add_node(new_node_name, level=adjusted_level, node_type=get_node_type(adjusted_level))
            node_mapping[node] = new_node_name
        
        # Connect to parent level
        parent_level_nodes = [n for n in G.nodes() if G.nodes[n].get('level', 0) == adjusted_level - 1]
        if parent_level_nodes:
            for new_node in node_mapping.values():
                parents = random.sample(parent_level_nodes, min(connections_per_node, len(parent_level_nodes)))
                for parent in parents:
                    G.add_edge(parent, new_node)
        else:
            G.add_edge(root_node, list(node_mapping.values())[0])
        
        # Add edges between new nodes based on the generated graph
        for edge in new_nodes.edges():
            G.add_edge(node_mapping[edge[0]], node_mapping[edge[1]])
        
        # Add jumps between levels
        if jump_probability > 0:
            all_nodes = list(G.nodes())
            for new_node in node_mapping.values():
                if random.random() < jump_probability:
                    jump_target = random.choice(all_nodes)
                    if jump_target != new_node:
                        G.add_edge(new_node, jump_target)
    
    return G




# import networkx as nx
# import random

# import time
# from memory_profiler import memory_usage 

# start_time = time.time()

# before_usage = memory_usage()[0]



# #nodes_at_level = [node for node, depth in nx.single_source_shortest_path_length(G, "Business Group (Etch)").items() if depth == level]


# def add_nodes_to_multiple_levels(G, level_node_dict, connections_per_node=1, jump_probability=0):
#     root_node = [n for n in G.nodes() if G.in_degree(n) == 0][0]  # Assume the root is the only node with in_degree 0
    
#     for level_number, num_nodes in level_node_dict.items():
#         # Generate new nodes
#         new_nodes = nx.gn_graph(num_nodes, kernel=custom_kernel)
        
#         # Add new nodes to the main graph
#         node_mapping = {}
#         for node in new_nodes.nodes():
#             new_node_name = f"{get_node_type(level_number)}_{len(G.nodes())}"
#             G.add_node(new_node_name, level=level_number, node_type=get_node_type(level_number))
#             node_mapping[node] = new_node_name
        
#         # Connect to parent level
#         parent_level_nodes = [n for n in G.nodes() if G.nodes[n].get('level', 0) == level_number - 1]
#         if parent_level_nodes:
#             for new_node in node_mapping.values():
#                 parents = random.sample(parent_level_nodes, min(connections_per_node, len(parent_level_nodes)))
#                 for parent in parents:
#                     G.add_edge(parent, new_node)
#         else:
#             G.add_edge(root_node, list(node_mapping.values())[0])
        
#         # Add edges between new nodes based on the generated graph
#         for edge in new_nodes.edges():
#             new_node_name = f"{get_node_type(level_number)}_{len(G.nodes())}"
#             G.add_edge(node_mapping[edge[0]], node_mapping[edge[1]])
        
#         # Add jumps between levels
#         if jump_probability > 0:
#             all_nodes = list(G.nodes())
#             for new_node in node_mapping.values():
#                 if random.random() < jump_probability:
#                     jump_target = random.choice(all_nodes)
#                     if jump_target != new_node:
#                         G.add_edge(new_node, jump_target)
    
#     return G


# # Example usage
# json_file = 'data_schema_corrected.json'
# base_graph = create_base_schema_graph(json_file)
# print("Base graph created")
# print("Nodes:", base_graph.number_of_nodes())
# print("Edges:", base_graph.number_of_edges())

# # Add nodes to multiple levels with specific numbers for each level
# level_node_dict = {
#     3: 2000,
#     4: 3000,
#     5: 2000,
#     6: 1000,
#     7: 2000,
#     8: 5000,
#     9: 6500,
#     10: 4900,
#     11: 3500,
#     12: 1500,
#     13: 6000,
#     14: 4000,
#     15: 8000,
#     16: 2000,
#     17: 3000,
#     18: 2000,
#     19: 1000,
#     20: 2000,
#     21: 5000,
#     22: 6500,
#     23: 4900,
#     24: 3500,
#     25: 1500,
#     26: 6000,
#     27: 4000,
#     28: 8000,
#     29: 3000,# Add 5 nodes to level 3
    
# }

# connections_per_node = 2
# jump_probability= 0.1

# updated_graph = add_nodes_to_multiple_levels(base_graph, level_node_dict, connections_per_node, jump_probability)
# print("\nAdded nodes to multiple levels:")
# for level, count in level_node_dict.items():
#     print(f"  Level {level}: {count} nodes")
# print("Updated Nodes:", updated_graph.number_of_nodes())
# print("Updated Edges:", updated_graph.number_of_edges())

# #visualize_graph(updated_graph)


# end_time = time.time()
# after_usage = memory_usage()[0]

# total_memory = after_usage - before_usage
# print("1 MiB = 1.048576 MB, Mega binary byte")
# print("memory usage in MiB mebibyte (binary system): ", total_memory)
# execution_time = end_time - start_time
# print("execution time in seconds: ",execution_time)
