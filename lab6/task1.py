
"""
a) CSP Problem Definition:
Variables:

Each grid cell (i,j) where i ∈ {0,4}, j ∈ {0,4} represents a position the robot could be in

Domains:

For each cell: {0,1} where 0 means not part of path, 1 means part of path

For movement variables: {top-left, top-right, bottom-left, bottom-right}

Constraints:

Path must start at (1,1) and end at (4,4)

Robot can only move diagonally

Cannot move through obstacles

Path must be continuous (no jumps)

Each cell can be visited at most once (no cycles)
"""


from ortools.sat.python import cp_model
import math

def solve_robot_path():
    grid_size = 5
    start = (1, 1)
    target = (4, 4)
    obstacles = []

    model = cp_model.CpModel()

    in_path = {
        (i, j): model.NewBoolVar(f'path_{i}_{j}')
        for i in range(grid_size)
        for j in range(grid_size)
    }

    moves = {}
    for i in range(grid_size):
        for j in range(grid_size):
            for di, dj in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < grid_size and 0 <= nj < grid_size:
                    moves[(i,j), (ni,nj)] = model.NewBoolVar(f'move_{i}_{j}_to_{ni}_{nj}')

    model.Add(in_path[start] == 1)
    model.Add(in_path[target] == 1)

    for (i,j) in obstacles:
        model.Add(in_path[(i,j)] == 0)

    for i in range(grid_size):
        for j in range(grid_size):
            incoming = []
            outgoing = []
            for (from_pos, to_pos), var in moves.items():
                if to_pos == (i,j):
                    incoming.append(var)
                if from_pos == (i,j):
                    outgoing.append(var)
            
            if (i,j) == start:
                model.Add(sum(outgoing) == 1)
            elif (i,j) == target:
                model.Add(sum(incoming) == 1)
            else:
                model.Add(sum(incoming) == in_path[(i,j)])
                model.Add(sum(outgoing) == in_path[(i,j)])

    cost = sum(round(math.sqrt(2) * 100) * var for move, var in moves.items())
    model.Minimize(cost)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        path = []
        current = start
        path.append(current)
        visited = set([current])
        
        while current != target:
            found_move = False
            for (from_pos, to_pos), var in moves.items():
                if from_pos == current and solver.Value(var) == 1 and to_pos not in visited:
                    path.append(to_pos)
                    visited.add(to_pos)
                    current = to_pos
                    found_move = True
                    break
            
            if not found_move:
                break
        
        for step, pos in enumerate(path):
            print(f"Step {step}: {pos}")
        
        print(f"Total cost: {solver.ObjectiveValue()/100:.2f}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    solve_robot_path()