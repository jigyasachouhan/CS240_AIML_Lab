import heapq
import json
from typing import List, Tuple


class State:
    def __init__(self, state, parent, cost, steps):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.steps = steps
        
    def __lt__(self, other):
        return self.cost < other.cost  

def equal(list1, list2):
    if list1[0] == list2[0] and list1[1] == list2[1] and list1[2] == list2[2]:
        return True
    return False

def check_valid(
    state: list, max_missionaries: int, max_cannibals: int
) -> bool:  # 10 marks
    """
    Graded
    Check if a state is valid. State format: [m_left, c_left, boat_position].
    """
    
    m_left, c_left, boat_pos = state
    if m_left >= c_left and (max_missionaries-m_left) >= (max_cannibals-c_left) and (boat_pos ==0 or boat_pos==1):
        return True
    else: 
        return False

def get_neighbours(
    state: list, max_missionaries: int, max_cannibals: int
) -> List[list]:  # 10 marks
    """
    Graded
    Generate all valid neighbouring states.
    """
    
    nbrs = []
    m_left, c_left, boat_pos = state
    
    if m_left >=1:
        curr = [m_left-1, c_left, abs(boat_pos-1)]
        if(check_valid(curr, max_missionaries, max_cannibals)): 
            nbrs.append(curr)
            
    if c_left >=1:
        curr = [m_left, c_left-1, abs(boat_pos-1)]
        if(check_valid(curr, max_missionaries, max_cannibals)): 
            nbrs.append(curr)
    
    if m_left >=2:
        curr = [m_left-2, c_left, abs(boat_pos-1)]
        if(check_valid(curr, max_missionaries, max_cannibals)): 
            nbrs.append(curr)
            
    if c_left >=2:
        curr = [m_left, c_left-2, abs(boat_pos-1)]
        if(check_valid(curr, max_missionaries, max_cannibals)): 
            nbrs.append(curr)
            
    if c_left >=1 and m_left>=1:
        curr = [m_left-1, c_left-1, abs(boat_pos-1)]
        if(check_valid(curr, max_missionaries, max_cannibals)): 
            nbrs.append(curr)    
            
    return nbrs
    
def gstar(state: list, new_state: list) -> int:  # 5 marks
    """
    Graded
    The weight of the edge between state and new_state, this is the number of people on the boat.
    """
    m1, c1, bp1 = state
    m2, c2, bp2 = new_state
    return abs(m1+c1-m2-c2)

def h1(state: list) -> int:  # 3 marks
    """
    Graded
    h1 is the number of people on the left bank.
    """
    m, c, bp = state
    return(m+c)

def h2(state: list) -> int:  # 3 marks
    """
    Graded
    h2 is the number of missionaries on the left bank. 
    """
    m,c,bp = state
    return(m)

def h3(state: list) -> int:  # 3 marks
    """
    Graded
    h3 is the number of cannibals on the left bank.
    """
    return state[1]

def h4(state: list) -> int:  # 3 marks
    """
    Graded
    Weights of missionaries is higher than cannibals.
    h4 = missionaries_left * 1.5 + cannibals_left
    """
    return state[0] * 1.5 + state[1]

def h5(state: list) -> int:  # 3 marks
    """
    Graded
    Weights of missionaries is lower than cannibals.
    h5 = missionaries_left + cannibals_left*1.5
    """
    return state[0] + state[1]*1.5

