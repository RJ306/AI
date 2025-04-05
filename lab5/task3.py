
import random
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1)) + distance(route[-1], route[0])

def create_population(points, size):
    return [random.sample(points, len(points)) for _ in range(size)]

def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]

def crossover(parent1, parent2):
    cut = random.randint(0, len(parent1) - 1)
    child = parent1[:cut] + [p for p in parent2 if p not in parent1[:cut]]
    return child

def genetic_algorithm(points, generations=1000, population_size=100):
    population = create_population(points, population_size)

    for _ in range(generations):
        population.sort(key=total_distance)

        new_population = population[:10]  
        for _ in range(population_size - 10): 
            p1, p2 = random.sample(new_population, 2)
            child = crossover(p1, p2)
            if random.random() < 0.1: 
                mutate(child)
            new_population.append(child)

        population = new_population

    return population[0], total_distance(population[0])

points = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]

best_route, best_distance = genetic_algorithm(points)
print("Best Route:", best_route)
print("Total Distance:", best_distance)
