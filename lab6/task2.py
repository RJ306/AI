




from ortools.sat.python import cp_model

def compute_island_perimeter(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    model = cp_model.CpModel()
    
    
    is_boundary = [[model.NewBoolVar(f'boundary_{i}_{j}') 
                  for j in range(cols)] for i in range(rows)]
    
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:  
                neighbors = []
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors.append(grid[ni][nj] == 0)
                    else:
                        neighbors.append(True)  
                
               
                model.Add(is_boundary[i][j] == 1).OnlyEnforceIf(sum(neighbors) >= 1)
                model.Add(is_boundary[i][j] == 0).OnlyEnforceIf(sum(neighbors) == 0)
            else:
                model.Add(is_boundary[i][j] == 0)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    perimeter = 0
    boundary_cells = []
    for i in range(rows):
        for j in range(cols):
            if solver.Value(is_boundary[i][j]) == 1:
                perimeter += 1
                boundary_cells.append((i,j))
    
    return perimeter, boundary_cells

island_grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

perimeter, boundary = compute_island_perimeter(island_grid)
print(f"Perimeter length: {perimeter}")
print("Boundary cells:", boundary)