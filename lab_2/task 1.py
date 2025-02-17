class Environment:
 def __init__(self):
  self.grid = ['S', 'V', 'V',
               'V', 'S', 'V',
               'V', 'V', 'S']
 
 def get_percept(self, position):
  return self.grid[position]
 
 def patch_component(self, position):
    self.grid[position] = "S"

 
 def display_grid(self, agent_position):
  grid_with_agent = self.grid[:] 
  for i in range(0, 9, 3):
   print(" | ".join(grid_with_agent[i:i + 3]))
   print() 



class SimpleReflexAgent:
 def __init__(self):
  self.position = 0 
  self.vulnerable_components = []
 
 def act(self, percept):
  if percept == 'V':
    self.vulnerable_components.append(self.position)
    return 'WARNING!! COMPONENT IS VULNERABLE'
  else:
   return 'SAFE!'
 
 def move(self):
  if self.position < 8:
   self.position += 1
  return self.position

def run_agent(agent, environment, steps):
 print("\nInitial State of the System:")
 environment.display_grid(agent.position) 
 for step in range(steps):
  percept = environment.get_percept(agent.position)
  action = agent.act(percept)
  print(f"Step {step + 1}: Position {agent.position} -> Percept- {percept},   {action}")
  agent.move()
 for component in agent.vulnerable_components:
    environment.patch_component(component)  # Directly pass component, no indexing needed
    print(f"Patched: Component {component} is now secure.")
 
 print("\nFinal State of the System:")
 environment.display_grid(agent.position) 



agent = SimpleReflexAgent()
environment = Environment()
run_agent(agent, environment, 9)




