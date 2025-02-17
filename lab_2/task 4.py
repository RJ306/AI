import random

class Environment:
    def __init__(self):
        self.components = {
            'Comp 1': 'Safe',
            'Comp 2': 'High Risk Vulnerable',
            'Comp 3': 'Low Risk Vulnerable',
            'Comp 4': 'Safe',
            'Comp 5': 'High Risk Vulnerable',
            'Comp 6': 'High Risk Vulnerable',
            'Comp 7': 'Low Risk Vulnerable',
            'Comp 8': 'Safe',
            'Comp 9': 'Low Risk Vulnerable',

        }

    def get_percept(self):
        return self.components

    def patch_low_risk(self):
        for step in self.components:
            if self.components[step] == 'Low Risk Vulnerable':
                self.components[step] = 'Safe'

class SecurityRiskAgent:
    def act(self, percept):
        for s,component in percept.items():
            if component == 'Safe':
                print('Safe!!')
            elif component == 'Low Risk Vulnerable':
                print('WARNING!! Low Risk Vulnerable. Patching...')
            else:
                print('WARNING!! High Risk Vulnerable. Premium service needed!')

def run_agent(agent, environment):
    print("Initial System State:")
    for component, status in environment.get_percept().items():
        print(f'{component}: {status}')
    print()
    
    print("System Scan:")
    agent.act(environment.get_percept())
    print()
    
    print("Patching Vulnerabilities:")
    environment.patch_low_risk()
    print()
    
    print("Final System State:")
    for component, status in environment.get_percept().items():
        print(f'{component}: {status}')

# Create instances
environment = Environment()
agent = SecurityRiskAgent()

# Run the simulation
run_agent(agent, environment)
