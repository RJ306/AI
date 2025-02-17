class GoalBasedAgent:
    def __init__(self, goal):
        self.goal = goal

    def formulate_goal(self, percept):
        if percept == self.goal:
            return "Goal reached"
        return "Searching"

    def dls(self, graph, start, goal, depth_limit):
        visited = []
        
        def dfs(node, depth):
            if depth > depth_limit:
                return None
            
            visited.append(node)
            print(f"Visiting: {node}")
            
            if node == goal:
                print(f"Goal found with DLS. Path: {visited}")
                return visited
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    path = dfs(neighbor, depth + 1)
                    if path:
                        return path
            
            visited.pop()
            return None
        
        result = dfs(start, 0)
        if result is None:
            print("Goal not found within the depth limit.")
        return result

    def act(self, percept, graph, depth_limit):
        goal_status = self.formulate_goal(percept)

        if goal_status == "Goal reached":
            return f"Goal {self.goal} found!"
        else:
            return self.dls(graph, percept, self.goal, depth_limit)


class Environment:
    def __init__(self, graph):
        self.graph = graph

    def get_percept(self, node):
        return node


def run_agent(agent, environment, start_node, depth_limit):
    percept = environment.get_percept(start_node)
    action = agent.act(percept, environment.graph, depth_limit)
    print(action)


tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

start_node = 'A'
goal_node = 'I'

agent = GoalBasedAgent(goal_node)
environment = Environment(tree)

depth_limit = 3
run_agent(agent, environment, start_node, depth_limit)
