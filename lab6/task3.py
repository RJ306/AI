from ortools.sat.python import cp_model
import numpy as np
import time

def solve_tsp(distances, time_limit=10):
    num_cities = len(distances)
    all_cities = range(num_cities)
    
    model = cp_model.CpModel()
    
    next_city = [model.NewIntVar(0, num_cities - 1, f'next_{i}') for i in all_cities]
    arcs = []
    for i in all_cities:
        for j in all_cities:
            if i != j:
                arcs.append((i, j, model.NewBoolVar(f'arc_{i}_{j}')))
    
    for i in all_cities:
        model.Add(sum(arc[2] for arc in arcs if arc[0] == i) == 1)  # Outgoing
        model.Add(sum(arc[2] for arc in arcs if arc[1] == i) == 1)  # Incoming
    
    for i in all_cities:
        model.Add(next_city[i] == sum(j * arcs[i*num_cities + j - (i+1 if j < i else i)][2] 
                 for j in all_cities if j != i))
    
    
    total_distance = model.NewIntVar(0, 1000000, 'total_distance')
    model.Add(total_distance == sum(distances[i][j] * arcs[i*num_cities + j - (i+1 if j < i else i)][2] 
             for i in all_cities for j in all_cities if i != j))
    model.Minimize(total_distance)
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        tour = [0]
        current = 0
        for _ in range(num_cities - 1):
            current = solver.Value(next_city[current])
            tour.append(current)
        return tour, solver.ObjectiveValue()
    return None, None

np.random.seed(42)
num_cities = 10
coords = np.random.rand(num_cities, 2) * 100
distances = np.zeros((num_cities, num_cities), dtype=int)
for i in range(num_cities):
    for j in range(num_cities):
        distances[i][j] = int(np.linalg.norm(coords[i] - coords[j]))

print("Starting TSP solver...")
start_time = time.time()
tour, distance = solve_tsp(distances, time_limit=30)  # 30 second limit

if tour:
    print(f"\nFound solution in {time.time()-start_time:.2f} seconds")
    print("Optimal Tour:", tour)
    print("Total Distance:", distance)
    print("\nCity Coordinates:")
    for i, (x, y) in enumerate(coords):
        print(f"City {i}: ({x:.1f}, {y:.1f})")
else:
    print("\nNo solution found within time limit")