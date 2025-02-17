from collections import deque

class Environment:
    def __init__(self, grid):
        self.grid = grid

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]) and self.grid[nx][ny] != 1:
                neighbors.append((nx, ny))
        
        return neighbors
        
class Agent:
    def __init__(self, start, goal, environment):
        self.current_node = start
        self.goal = goal
        self.visited = set()
        self.parent_map = {}
        self.environment = environment
        
    def run_agent(self):
        queue = deque([self.current_node])
        self.visited.add(self.current_node)
        
        while queue:
            node = queue.popleft()
            print(f"Visited: {node}")
            
            if node == self.goal:
                print("Goal found!")
                break
            
            for neighbor in self.environment.get_neighbors(node):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append(neighbor)
                    self.parent_map[neighbor] = node
        
        
        path = self.reconstruct_path()
        print("\nPath to goal:", path)
    
    def reconstruct_path(self):
        path = []
        node = self.goal
        while node != self.current_node:
            path.append(node)
            node = self.parent_map[node]
        path.append(self.current_node)
        return path[::-1] 
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)  
goal = (4, 4) 

env = Environment(grid)
agent = Agent(start, goal, env)

agent.run_agent()
