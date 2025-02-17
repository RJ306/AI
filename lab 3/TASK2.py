import itertools

class Environment:
    def __init__(self, graph, start_node):
        self.graph = graph
        self.current_node = start_node

    def get_neighbors(self):
        return self.graph[self.current_node]

    def move_agent(self, next_node):
        if next_node in self.graph[self.current_node]:
            self.current_node = next_node
            return f"Agent moved to {next_node}"
        else:
            return f"Move to {next_node} is not possible"

class UtilityBasedAgent:
    def __init__(self, goal):
        self.goal = goal

    def select_action(self, current_node, neighbors):
        if self.goal in neighbors:
            return f"Move to {self.goal} (goal found)"
        else:
            return f"Explore neighbors of {current_node}"

    def act(self, environment):
        current_node = environment.current_node
        neighbors = environment.get_neighbors()
        action = self.select_action(current_node, neighbors)
        return action

def TSP(graph, start):
    cities = list(graph.keys())
    cities.remove(start)
    permutations = itertools.permutations(cities)
    
    min_cost = float('inf')
    best_path = None
    
    for perm in permutations:
        path = [start] + list(perm) + [start]
        cost = 0
        for i in range(len(path) - 1):
            cost += graph[path[i]].get(path[i + 1], float('inf'))
        
        if cost < min_cost:
            min_cost = cost
            best_path = path
    
    if best_path is None:
        print("No path found.")
        return None, None
    
    return best_path, min_cost

graph = {
    '1': {'2': 10, '4': 20, '3': 15},
    '2': {'1': 10, '3': 35, '4': 25},
    '3': {'1': 15, '2': 35, '4': 30},
    '4': {'1': 20, '2': 25, '3': 30}
}

env = Environment(graph, '1')
agent = UtilityBasedAgent('3')

while True:
    action = agent.act(env)
    print(action)
    if "goal found" in action:
        break
    next_node = env.get_neighbors().pop(0)
    env.move_agent(next_node)

path, cost = TSP(graph, '1')
if path:
    print(f"Shortest path: {path}, Total cost: {cost}")
else:
    print("No path found.")
