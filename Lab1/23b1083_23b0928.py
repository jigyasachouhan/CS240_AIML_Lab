import numpy as np
from collections import deque
import heapq
from typing import List, Tuple, Set, Dict
"""
Do not import any other package unless allowed by te TAs in charge of the lab.
Do not change the name of any of the functions below.
"""

class state:
    def __init__(self, parent, board, cost, dir, steps):
        self.parent = parent
        # self.visited = visited
        self.board = board
        self.cost = cost
        self.dir = dir
        self.steps = steps
        
    def __lt__(self, other):
        return self.cost < other.cost      
        
def bfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    """
    Implement Breadth-First Search algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array.
                            Example: np.array([[1, 2, 3], [4, 0, 5], [6, 7, 8]])
                            where 0 represents the blank space
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array.
                          Example: np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    
    Returns:
        Tuple[List[str], int]: A tuple containing:
            - List of moves to reach the goal state. Each move is represented as
              'U' (up), 'D' (down), 'L' (left), or 'R' (right), indicating how
              the blank space should move
            - Number of nodes expanded during the search

    Example return value:
        (['R', 'D', 'R'], 12) # Means blank moved right, down, right; 12 nodes were expanded
              
    """
    open = []
    closed = set()
    seq = []
    nodes = 0
    
    initial_state = state(None, initial, 0, '', 0)
    heapq.heappush(open, initial_state)
    
    while open:
        top = heapq.heappop(open)
        closed.add(tuple(map(tuple, top.board)))
        nodes += 1
        
        eq = np.array_equal(top.board, goal)
        if eq:
            curr = top
            while curr.dir!='':
                seq.append(curr.dir)
                curr = curr.parent
            seq = seq[::-1]
            return (seq, nodes)
        
        row, col = np.where(top.board==0)
        row = row[0]
        col = col[0]
                            
        if row-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row-1][col]
            adj[row-1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'U', top.steps+1))
                # parent[adj.flatten()] = top.flatten() # up
                # dir[[top, adj]] = 'U'
            
        if col+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row][col+1]
            adj[row][col+1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'R', top.steps+1))
                # parent[adj] = top # right
                # dir[[top, adj]] = 'R'
                
        if row+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row+1][col]
            adj[row+1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'D', top.steps+1))
                # parent[adj] = top # down
                # dir[[top, adj]] = 'D'
                
        if col-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row][col-1]
            adj[row][col-1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'L', top.steps+1))
                # parent[adj] = top # left
                # dir[[top, adj]] = 'L'
                
    return ([], 0)
    
def dfs(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int]:
    """
    Implement Depth-First Search algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
    """
    # TODO: Implement this function
    open = []
    closed = set()
    seq = []
    nodes = 0
    
    initial_state = state(None, initial, 1, '', 0)
    heapq.heappush(open, initial_state)
    
    while open:
        top = heapq.heappop(open)
        closed.add(tuple(map(tuple, top.board)))
        nodes += 1
        
        eq = np.array_equal(top.board, goal)
        if eq:
            curr = top
            while curr.dir!='':
                seq.append(curr.dir)
                curr = curr.parent
            seq = seq[::-1]
            return (seq, nodes)
        
        row, col = np.where(top.board==0)
        row = row[0]
        col = col[0]
                            
        if row-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row-1][col]
            adj[row-1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, 1/(top.steps+1), 'U', top.steps+1))
                # parent[adj.flatten()] = top.flatten() # up
                # dir[[top, adj]] = 'U'
            
        if col+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row][col+1]
            adj[row][col+1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, 1/(top.steps+1), 'R', top.steps+1))
                # parent[adj] = top # right
                # dir[[top, adj]] = 'R'
                
        if row+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row+1][col]
            adj[row+1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, 1/(top.steps+1), 'D', top.steps+1))
                # parent[adj] = top # down
                # dir[[top, adj]] = 'D'
                
        if col-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row][col-1]
            adj[row][col-1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, 1/(top.steps+1), 'L', top.steps+1))
                # parent[adj] = top # left
                # dir[[top, adj]] = 'L'
                
    return ([], 0)

