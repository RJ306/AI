"""
a) Problem Formulation as a CSP
Variables
Let grid[i][j] represent a variable for the cell in the ith row and jth column of a 9x9 Sudoku grid, where i, j ∈ {0, ..., 8}.

Domains
Each variable grid[i][j] can take a value from {1, 2, ..., 9}, unless pre-filled (then it’s fixed to the given value).

Constraints
Standard Sudoku Constraints:

Row Constraint: All numbers in a row must be unique.

Column Constraint: All numbers in a column must be unique.

3×3 Subgrid Constraint: All numbers in a 3×3 box must be unique.

New Constraints:

Diagonal Divisibility by 3:

sum(grid[i][i] for i in 0..8) % 3 == 0 (main diagonal)

sum(grid[i][8-i] for i in 0..8) % 3 == 0 (anti-diagonal)

No Adjacent Primes: No two adjacent cells (up/down/left/right) can both be prime numbers. Prime values: {2, 3, 5, 7}


"""


from ortools.sat.python import cp_model

def sudoku_solver(board):
    model = cp_model.CpModel()
    size = 9

    cells = [[model.NewIntVar(1, 9, f'c_{i}_{j}') for j in range(size)] for i in range(size)]

    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                model.Add(cells[i][j] == board[i][j])

    for i in range(size):
        model.AddAllDifferent(cells[i])
        model.AddAllDifferent([cells[j][i] for j in range(size)])

    for r in range(0, size, 3):
        for c in range(0, size, 3):
            block = [cells[r + dr][c + dc] for dr in range(3) for dc in range(3)]
            model.AddAllDifferent(block)

    diag1 = [cells[i][i] for i in range(size)]
    diag2 = [cells[i][size - 1 - i] for i in range(size)]

    sum1 = model.NewIntVar(0, 100, "d1")
    sum2 = model.NewIntVar(0, 100, "d2")

    model.Add(sum1 == sum(diag1))
    model.Add(sum2 == sum(diag2))
    model.AddModuloEquality(0, sum1, 3)
    model.AddModuloEquality(0, sum2, 3)

    primes = {2, 3, 5, 7}
    for i in range(size):
        for j in range(size):
            for dx, dy in [(0, 1), (1, 0)]:
                ni, nj = i + dx, j + dy
                if ni < size and nj < size:
                    for p1 in primes:
                        for p2 in primes:
                            b1 = model.NewBoolVar('')
                            b2 = model.NewBoolVar('')
                            model.Add(cells[i][j] != p1).OnlyEnforceIf(b1)
                            model.Add(cells[i][j] == p1).OnlyEnforceIf(b1.Not())
                            model.Add(cells[ni][nj] != p2).OnlyEnforceIf(b2)
                            model.Add(cells[ni][nj] == p2).OnlyEnforceIf(b2.Not())
                            model.AddBoolOr([b1, b2])

    solver = cp_model.CpSolver()
    result = solver.Solve(model)

    if result in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        print("\nSolved Sudoku:")
        for i in range(size):
            print([solver.Value(cells[i][j]) for j in range(size)])
    else:
        print("No solution found.")

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

sudoku_solver(grid)
