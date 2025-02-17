# Example Tree
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['A'], 
    'E': ['F'],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': ['E'] 
}

def dls(node, goal, depth, path, visited):
    if depth == 0:
        return False
    if node == goal:
        path.append(node)
        return True
    if node in visited:
        return False  
    visited.add(node)
    
    if node not in tree and node not in graph:
        return False
    
    children = tree.get(node, []) if node in tree else graph.get(node, [])
    
    for child in children:
        if dls(child, goal, depth - 1, path, visited):
            path.append(node) 
            return True
    
    return False

def id(start, goal, max_depth, graph_or_tree):
    print(f"Searching in {'Graph' if graph_or_tree == 'graph' else 'Tree'}")
    for depth in range(max_depth + 1):
        print(f"Depth: {depth}")
        path = []
        visited = set()  
        if dls(start, goal, depth, path, visited):
            print("\nPath to goal:", " → ".join(reversed(path)))  
            return
    print("Goal not found within depth limit.")

start_node = 'A'
goal_node = 'I'
search_depth = 5
id(start_node, goal_node, search_depth, 'tree')

print("\n" "\n")  
id(start_node, goal_node, search_depth, 'graph')