def dijkstra(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement Dijkstra's algorithm to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
            
    """
    # TODO: Implement this function
    open = []
    closed = set()
    seq = []
    nodes = 0
    
    initial_state = state(None, initial, 0, '', 0)
    heapq.heappush(open, initial_state)
    
    while open:
        top = heapq.heappop(open)
        closed.add(tuple(map(tuple, top.board)))
        nodes += 1
        
        eq = np.array_equal(top.board, goal)
        if eq:
            curr = top
            while curr.dir!='':
                seq.append(curr.dir)
                curr = curr.parent
            seq = seq[::-1]
            return (seq, nodes, top.cost)
        
        row, col = np.where(top.board==0)
        row = row[0]
        col = col[0]
                            
        if row-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row-1][col]
            adj[row-1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'U', top.steps+1))
                # parent[adj.flatten()] = top.flatten() # up
                # dir[[top, adj]] = 'U'
            
        if col+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row][col+1]
            adj[row][col+1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'R', top.steps+1))
                # parent[adj] = top # right
                # dir[[top, adj]] = 'R'
                
        if row+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row+1][col]
            adj[row+1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'D', top.steps+1))
                # parent[adj] = top # down
                # dir[[top, adj]] = 'D'
                
        if col-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row][col-1]
            adj[row][col-1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, top.steps+1, 'L', top.steps+1))
                # parent[adj] = top # left
                # dir[[top, adj]] = 'L'
                
    return ([], 0, 0)

def md(curr: np.ndarray, goal: np.ndarray) -> int:
    ans = 0
    for curr_r in range(3):
        for curr_c in range(3):
            if curr[curr_r][curr_c] == 0:
                continue
            goal_r, goal_c = np.where(goal==curr[curr_r][curr_c])
            goal_r = goal_r[0]
            goal_c = goal_c[0]
            dist = abs(goal_r - curr_r) + abs(goal_c - curr_c)
            ans += dist
    
    return ans

def dt(curr: np.ndarray, goal: np.ndarray) -> int:
    ans = 0
    for r in range(3):
        for c in range(3):
            if(curr[r][c]==0):
                continue
            if curr[r][c] != goal[r][c]: 
                ans = ans + 1
            
    return ans

def astar_dt(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Displaced Tiles heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
    """
    open = []
    closed = set()
    seq = []
    nodes = 0
    
    initial_state = state(None, initial, dt(initial, goal), '', 0)
    heapq.heappush(open, initial_state)
    
    while open:
        top = heapq.heappop(open)
        closed.add(tuple(map(tuple, top.board)))
        nodes += 1
        
        eq = np.array_equal(top.board, goal)
        if eq:
            curr = top
            while curr.dir!='':
                seq.append(curr.dir)
                curr = curr.parent
            seq = seq[::-1]
            return (seq, nodes, top.cost)
        
        row, col = np.where(top.board==0)
        row = row[0]
        col = col[0]
                            
        if row-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row-1][col]
            adj[row-1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, dt(adj, goal)+top.steps+1, 'U', top.steps+1))
                # parent[adj.flatten()] = top.flatten() # up
                # dir[[top, adj]] = 'U'
            
        if col+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row][col+1]
            adj[row][col+1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, dt(adj, goal)+top.steps+1, 'R', top.steps+1))
                # parent[adj] = top # right
                # dir[[top, adj]] = 'R'
                
        if row+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row+1][col]
            adj[row+1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, dt(adj, goal)+top.steps+1, 'D', top.steps+1))
                # parent[adj] = top # down
                # dir[[top, adj]] = 'D'
                
        if col-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row][col-1]
            adj[row][col-1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, dt(adj, goal)+top.steps+1, 'L', top.steps+1))
                # parent[adj] = top # left
                # dir[[top, adj]] = 'L'
    
    return ([], 0, 0)
        
