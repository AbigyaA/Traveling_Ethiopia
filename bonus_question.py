from all_code_combine import draw_graph, traverse_all_cities


cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}


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

# Example
road_conditions = [
    ("block", "Addis Ababa", "Bahir Dar"),  # Block the road between Addis Ababa and Bahir Dar
    ("update", "Gondar", "Mekelle", 350),  # Increase the distance between Gondar and Mekelle
    ("add", "Hawassa", "Mekelle", 400)     # Add a new road between Hawassa and Mekelle
]
start_city = 'Addis Ababa'
strategy='bfs'

path, cost = traverse_with_dynamic_conditions(cities, roads, start_city, strategy, road_conditions)
print(f"Path: {path}, Cost: {cost}")

# Visualize the path if found
if path:
    draw_graph(path=path)