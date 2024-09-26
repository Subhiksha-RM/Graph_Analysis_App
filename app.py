import streamlit as st
import json
import time
from memory_profiler import memory_usage
from input import get_user_inputs
from graph_gen import create_base_schema_graph, add_nodes_to_multiple_levels
from visualize import visualize_graph  
from graph_query import demonstrate_traversal_methods, get_subgraph

def main():
    st.title("Graph Generator App")

    # Sidebar for navigation
    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Graph Generation", "Graph Query"])

    if app_mode == "Graph Generation":
        graph_generation()
    elif app_mode == "Graph Query":
        graph_query()


def graph_generation():
    # File upload for JSON
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    if uploaded_file is not None:
        json_data = uploaded_file.read().decode("utf-8")
        base_graph = create_base_schema_graph(json_data)
        st.success("Base graph created successfully!")
        st.write(f"Base graph nodes: {base_graph.number_of_nodes()}")
        st.write(f"Base graph edges: {base_graph.number_of_edges()}")

        # Get user inputs
        inputs = get_user_inputs()

        start_time = time.time()
        before_usage = memory_usage()[0]

        if st.button("Generate Graph"):
            updated_graph = add_nodes_to_multiple_levels(
                base_graph,
                inputs['level_node_dict'],
                inputs['connections_per_node'],
                inputs['jump_probability'],
                inputs['probability_distribution']
            )

            

            st.success("Graph generated successfully!")
            st.write(f"Total nodes: {updated_graph.number_of_nodes()}")
            st.write(f"Total edges: {updated_graph.number_of_edges()}")
            end_time = time.time()
            after_usage = memory_usage()[0]
            memory_used = after_usage - before_usage
            st.write("Memory used in MiB -Mega Binary Bytes : ", memory_used)
            time_taken = end_time - start_time
            st.write ("Time taken for Graph Generation: ",time_taken)

            # Visualize the graph
            if updated_graph.number_of_nodes() <= 2000:
                visualize_graph(updated_graph)
        else:
            st.warning("Graph is too large to visualize (> 2000 nodes)")
            

            # Convert graph to JSON and display
        graph_json = json.dumps(dict(nodes=list(updated_graph.nodes(data=True)),
                                         edges=list(updated_graph.edges(data=True))),
                                    indent=2)
        st.subheader("Generated Graph (JSON)")
        st.json(graph_json)

            # Download button for JSON
        st.download_button(
                label="Download JSON",
                data=graph_json,
                file_name="generated_graph.json",
                mime="application/json"
            )

            # Store the graph in session state for use in graph_query
        st.session_state['graph'] = updated_graph


def graph_query():
    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first in the Graph Generation tab.")
        return

    updated_graph = st.session_state['graph']
    
    # Extract node IDs and levels
    node_info = {node: data for node, data in updated_graph.nodes(data=True)}
    levels = sorted(set(data.get('level', 0) for data in node_info.values()))

    # Query methods
    st.subheader("Query Methods")
    query_method = st.selectbox("Select a query method", [
        "Depth-First Search (DFS)",
        "Breadth-First Search (BFS)",
        "Shortest Path",
        "All Simple Paths",
        "Descendants and Ancestors",
        "Degree Centrality",
        "Subgraph Extraction"
    ])

    # Initialize variables
    source = None
    target = None
    max_depth = 3

    # Common inputs for most query methods
    if query_method in ["Depth-First Search (DFS)", "Breadth-First Search (BFS)", "Descendants and Ancestors", "Shortest Path", "All Simple Paths", "Subgraph Extraction"]:
        source_level = st.selectbox("Select source node level", levels, key="source_level")
        source_nodes = [node for node, data in node_info.items() if data.get('level', 0) == source_level]
        source = st.selectbox("Select source node", source_nodes, key="source")

    # Additional inputs for specific query methods
    if query_method in ["Shortest Path", "All Simple Paths"]:
        target_level = st.selectbox("Select target node level", levels, key="target_level")
        target_nodes = [node for node, data in node_info.items() if data.get('level', 0) == target_level]
        target = st.selectbox("Select target node", target_nodes, key="target")

    if query_method == "Subgraph Extraction":
        max_depth = st.number_input("Maximum depth", min_value=1, value=3, key="max_depth")

    if st.button("Run Query"):
        result = demonstrate_traversal_methods(
            updated_graph, 
            query_method, 
            source, 
            target if query_method in ["Shortest Path", "All Simple Paths"] else None,
            max_depth if query_method == "Subgraph Extraction" else None
        )
        st.write(result)

        # Visualization
        if updated_graph.number_of_nodes() <= 2000:
            st.subheader("Graph Visualization")
            visualize_graph(updated_graph)
        else:
            st.warning("Graph is too large to visualize (> 2000 nodes)")

if __name__ == "__main__":
    main()