def astar_h1(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 28 marks
    """
    Graded
    Implement A* with h1 heuristic.
    This function must return path obtained and a boolean which says if the heuristic chosen satisfes Monotone restriction property while exploring or not.
    """
    
    init_st = State(init_state, None, h1(init_state) + 0, 0)
    monotone = True
    open = []
    closed = set()
    closed_st = set()
    seq = []
    heapq.heappush(open, init_st)
    
    while len(open)>0:
        top = heapq.heappop(open)
        closed.add(top.state)
        closed_st.add(top)
        
        # eq = equal(top.state, final_state)
        # if eq:
        #     curr = top
        #     while curr.parent!=None:
        #         seq.append(curr.state)
        #         curr = curr.parent
        #     seq = seq[::-1]
            
        nbrs = get_neighbours(top.state, max_missionaries, max_cannibals)
        
        for nbr in nbrs:
            if nbr not in closed:
                new_st = State(nbr, top, h1(nbr) + gstar(top.state, nbr), gstar(top.state, nbr))
                heapq.heappush(open, new_st)
            else:
                for x in closed_st:
                    if equal(x.state, nbr):
                        nbr_st = x
                        break
                
                if nbr_st.steps > gstar(top.state, nbr):
                    monotone = False
                    nbr_st.parent = top
                    nbr_st.cost = h1(nbr) + gstar(top.state, nbr)
                    nbr_st.steps = gstar(top.state, nbr)
                    
    
    if final_state not in closed:
        return ([], monotone)
    
    curr = top
    while curr.parent!=None:
        seq.append(curr.state)
        curr = curr.parent
    seq = seq[::-1]
    
    return (seq, monotone)
       

def astar_h2(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h2 heuristic.
    """
    raise ValueError("astar_h2 not implemented")


def astar_h3(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h3 heuristic.
    """
    raise ValueError("astar_h3 not implemented")

def astar_h4(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h4 heuristic.
    """
    raise ValueError("astar_h4 not implemented")


def astar_h5(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h5 heuristic.
    """
    raise ValueError("astar_h5 not implemented")


def print_solution(solution: List[list],max_mis,max_can):
    """
    Prints the solution path. 
    """
    if not solution:
        print("No solution exists for the given parameters.")
        return
        
    print("\nSolution found! Number of steps:", len(solution) - 1)
    print("\nLeft Bank" + " "*20 + "Right Bank")
    print("-" * 50)
    
    for state in solution:
        if state[-1]:
            boat_display = "(B) " + " "*15
        else:
            boat_display = " "*15 + "(B) "
            
        print(f"M: {state[0]}, C: {state[1]}  {boat_display}" 
              f"M: {max_mis-state[0]}, C: {max_can-state[1]}")


def print_mon(ism: bool):
    """
    Prints if the heuristic function is monotone or not.
    """
    if ism:
        print("-" * 10)
        print("|Monotone|")
        print("-" * 10)
    else:
        print("-" * 14)
        print("|Not Monotone|")
        print("-" * 14)


def main():
    try:
        testcases = [{"m": 3, "c": 3}]

        for case in testcases:
            max_missionaries = case["m"]
            max_cannibals = case["c"]
            
            init_state = [max_missionaries, max_cannibals, 1] #initial state 
            final_state = [0, 0, 0] # final state
            
            if not check_valid(init_state, max_missionaries, max_cannibals):
                print(f"Invalid initial state for case: {case}")
                continue
                
            path_h1,ism1 = astar_h1(init_state, final_state, max_missionaries, max_cannibals)
            path_h2,ism2 = astar_h2(init_state, final_state, max_missionaries, max_cannibals)
            path_h3,ism3 = astar_h3(init_state, final_state, max_missionaries, max_cannibals)
            path_h4,ism4 = astar_h4(init_state, final_state, max_missionaries, max_cannibals)
            path_h5,ism5 = astar_h5(init_state, final_state, max_missionaries, max_cannibals)
            print_solution(path_h1,max_missionaries,max_cannibals)
            print_mon(ism1)
            print("-"*50)
            print_solution(path_h2,max_missionaries,max_cannibals)
            print_mon(ism2)
            print("-"*50)
            print_solution(path_h3,max_missionaries,max_cannibals)
            print_mon(ism3)
            print("-"*50)
            print_solution(path_h4,max_missionaries,max_cannibals)
            print_mon(ism4)
            print("-"*50)
            print_solution(path_h5,max_missionaries,max_cannibals)
            print_mon(ism5)
            print("="*50)

    except KeyError as e:
        print(f"Missing required key in test case: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
