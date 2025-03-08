from queue import PriorityQueue
from itertools import permutations

class N:
    def __init__(self, pos, par=None):
        self.pos = pos
        self.par = par
        self.g = 0  
        self.h = 0 
        self.f = 0 

    def __lt__(self, o):
        return self.f < o.f


def h_cost(c_pos, e_pos):
    return abs(c_pos[0] - e_pos[0]) + abs(c_pos[1] - e_pos[1])


def bfs(maze, s, e):
    r, c = len(maze), len(maze[0])
    s_n, e_n = N(s), N(e)
    pq = PriorityQueue()
    pq.put(s_n)
    vis = set()

    while not pq.empty():
        c_n = pq.get()
        c_pos = c_n.pos

        if c_pos == e:
            p = []
            while c_n:
                p.append(c_n.pos)
                c_n = c_n.par
            return p[::-1]  
        vis.add(c_pos)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            n_pos = (c_pos[0] + dx, c_pos[1] + dy)
            if (0 <= n_pos[0] < r and 0 <= n_pos[1] < c and
                    maze[n_pos[0]][n_pos[1]] == 0 and n_pos not in vis):
                n_n = N(n_pos, c_n)
                n_n.g = c_n.g + 1
                n_n.h = h_cost(n_pos, e)
                n_n.f = n_n.h 
                pq.put(n_n)
                vis.add(n_pos)
    
    return None 


def shortest_path(maze, s, g):
    sh_p, sh_l = None, float('inf')
    
    for perm in permutations(g):
        c_s, t_p, t_l = s, [], 0
        for goal in perm:
            p = bfs(maze, c_s, goal)
            if p is None:
                break
            t_l += len(p) - 1
            t_p.extend(p if not t_p else p[1:])
            c_s = goal
        
        if p and t_l < sh_l:
            sh_l = t_l
            sh_p = t_p
    
    return sh_p

maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

s = (0, 0)
g = [(4, 4), (3, 3), (3, 1)] 
p = shortest_path(maze, s, g)
if p:
    print("Shortest path visiting all goals:", p)
else:
    print("No path found")