class Environment:
 def __init__(self):
  self.grid = ['C', 'F', 'C',
               'C', 'F', 'F',
               'C', 'F', 'C']
 
 def get_percept(self, position):
  return self.grid[position]
 
 def failed(self, position):
    self.grid[position] = "C"

 
 def display_grid(self, agent_position):
  grid_with_agent = self.grid[:] 
  for i in range(0, 9, 3):
   print(" | ".join(grid_with_agent[i:i + 3]))
   print() 



class backup_agent:
 def __init__(self):
  self.position = 0 
 
 def act(self, percept):
  if percept == 'F':
    return 'RETRYING BACKUP!!'
  else:
    return 'BACKUP SUCCESSFUL!!'
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
  print(f" TASK {agent.position} : {action}")
  if percept =='F':
    environment.failed(agent.position)
  agent.move()
  
  
 
 print("\nFinal State of the System:")
 environment.display_grid(agent.position) 



agent = backup_agent()
environment = Environment()
run_agent(agent, environment, 9)




