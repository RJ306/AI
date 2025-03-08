delivery_graph = {
    'A': {'B': 2, 'C': 1},
    'B': {'D': 4, 'E': 3},
    'C': {'F': 1, 'G': 5},
    'D': {'H': 2},
    'E': {},
    'F': {'I': 6},
    'G': {},
    'H': {},
    'I': {}
}

heuristic = {'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 7, 'F': 3, 'G': 6, 'H': 2, 'I': 0}

time_windows = {
    'A': (0, 60),  # No strict deadline
    'B': (10, 30),  # Must be delivered between 10-30 minutes
    'C': (5, 20),   
    'D': (15, 40),
    'E': (25, 50),
    'F': (10, 25),
    'G': (30, 60),
    'H': (20, 35),
    'I': (0, 60)  
}

def greedy_bfs(graph, start, goal, time_windows):
    
    frontier = [(start, heuristic[start], 0)]  # (node, heuristic, current_time)
    visited = set()
    came_from = {start: None}
    
    while frontier:
        frontier.sort(key=lambda x: (x[1], time_windows[x[0]][1]))  # Prioritize stricter deadlines
        current_node, _, current_time = frontier.pop(0)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        print(f"Visited: {current_node} (Time: {current_time} minutes)")
        
        window_start, window_end = time_windows[current_node]
        if not (window_start <= current_time <= window_end):
            print(f"Missed time window for {current_node}. Skipping...")
            continue
        
        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"\nGoal reached! Optimal path: {' -> '.join(path)}")
            print(f"Total travel time: {current_time} minutes")
            return path
        
        for neighbor, travel_time in graph[current_node].items():
            if neighbor not in visited:
                new_time = current_time + travel_time
                came_from[neighbor] = current_node
                frontier.append((neighbor, heuristic[neighbor], new_time))
    
    print("\nGoal not reachable within time constraints.")
    return None

print("Starting Delivery Route Optimization with Time Windows...")
greedy_bfs(delivery_graph, 'A', 'I', time_windows)