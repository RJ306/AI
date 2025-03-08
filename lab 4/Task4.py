import heapq
import threading
import random
import time

city_map = {
    'A': {'B': 4, 'C': 3},
    'B': {'E': 12, 'F': 5},
    'C': {'D': 7, 'E': 10},
    'D': {'E': 2},
    'E': {'G': 5},
    'F': {'G': 16},
    'G': {}
}

heuristic = {'A': 14, 'B': 12, 'C': 11, 'D': 6, 'E': 4, 'F': 11, 'G': 0}

def a_star_dynamic_traffic(graph, start, goal):
    
    frontier = []
    heapq.heappush(frontier, (heuristic[start], 0, start, []))  # (f_cost, g_cost, node, path)
    visited = set()
    
    while frontier:
        f_cost, g_cost, current, path = heapq.heappop(frontier)
        
        if current in visited:
            continue
        
        visited.add(current)
        path = path + [current]
        
        print(f"Exploring node: {current} with path: {' -> '.join(path)}")
        
        if current == goal:
            print(f"\nGoal reached! Optimal path: {' -> '.join(path)}")
            return path
        
        for neighbor, travel_time in graph[current].items():
            if neighbor not in visited:
                new_g_cost = g_cost + travel_time
                f_cost = new_g_cost + heuristic[neighbor]
                heapq.heappush(frontier, (f_cost, new_g_cost, neighbor, path))
    
    print("\nGoal not reachable with current traffic conditions.")
    return None

def simulate_traffic_updates(graph):
  
    while True:
        time.sleep(random.randint(2, 5))  # Simulate traffic updates every 2-5 seconds
        node = random.choice(list(graph.keys()))
        if graph[node]:
            neighbor = random.choice(list(graph[node].keys()))
            new_travel_time = random.randint(1, 20)  # Random traffic congestion
            graph[node][neighbor] = new_travel_time
            print(f"Traffic update: {node} -> {neighbor} now takes {new_travel_time} minutes.")

def restart_search(graph, start, goal):
   
    while True:
        time.sleep(5)  
        print("\nRestarting A* search due to traffic changes...")
        a_star_dynamic_traffic(graph, start, goal)

traffic_thread = threading.Thread(target=simulate_traffic_updates, args=(city_map,), daemon=True)
traffic_thread.start()

search_thread = threading.Thread(target=restart_search, args=(city_map, 'A', 'G'), daemon=True)
search_thread.start()

# Keep the main thread alive to allow background threads to run
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation stopped.")