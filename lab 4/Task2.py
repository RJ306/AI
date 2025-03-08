import heapq
import threading
import random
import time

graph = {
    'A': {'B': 4, 'C': 3},
    'B': {'E': 12, 'F': 5},
    'C': {'D': 7, 'E': 10},
    'D': {'E': 2},
    'E': {'G': 5},
    'F': {'G': 16},
    'G': {}
}

heuristic = {'A': 14, 'B': 12, 'C': 11, 'D': 6, 'E': 4, 'F': 11, 'G': 0}

def a_star(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (heuristic[start], 0, start, None))
    g_costs = {start: 0}
    came_from = {start: None}
    visited = set()
    
    while frontier:
        _, g_cost, current, parent = heapq.heappop(frontier)
        
        if current in visited:
            continue
        
        visited.add(current)
        came_from[current] = parent
        
        print(current, end=" ")
        
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            print(f"\nGoal found with A*. Path: {path}")
            return
        
        for neighbor, cost in graph[current].items():
            new_g_cost = g_cost + cost
            f_cost = new_g_cost + heuristic[neighbor]
            
            if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = new_g_cost
                heapq.heappush(frontier, (f_cost, new_g_cost, neighbor, current))
    
    print("\nGoal not found")

def update_edge_costs(graph):
    while True:
        time.sleep(random.randint(3, 6))
        node = random.choice(list(graph.keys()))
        if graph[node]:
            neighbor = random.choice(list(graph[node].keys()))
            new_cost = random.randint(1, 20)
            graph[node][neighbor] = new_cost
            print(f"\nEdge cost updated: {node} -> {neighbor} = {new_cost}")

threading.Thread(target=update_edge_costs, args=(graph,), daemon=True).start()

print("\nFollowing is the dynamic A* Search:")
a_star(graph, 'A', 'G')