def astar_md(initial: np.ndarray, goal: np.ndarray) -> Tuple[List[str], int, int]:
    """
    Implement A* Search with Manhattan Distance heuristic to solve 8-puzzle problem.
    
    Args:
        initial (np.ndarray): Initial state of the puzzle as a 3x3 numpy array
        goal (np.ndarray): Goal state of the puzzle as a 3x3 numpy array
    
    Returns:
        Tuple[List[str], int, int]: A tuple containing:
            - List of moves to reach the goal state
            - Number of nodes expanded during the search
            - Total cost of the path for transforming initial into goal configuration
    """
    # TODO: Implement this function
    open = []
    closed = set()
    seq = []
    nodes = 0
    
    initial_state = state(None, initial, md(initial, goal), '', 0)
    heapq.heappush(open, initial_state)
    
    while open:
        top = heapq.heappop(open)
        closed.add(tuple(map(tuple, top.board)))
        nodes += 1
        
        eq = np.array_equal(top.board, goal)
        if eq:
            curr = top
            while curr.dir!='':
                seq.append(curr.dir)
                curr = curr.parent
            seq = seq[::-1]
            return (seq, nodes, top.cost)
        
        row, col = np.where(top.board==0)
        row = row[0]
        col = col[0]
                            
        if row-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row-1][col]
            adj[row-1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, md(adj, goal)+top.steps+1, 'U', top.steps+1))
                # parent[adj.flatten()] = top.flatten() # up
                # dir[[top, adj]] = 'U'
            
        if col+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row][col+1]
            adj[row][col+1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, md(adj, goal)+top.steps+1, 'R', top.steps+1))
                # parent[adj] = top # right
                # dir[[top, adj]] = 'R'
                
        if row+1<3:
            adj = top.board.copy()
            adj[row][col] = adj[row+1][col]
            adj[row+1][col] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, md(adj, goal)+top.steps+1, 'D', top.steps+1))
                # parent[adj] = top # down
                # dir[[top, adj]] = 'D'
                
        if col-1>=0:
            adj = top.board.copy()
            adj[row][col] = adj[row][col-1]
            adj[row][col-1] = 0
            adj_tuple = tuple(map(tuple, adj))
            if adj_tuple not in closed:
                heapq.heappush(open, state(top, adj, md(adj, goal)+top.steps+1, 'L', top.steps+1))
                # parent[adj] = top # left
                # dir[[top, adj]] = 'L'
                
    return ([], 0, 0)


# Example test case to help verify your implementation
if __name__ == "__main__":
    # Example puzzle configuration
    initial_state = np.array([
        [1, 2, 3],
        [4, 0, 5],
        [6, 7, 8]
    ])
    
    # initial_state = np.array([
    #     [6, 8, 7],
    #     [2, 5, 4],
    #     [3, 0, 1]
    # ])
    
    
    goal_state = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ])
    
    # Test each algorithm
    print("Testing BFS...")
    bfs_moves, bfs_expanded = bfs(initial_state, goal_state)
    print(f"BFS Solution: {bfs_moves}")
    print(f"Nodes expanded: {bfs_expanded}")
    
    print("\nTesting DFS...")
    dfs_moves, dfs_expanded = dfs(initial_state, goal_state)
    print(f"DFS Solution: {dfs_moves}")
    print(f"Nodes expanded: {dfs_expanded}")
    
    print("\nTesting Dijkstra...")
    dijkstra_moves, dijkstra_expanded, dijkstra_cost = dijkstra(initial_state, goal_state)
    print(f"Dijkstra Solution: {dijkstra_moves}")
    print(f"Nodes expanded: {dijkstra_expanded}")
    print(f"Total cost: {dijkstra_cost}")
    
    print("\nTesting A* with Displaced Tiles...")
    dt_moves, dt_expanded, dt_fscore = astar_dt(initial_state, goal_state)
    print(f"A* (DT) Solution: {dt_moves}")
    print(f"Nodes expanded: {dt_expanded}")
    print(f"Total cost: {dt_fscore}")
    
    print("\nTesting A* with Manhattan Distance...")
    md_moves, md_expanded, md_fscore = astar_md(initial_state, goal_state)
    print(f"A* (MD) Solution: {md_moves}")
    print(f"Nodes expanded: {md_expanded}")
    print(f"Total cost: {md_fscore}")