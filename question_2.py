from collections import deque

from all_code_combine import draw_graph


cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
roads = {
    'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
    'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
    'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
    'Hawassa': [('Addis Ababa', 275)],
    'Mekelle': [('Gondar', 300)]
}

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


# Example
start_city = 'Addis Ababa'
goal_city = 'Mekelle'
strategy = 'dfs' 

path, cost = uninformed_path_finder(cities, roads, start_city, goal_city, strategy)
print(f"{strategy.upper()} Path: {path}, Cost: {cost}")

# Visualize the path if found
if path:
    draw_graph(path=path)
