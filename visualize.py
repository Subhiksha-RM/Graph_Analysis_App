import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def visualize_graph(G):
    pos = nx.spring_layout(G, k=2, iterations=50)
    plt.figure(figsize=(12, 8))
    node_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#CCCCFF']
    
    max_level = max(G.nodes[node].get('level', 0) for node in G.nodes())
    
    for level in range(max_level + 1):
        nx.draw_networkx_nodes(G, pos, 
                               nodelist=[n for n, d in G.nodes(data=True) if d.get('level', 0) == level],
                               node_color=node_colors[level % len(node_colors)],
                               node_size=1000,
                               alpha=0.8)
    
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")
    
    plt.title("Schema to Graph")
    plt.axis('off')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig("graph.png")
    
    # Display the figure in Streamlit
    st.pyplot(plt)

def visualize_graph1(G, highlight_nodes=None, highlight_edges=None, title="Graph Visualization"):
    plt.figure(figsize=(12, 8))
    
    # Create a subgraph with only the first 20 nodes
    nodes_to_draw = highlight_nodes[:20]
    subgraph = G.subgraph(nodes_to_draw)
    
    pos = nx.spring_layout(subgraph, k=2, iterations=50)
    
    # Draw the subgraph
    nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=8, arrows=True)
    
    if highlight_nodes:
        nx.draw_networkx_nodes(subgraph, pos, nodelist=nodes_to_draw, node_color='red', node_size=400)
        
        # Add labels to show traversal order
        labels = {node: node for node in (nodes_to_draw)}
        nx.draw_networkx_labels(subgraph, pos, labels, font_size=10, font_color="white")
    
    if highlight_edges:
        edges_in_subgraph = [edge for edge in highlight_edges if edge[0] in nodes_to_draw and edge[1] in nodes_to_draw]
        nx.draw_networkx_edges(subgraph, pos, edgelist=edges_in_subgraph, edge_color='r', width=2)
    
    plt.title(title)
    st.pyplot(plt)
    plt.close()



def visualize_graph2(G, highlight_nodes=None, highlight_edges=None, title="Graph Visualization"):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Draw the full graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=8, arrows=True)
    
    if highlight_nodes:
        # If there are many highlight_nodes, we'll only highlight a subset
        highlight_subset = highlight_nodes[:20] if len(highlight_nodes) > 20 else highlight_nodes
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_subset, node_color='red', node_size=400)
        
        # Add labels to highlight order
        labels = {node: node for node in (highlight_subset)}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="white")
    
    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='r', width=2)
    
    plt.title(title)
    st.pyplot(plt)
    plt.close()  # Close the figure to free up memory




# Example usage
# G = nx.DiGraph()  # Create your graph here
# visualize_graph(G)



# def visualize_graph(G):
#     pos = nx.spring_layout(G, k=2, iterations=50)
#     plt.figure(figsize=(12, 8))
#     node_colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#CCCCFF']
    
#     max_level = max(G.nodes[node].get('level', 0) for node in G.nodes())
    
#     for level in range(max_level + 1):
#         nx.draw_networkx_nodes(G, pos, 
#                                nodelist=[n for n, d in G.nodes(data=True) if d.get('level', 0) == level],
#                                node_color=node_colors[level % len(node_colors)],
#                                node_size=1000,
#                                alpha=0.8)
    
#     nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
#     nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")
    
#     plt.title("Schema to Graph")
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()
#     st.pyplot(G)
