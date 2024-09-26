import streamlit as st
import numpy as np

def normalize_probabilities(probabilities):
    """Normalize the probabilities so they sum to 1."""
    return list(np.array(probabilities) / sum(probabilities))

def get_user_inputs():
    st.subheader("Probability Distribution for Custom Kernel")
    prob_0 = st.slider("Probability for degree 0", 0.0, 1.0, 1.0)
    prob_1_2 = st.slider("Probability for degree 1-2", 0.0, 1.0, 0.8)
    prob_3_4 = st.slider("Probability for degree 3-4", 0.0, 1.0, 0.6)
    prob_5_plus = st.slider("Probability for degree 5+", 0.0, 1.0, 0.4)

    probability_distribution = [prob_0, prob_1_2, prob_3_4, prob_5_plus]
    
    # Normalize the probability distribution
    normalized_probability_distribution = normalize_probabilities(probability_distribution)
    
    st.write("Normalized Probability Distribution:")
    st.write(f"Degree 0: {normalized_probability_distribution[0]:.4f}")
    st.write(f"Degree 1-2: {normalized_probability_distribution[1]:.4f}")
    st.write(f"Degree 3-4: {normalized_probability_distribution[2]:.4f}")
    st.write(f"Degree 5+: {normalized_probability_distribution[3]:.4f}")

    st.subheader("Graph Generation Options")
    generation_type = st.radio("Choose generation type", ["Same for all levels", "Custom for each level"])

    if generation_type == "Same for all levels":
        num_levels = st.number_input("Number of levels", min_value=1, value=5)
        nodes_per_level = st.number_input("Nodes per level", min_value=1, value=1000)
        level_node_dict = {level: nodes_per_level for level in range(3, 3 + num_levels)}
    else:
        num_levels = st.number_input("Number of levels", min_value=1, value=5)
        level_node_dict = {}
        for level in range(3, 3 + num_levels):
            nodes = st.number_input(f"Nodes for level {level}", min_value=1, value=1000)
            level_node_dict[level] = nodes

    connections_per_node = st.number_input("Connections per node", min_value=1, value=2)
    jump_probability = st.slider("Jump probability", 0.0, 1.0, 0.1)

    return {
        'probability_distribution': normalized_probability_distribution,
        'level_node_dict': level_node_dict,
        'connections_per_node': connections_per_node,
        'jump_probability': jump_probability
    }




# import json
# import networkx as nx


# def create_base_schema_graph(json_file):
#     with open(json_file, 'r') as f:
#         data = json.load(f)
    
#     G = nx.DiGraph()
    
#     def add_nodes_recursively(node, parent=None, level=0):
#         node_id = node['name']
#         G.add_node(node_id, level=level, node_type=get_node_type(level))
        
#         if parent:
#             G.add_edge(parent, node_id)
        
#         if 'connected_to' in node:
#             G.add_edge(node_id, node['connected_to'])
        
#         if 'children' in node:
#             for child in node['children']:
#                 add_nodes_recursively(child, node_id, level + 1)
    
#     add_nodes_recursively(data['Business Group'])
    
#     return G


# def get_node_type(level):
#     node_types = {
#         0: "business_group",
#         1: "product_family",
#         2: "product_offering",
#         3: "module",
#         4: "part"
#     }
    
#     return node_types.get(level, f"level_{level}")



# def custom_kernel(degree):
#     if degree == 0:
#         return 1
#     elif degree < 3:
#         return 0.8
#     elif degree < 5:
#         return 0.6
#     else:
#         return 0.4