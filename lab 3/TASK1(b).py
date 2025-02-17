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


def ucs(graph, start, goal):
    frontier = [(start, 0)]  # (node, cost)
    visited = set()
    cost_so_far = {start: 0}
    came_from = {start: None}

    while frontier:
        frontier.sort(key=lambda x: x[1])
        current_node, current_cost = frontier.pop(0)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == goal:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from[current_node]
            path.reverse()
            print(f"Goal found with UCS. Path: {path}, Total Cost: {current_cost}")
            return

        for neighbor, cost in graph[current_node].items():
            new_cost = current_cost + cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current_node
                frontier.append((neighbor, new_cost))

    print("Goal not found")


graph = {
    'A': {'B': 1, 'C': 2},
    'B': {'D': 4, 'E': 2},
    'C': {'F': 3, 'G': 1},
    'D': {'H': 5},
    'E': {},
    'F': {'I': 1},
    'G': {},
    'H': {},
    'I': {}
}

environment = Environment(graph, start_node='A')
agent = UtilityBasedAgent(goal='I')

action = agent.act(environment)
print(f"Agent Action: {action}")

ucs(graph, 'A','H')
