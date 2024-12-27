import networkx as nx
import matplotlib.pyplot as plt

cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

graph = nx.Graph()

for city, connections in roads.items():
    for connected_city, distance in connections:
        graph.add_edge(city, connected_city, weight=distance)

def draw_graph(path=None):
    pos = nx.spring_layout(graph, seed=42) 

    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Road Network of Ethiopian Cities")
    plt.show()


# Visualization of the road network
draw_graph()