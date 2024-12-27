import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}



# QUESTION 1

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



# QUESTION 2

def uninformed_path_finder(cities, roads, start_city, goal_city, strategy):
    """
    Parameters:
    - cities: List of city names.
    - roads: Dictionary with city connections as {city: [(connected_city, distance)]}.
    - start_city: The city to start the journey.
    - goal_city: The destination city (for specific tasks).
    - strategy: The uninformed search strategy to use ('bfs' or 'dfs').
    Returns:
    - path: List of cities representing the path from start_city to goal_city.
    - cost: Total cost (distance) of the path.
    """
    visited = set()
    if strategy == 'bfs':
        queue = deque([(start_city, [start_city], 0)])
        while queue:
            current_city, path, cost = queue.popleft()
            if current_city == goal_city:
                return path, cost
            if current_city not in visited:
                visited.add(current_city)
                for neighbor, distance in roads.get(current_city, []):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor], cost + distance))

    elif strategy == 'dfs':
        stack = [(start_city, [start_city], 0)]
        while stack:
            current_city, path, cost = stack.pop()
            if current_city == goal_city:
                return path, cost
            if current_city not in visited:
                visited.add(current_city)
                for neighbor, distance in roads.get(current_city, []):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor], cost + distance))

    return None, None 



# QUESTION 3

def traverse_all_cities(cities, roads, start_city, strategy):
    """
    Parameters:
    - cities: List of city names.
    - roads: Dictionary with city connections as {city: [(connected_city, distance)]}.
    - start_city: The city to start the journey.
    - strategy: The uninformed search strategy to use ('bfs' or 'dfs').
    Returns:
    - path: List of cities representing the traversal path.
    - cost: Total cost (distance) of the traversal.
    """
    def dfs(current_city, visited, path, cost):
        visited.add(current_city)
        path.append(current_city)
        all_paths.append((list(path), cost))  

        for neighbor, distance in roads.get(current_city, []):
            if neighbor not in visited:
                dfs(neighbor, visited, path, cost + distance)

        visited.remove(current_city)
        path.pop()

    def bfs():
        queue = deque([(start_city, [start_city], 0)])  
        while queue:
            current_city, path, cost = queue.popleft()
            all_paths.append((path, cost))  
            for neighbor, distance in roads.get(current_city, []):
                if neighbor not in path:  
                    queue.append((neighbor, path + [neighbor], cost + distance))

    all_paths = []

    if strategy == 'dfs':
        dfs(start_city, set(), [], 0)
    elif strategy == 'bfs':
        bfs()

    best_path, best_cost = max(all_paths, key=lambda x: (len(x[0]), -x[1]))

    return best_path, best_cost




#  BONUS (ADVANCED CHALLENGES)

def traverse_with_dynamic_conditions(cities, roads, start_city, strategy, road_conditions=None):
    """
    Parameters:
    - cities: List of city names.
    - roads: Dictionary with city connections as {city: [(connected_city, distance)]}.
    - start_city: The city to start the journey.
    - strategy: The uninformed search strategy to use ('bfs' or 'dfs').
    - road_conditions: List of road conditions, where each condition is a tuple:
        - ("block", city1, city2): Block a road between city1 and city2.
        - ("update", city1, city2, new_distance): Update the distance between city1 and city2.
        - ("add", city1, city2, distance): Add a new road between city1 and city2 with the given distance.
    Returns:
    - path: List of cities representing the traversal path.
    - cost: Total cost (distance) of the traversal.
    """
    dynamic_roads = {city: list(neighbors) for city, neighbors in roads.items()}

    if road_conditions:
        for condition in road_conditions:
            action = condition[0]
            city1, city2 = condition[1], condition[2]

            if action == "block":
                dynamic_roads[city1] = [(c, d) for c, d in dynamic_roads[city1] if c != city2]
                dynamic_roads[city2] = [(c, d) for c, d in dynamic_roads[city2] if c != city1]

            elif action == "update":
                new_distance = condition[3]
                dynamic_roads[city1] = [(c, d if c != city2 else new_distance) for c, d in dynamic_roads[city1]]
                dynamic_roads[city2] = [(c, d if c != city1 else new_distance) for c, d in dynamic_roads[city2]]

            elif action == "add":
                distance = condition[3]
                if city2 not in [c for c, _ in dynamic_roads[city1]]:
                    dynamic_roads[city1].append((city2, distance))
                if city1 not in [c for c, _ in dynamic_roads[city2]]:
                    dynamic_roads[city2].append((city1, distance))

    return traverse_all_cities(cities, dynamic_roads, start_city, strategy)
