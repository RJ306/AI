
import random

class LoadBalancerAgent:
    def __init__(self, percept):
        self.percepts = percept

    def act(self):
        underloaded_servers = [percept for percept, load in self.percepts.items() if load == 'U']
        overloaded_servers = [percept for percept, load in self.percepts.items() if load == 'O']

        if overloaded_servers and underloaded_servers:
            for overloaded in overloaded_servers:
                task_to_move = 1  # Move one task
                underloaded = underloaded_servers.pop(0)  
                print(f"Moving 1 task from {overloaded} to {underloaded} to balance the load.")
                
                self.percepts[overloaded] = 'B'  
                self.percepts[underloaded] = 'B'  
            
                underloaded_servers.append(underloaded)
                
        else:
            print("No load balancing needed.")

    def display_servers(self):
        print("\nUpdated load status of each server:")
        for server, load in self.percepts.items():
            print(f"{server}: {load}")


class Environment:
    def __init__(self):
        # Initialize servers with load states, U = Underloaded, B = Balanced, O = Overloaded
        self.servers = {
            'Server 1': 'U',
            'Server 2': 'B',
            'Server 3': 'U',
            'Server 4': 'O',
            'Server 5': 'O',
        }

    def get_percept(self):
        return self.servers


def run_agent(agent, environment):
    print("Initial load status of each server:")
    for server, load in environment.get_percept().items():
        print(f"{server}: {load}")
    
    agent.act()
    agent.display_servers()


# Create instances of environment and load balancer agent
environment = Environment()
agent = LoadBalancerAgent(environment.get_percept())

# Run the load balancer in the environment
run_agent(agent, environment)
