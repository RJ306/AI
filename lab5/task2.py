
import random
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1)) + distance(route[-1], route[0])

def hill_climb_tsp(points):
    current_route = points[:]
    random.shuffle(current_route) 
    current_distance = total_distance(current_route)
    
    for _ in range(10000): 
        i, j = random.sample(range(len(points)), 2)
        new_route = current_route[:]
        new_route[i], new_route[j] = new_route[j], new_route[i]  # Swap two cities
        new_distance = total_distance(new_route)
        
        if new_distance < current_distance: 
            current_route, current_distance = new_route, new_distance
    
    return current_route, current_distance

points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]

best_route, best_dist = hill_climb_tsp(points)
print("Best Route:", best_route)
print("Total Distance:", best_dist)
