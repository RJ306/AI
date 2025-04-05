
"""
a) CSP Model Definition
Variables:

robot_position[r][t]: (x,y) position of robot r at time t

robot_battery[r][t]: Battery level of robot r at time t

robot_load[r][t]: Current load of robot r at time t

package_status[p][t]: Status of package p at time t (0=waiting, 1=in transit, 2=delivered)

package_carrier[p][t]: Robot assigned to package p at time t (-1 if none)

action[r][t]: Action taken by robot r at time t (move, pick-up, deliver, charge)

Domains:

Positions: Grid coordinates (0≤x<6, 0≤y<6)

Battery: Integer (0-100%)

Load: Integer (0 to robot capacity)

Package status: {0,1,2}

Package carrier: {-1} ∪ robot IDs

Actions: {'move-N', 'move-S', 'move-E', 'move-W', 'pick-up', 'deliver', 'charge'}

Constraints:

Movement Constraints:

Robots can only move to adjacent cells

Robots cannot move outside grid boundaries

No two robots can occupy same cell simultaneously

Battery Constraints:

Moving consumes battery (5% per move)

Charging restores battery (20% per time unit at charging station)

Robots must maintain ≥10% battery

Load Constraints:

Pick-up only if robot has sufficient capacity

Deliver only when at destination

Load cannot exceed capacity

Package Constraints:

Each package must be delivered exactly once

Packages can only be picked up from their origin

Packages can only be delivered to their destination

Objective:

Minimize total delivery time (last delivery completion time)
"""
from ortools.sat.python import cp_model
import numpy as np

def warehouse_robots():
    size = 6
    robots = 2
    packages = 2
    steps = 5
    
    model = cp_model.CpModel()
    
    cap = [10, 15]
    start = [(0,0), (5,5)]
    
    pkg_w = [2, 3]
    pkg_from = [(1,1), (4,4)]
    pkg_to = [(5,5), (0,0)]
    
    pos = {}
    act = {}
    flags = {}  
    carry = {}      
    
    for r in range(robots):
        for t in range(steps):
            pos[(r,t)] = (
                model.NewIntVar(0, size-1, f'x{r}_{t}'),
                model.NewIntVar(0, size-1, f'y{r}_{t}')
            )
            
            act[(r,t)] = model.NewIntVar(0, 6, f'a{r}_{t}')
            
            flags[(r,t)] = {
                'none': model.NewBoolVar(f'n{r}_{t}'),
                'N': model.NewBoolVar(f'N{r}_{t}'),
                'S': model.NewBoolVar(f'S{r}_{t}'),
                'E': model.NewBoolVar(f'E{r}_{t}'),
                'W': model.NewBoolVar(f'W{r}_{t}'),
                'pick': model.NewBoolVar(f'p{r}_{t}'),
                'drop': model.NewBoolVar(f'd{r}_{t}')
            }
            
            for i, a in enumerate(['none', 'N', 'S', 'E', 'W', 'pick', 'drop']):
                model.Add(act[(r,t)] == i).OnlyEnforceIf(flags[(r,t)][a])
                model.Add(act[(r,t)] != i).OnlyEnforceIf(flags[(r,t)][a].Not())
            
            carry[(r,t)] = model.NewIntVar(-1, packages-1, f'c{r}_{t}')
    
    for r in range(robots):
        model.Add(pos[(r,0)][0] == start[r][0])
        model.Add(pos[(r,0)][1] == start[r][1])
        model.Add(act[(r,0)] == 0)
        model.Add(carry[(r,0)] == -1)
        model.Add(flags[(r,0)]['none'] == 1)
    
    for t in range(1, steps):
        for r in range(robots):
            px, py = pos[(r,t-1)]
            cx, cy = pos[(r,t)]
            
            model.Add(cy == py - 1).OnlyEnforceIf(flags[(r,t-1)]['N'])
            model.Add(cy == py + 1).OnlyEnforceIf(flags[(r,t-1)]['S'])
            model.Add(cx == px + 1).OnlyEnforceIf(flags[(r,t-1)]['E'])
            model.Add(cx == px - 1).OnlyEnforceIf(flags[(r,t-1)]['W'])
            
            no_move = [
                flags[(r,t-1)]['none'],
                flags[(r,t-1)]['pick'],
                flags[(r,t-1)]['drop']
            ]
            model.Add(cx == px).OnlyEnforceIf(sum(no_move) >= 1)
            model.Add(cy == py).OnlyEnforceIf(sum(no_move) >= 1)
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        names = ['none', 'N', 'S', 'E', 'W', 'pick', 'drop']
        print("Solution:")
        for t in range(steps):
            print(f"\nStep {t}:")
            for r in range(robots):
                x = solver.Value(pos[(r,t)][0])
                y = solver.Value(pos[(r,t)][1])
                a = solver.Value(act[(r,t)])
                c = solver.Value(carry[(r,t)])
                print(f"R{r}: ({x},{y}) {names[a]}, Carrying: {f'Pkg {c}' if c != -1 else '-'}")
    else:
        print("No solution")

if __name__ == "__main__":
    warehouse_robots()