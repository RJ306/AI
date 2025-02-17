class Environment:
    def __init__(self):
        self.grid = [
            ' ', ' ', '🔥',  
            ' ', '🔥', ' ',  
            ' ', ' ', '🔥'   
        ]
    
    def get_percept(self, position):
     
        return self.grid[position]
    
    def extinguish_fire(self, position):
        self.grid[position] = ' '
    
    def display_grid(self):
        print("\nCurrent Grid State:")
        for i in range(0, len(self.grid), 3):  
            print(" | ".join(self.grid[i:i+3]))
        print()

class SimpleReflexAgent:
    def __init__(self):
        self.position = 0 
    
    def act(self, percept, environment):
        print(f"At position {self.position}: Percept: {percept}")
        
        if percept == '🔥':
            environment.extinguish_fire(self.position)
            print(f"Fire extinguished at position {self.position}.")
        else:
            print(f"Position {self.position} is safe.")
    
    def move(self):
        if self.position < len(environment.grid) - 1:
            self.position += 1
        return self.position
    


def run_agent(agent, environment, steps):
    for step in range(steps):
        percept = environment.get_percept(agent.position)
        
        agent.act(percept, environment)
        
        environment.display_grid()
        
        agent.move()

agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment, 9)
