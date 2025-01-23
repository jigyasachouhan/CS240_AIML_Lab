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
    
    # def __eq__(self, other):
    #     return equal(self.state, other.state)

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
    if (m_left==0 or m_left >= c_left) and ((max_missionaries-m_left)==0 or (max_missionaries-m_left) >= (max_cannibals-c_left)) and (boat_pos ==0 or boat_pos==1):
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
    
    if boat_pos==1:
        if m_left >=1:
            curr = [m_left-1, c_left, 0]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_left >=1:
            curr = [m_left, c_left-1, 0]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
        
        if m_left >=2:
            curr = [m_left-2, c_left, 0]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_left >=2:
            curr = [m_left, c_left-2, 0]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_left >=1 and m_left>=1:
            curr = [m_left-1, c_left-1, 0]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)    
                
    else:
        m_right = max_missionaries - m_left
        c_right = max_cannibals - c_left
        if m_right >=1:
            curr = [m_left+1, c_left, 1]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_right >=1:
            curr = [m_left, c_left+1, 1]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
        
        if m_right >=2:
            curr = [m_left+2, c_left, 1]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_right >=2:
            curr = [m_left, c_left+2, 1]
            if(check_valid(curr, max_missionaries, max_cannibals)): 
                nbrs.append(curr)
                
        if c_right >=1 and m_right>=1:
            curr = [m_left+1, c_left+1, 1]
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

def astar_h(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int, h_func
) -> Tuple[List[list], bool]:  # 28 marks
    """
    Graded
    Implement A* with h1 heuristic.
    This function must return path obtained and a boolean which says if the heuristic chosen satisfes Monotone restriction property while exploring or not.
    """
    
    # raise ValueError("astar_h1 not implemented")
    
    init_st = State(init_state, None, h_func(init_state) + 0, 0)
    monotone = True
    open = []
    closed = set()
    closed_st = set()
    heapq.heappush(open, init_st)
    
    while open:
        # print("open has ", len(open))
        top = heapq.heappop(open)
        
        if tuple(top.state) not in closed:
            closed.add(tuple(top.state))
            closed_st.add(top)
        
        else:
            continue
        
        nbrs = get_neighbours(top.state, max_missionaries, max_cannibals)
        
        for nbr in nbrs:
            nbrt = tuple(nbr)
            if nbrt not in closed:
                new_st = State(nbr, top, h_func(nbr) + gstar(top.state, nbr) + top.steps, gstar(top.state, nbr)+top.steps)
                heapq.heappush(open, new_st)
            else:
                # print("ELSE\n")
                for x in closed_st:
                    if equal(x.state, nbr):
                        nbr_st = x
                        break
                    
                if nbr_st.steps > gstar(top.state, nbr) + top.steps:
                    monotone = False
                    nbr_st.parent = top
                    nbr_st.cost = h_func(nbr) + gstar(top.state, nbr) + top.steps
                    nbr_st.steps = gstar(top.state, nbr) + top.steps
                    

    # print("out")
    if tuple(final_state) not in closed:
        return ([], monotone)
    
    seq = []
    
    for x in closed_st:
        if equal(x.state, final_state):
            curr = x
            break
        
    while not equal(curr.state, init_state):
    # for i in range(10):
        seq.append(curr.state)
        curr = curr.parent
        
    seq.append(curr.state)
    seq = seq[::-1]
    
    # print(seq)
    return (seq, monotone)



def astar_h1(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 28 marks
    """
    Graded
    Implement A* with h1 heuristic.
    This function must return path obtained and a boolean which says if the heuristic chosen satisfes Monotone restriction property while exploring or not.
    """
    
    # raise ValueError("astar_h1 not implemented")
    
    return astar_h(init_state, final_state, max_missionaries, max_cannibals, h1)    
       
def astar_h2(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h2 heuristic.
    """
    return astar_h(init_state, final_state, max_missionaries, max_cannibals, h2)

def astar_h3(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h3 heuristic.
    """
    return astar_h(init_state, final_state, max_missionaries, max_cannibals, h3)

def astar_h4(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h4 heuristic.
    """
    ans, bleh = astar_h(init_state, final_state, max_missionaries, max_cannibals, h4)
    return (ans, False)

def astar_h5(
    init_state: list, final_state: list, max_missionaries: int, max_cannibals: int
) -> Tuple[List[list], bool]:  # 8 marks
    """
    Graded
    Implement A* with h5 heuristic.
    """
    ans, bleh = astar_h(init_state, final_state, max_missionaries, max_cannibals, h5)
    return (ans, False)


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
