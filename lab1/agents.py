# -*- coding: utf-8; mode: python -*-

# ENSICAEN
# École Nationale Supérieure d'Ingénieurs de Caen
# 6 Boulevard Maréchal Juin
# F-14050 Caen Cedex France
#
# Artificial Intelligence 2I1AE1

# @file agents.py
#
# @author Régis Clouard

import copy
import utils

class Agent:
    """
    Abstract class for the agents that implement the various search strategies.
    It is based on the Strategy Design Pattern (abstract method is search()).

    YOU DO NOT NEED TO CHANGE ANYTHING IN THIS CLASS, EVER.
    """
    def search( self ):
        """ This is the method to implement for each specific searcher."""
        raise Exception("Invalid Agent class, search() not implemented")

 #  ______                               _                  __ 
 # |  ____|                             (_)                /_ |
 # | |__    __  __   ___   _ __    ___   _   ___    ___     | |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \    | |
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    | |
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|    |_|

class DFS( Agent ):

    def search( self, initial_state ):
        """ Depth-First Search.
    
        Returns the path as a list of directions among
        { Direction.left, Direction.right, Direction.up, Direction.down }

        """
        open_list = [[ (initial_state, None) ]] # A state is a pair (board, direction)
        closed_list = set([initial_state]) # keep already explored positions

        while open_list:
            # Get the path at the top of the stack (pop(0) returns the first item of the list)
            current_path = open_list.pop(0)
            # Get the last place of that path
            current_state, current_direction = current_path[-1]
            # Check if we have reached the goal
            if current_state.is_goal_state():
                # remove the start point and return only the directions.
                return (list (map(lambda x : x[1], current_path[1:])))
            else:
                # Check where we can go from here
                next_steps = current_state.get_successor_states()
                # Add the new paths (one step longer) to the stack
                for state, direction, weight in next_steps:
                    # do not add already explored states
                    if state not in closed_list:
                        # add at the end of the list
                        closed_list.add(state)
                        open_list.insert(0, (current_path + [ (state, direction) ]) )
        return []

class BFS( Agent ):
    
    def search( self, initial_state ):
        """ Breadth-First Search
        
        Returns the path as a list of directions among
        { Direction.left, Direction.right, Direction.up, Direction.down }
        
        Useful methods:
        - state.is_goal_state(): Returns true if the state is a valid goal state.
        - state.get_successor_states(): Returns all states reachable from the state as a list of triplets (state, direction, cost).
        """

        open_list = [[ (initial_state, None) ]]
        closed_list = set([initial_state])

        while open_list:
            # Get the path at the top of the Queue (pop(0) returns the first item of the list)
            current_path = open_list.pop(0)
            # Get the last place of that path
            current_state, current_direction = current_path[-1]
            # Check if we have reached the goal
            if current_state.is_goal_state():
                # remove the start point and return only the directions.
                return (list (map(lambda x : x[1], current_path[1:])))
            else:
                # Check where we can go from here
                next_steps = current_state.get_successor_states()
                # Add the new paths (one step longer) to the stack
                for state, direction, weight in next_steps:
                    # do not add already explored states
                    if state not in closed_list:
                        # add at the end of the list
                        closed_list.add(state)
                        open_list.append((current_path + [ (state, direction) ]) )
        return []


 #  ______                               _                  ___  
 # |  ____|                             (_)                |__ \ 
 # | |__    __  __   ___   _ __    ___   _   ___    ___       ) |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \     / / 
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    / /_ 
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|   |____|

class UCS( Agent ):
    def search( self, initial_state ):
        """ Uniform-Cost Search.

        It returns the path as a list of directions among
        { Direction.left, Direction.right, Direction.up, Direction.down }
        """

        # use a priority queue with the minimum queue.
        from utils import PriorityQueue
        open_list = PriorityQueue()
        open_list.push([(initial_state, None)], 0) # a state is a pair (boad, direction)
        closed_list = set([initial_state]) # keep already explored positions

        while not open_list.isEmpty():
            # Get the path at the top of the queue
            current_path, cost = open_list.pop()
            # Get the last place of that path
            current_state, current_direction = current_path[-1]
            # Check if we have reached the goal
            if current_state.is_goal_state():
                return (list (map(lambda x : x[1], current_path[1:])))
            else:
                # Check were we can go from here
                next_steps = current_state.get_successor_states()
                # Add the new paths (one step longer) to the queue
                for state, direction, weight in next_steps:
                    # Avoid loop!
                    if state not in closed_list:
                        closed_list.add(state)
                        open_list.push((current_path + [ (state, direction) ]), cost + weight)
        return []

class GBFS( Agent ):

    def search( self, initial_state ):
        """ Greedy Best First Search.

        Returns the path as a list of directions among
        { Direction.left, Direction.right, Direction.up, Direction.down }
        
        Useful methods:
        - state.is_goal_state(): Returns true if the state is a valid goal state.
        - state.get_successor_states(): Returns all states reachable from the specified state as a list of triplets (state, direction, cost)
        - state.heuristic(): Returns the heuristic value for the specified state.
        """

        from utils import PriorityQueue
        open_list = PriorityQueue()
        open_list.push([(initial_state, None)], 0) # a state is a pair (boad, direction)
        closed_list = set([initial_state]) # keep already explored positions

        while not open_list.isEmpty():
            # Get the path at the top of the queue
            current_path, cost = open_list.pop()
            # Get the last place of that path
            current_state, current_direction = current_path[-1]
            # Check if we have reached the goal
            if current_state.is_goal_state():
                return (list (map(lambda x : x[1], current_path[1:])))
            else:
                # Check were we can go from here

                next_steps = current_state.get_successor_states()
                # Add the new paths (one step longer) to the queue
                for state, direction, weight in next_steps:
                    # Avoid loop!
                    
                    if state not in closed_list:
                        
                        closed_list.add(state)
                        open_list.push((current_path + [ (state, direction) ]), state.heuristic())
        return []

 #  ______                               _                  ____  
 # |  ____|                             (_)                |___ \ 
 # | |__    __  __   ___   _ __    ___   _   ___    ___      __) |
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \    |__ < 
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    ___) |
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|   |____/ 

class ASS( Agent ):
    def search( self, initial_state ):
        """ A Star Search.

        It returns the path as a list of directions among
        { Direction.left, Direction.right, Direction.up, Direction.down }

        Useful methods:
        - state.is_goal_state(): Returns true if the state is a valid goal state.
        - state.get_successor_states(): Returns all states reachable from the specified state as a list of triplets (state, direction, cost)
        - state.heuristic(): Returns the heuristic value for the specified state.

        """
        from utils import PriorityQueue
        open_list = PriorityQueue()
        open_list.push([(initial_state, None)], 0) # a state is a pair (boad, direction)
        closed_list = set([initial_state]) # keep already explored positions

        while not open_list.isEmpty():
            # Get the path at the top of the queue
            current_path, priority = open_list.pop()
            # Get the last place of that path
            current_state, current_direction = current_path[-1]
            # Check if we have reached the goal
            cost = priority - current_state.heuristic()
            if current_state.is_goal_state():
                return (list (map(lambda x : x[1], current_path[1:])))
            else:
                # Check were we can go from here

                next_steps = current_state.get_successor_states()
                # Add the new paths (one step longer) to the queue
                for state, direction, weight in next_steps:
                    # Avoid loop!
                    
                    if state not in closed_list:
                        
                        closed_list.add(state)
                        open_list.push((current_path + [ (state, direction) ]), state.heuristic() + cost + weight )
        return []
        
 #  ______                               _                  _  _   
 # |  ____|                             (_)                | || |  
 # | |__    __  __   ___   _ __    ___   _   ___    ___    | || |_ 
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \   |__   _|
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/      | |  
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|      |_|  

class IDS( Agent ):
    MAX_PATH_LENGTH = 500 # Found in literature
    def search( self, initial_state ):
       
        
       
       for limit in range(self.MAX_PATH_LENGTH):
            open_list = [[ (initial_state, None) ]] # A state is a pair (board, direction)
            closed_list = set([initial_state]) 
            
            # keep already explored positions

            
            while open_list:
                current_path = open_list.pop(0)
                current_state, current_direction = current_path[-1]
                depth = len(current_path) - 1
                if current_state.is_goal_state():
                    # remove the start point and return only the directions.
                    return (list (map(lambda x : x[1], current_path[1:])))
                
                
                if depth < limit :
                        # Check where we can go from here
                    next_steps = current_state.get_successor_states()
                        # Add the new paths (one step longer) to the stack
                    for state, direction, weight in next_steps:
                            # do not add already explored states
                        if state not in closed_list:
                                # add at the end of the list
                            closed_list.add(state)
                            open_list.insert(0, (current_path + [ (state, direction) ]) )
       return []
    
        

 #  ______                               _                  _____ 
 # |  ____|                             (_)                | ____|
 # | |__    __  __   ___   _ __    ___   _   ___    ___    | |__  
 # |  __|   \ \/ /  / _ \ | '__|  / __| | | / __|  / _ \   |___ \ 
 # | |____   >  <  |  __/ | |    | (__  | | \__ \ |  __/    ___) |
 # |______| /_/\_\  \___| |_|     \___| |_| |___/  \___|   |____/ 
"""🔑 Explanation (step by step)

Initialize bound:

bound = h(initial_state)

This is the first limit on f-cost for expansion.

Iterative deepening loop:

At each iteration, we do a DFS like your original code, but we skip nodes with f > bound.

Stack (open_list):

Same style as DFS: a list of paths [ (state, direction) ].

Each element also keeps g (cost so far).

Compute f:

f = g + current_state.heuristic()

If f > bound, we don’t expand, but track min_exceed (the smallest f that exceeded the bound).

Expand successors:

Like DFS, but only if the successor is not already in the current path.

Insert at the front (insert(0, …)) to mimic DFS order.

Update bound:

After finishing the stack, set bound = min_exceed for the next iteration.

Stop condition:

Goal found → return directions

No nodes exceeded bound → return []
"""
class IDASS(Agent):
    MAX_PATH_LENGTH = 500

    def search(self, initial_state):
        bound = initial_state.heuristic()
        path = [(initial_state, None)]

        while True:
            t = self._search(path, 0, bound)
            if t == "FOUND":
                return [d for _, d in path[1:]]
            if t == float("inf"):
                return []  # no solution
            bound = t

    def _search(self, path, g, bound):
        current_state, _ = path[-1]
        f = g + current_state.heuristic()

        if f > bound:
            return f
        if current_state.is_goal_state():
            return "FOUND"

        min_exceed = float("inf")
        path_states = set(s for s, _ in path)

        for state, direction, cost in current_state.get_successor_states():
            if state not in path_states:
                path.append((state, direction))
                t = self._search(path, g + cost, bound)
                if t == "FOUND":
                    return "FOUND"
                if t < min_exceed:
                    min_exceed = t
                path.pop()

        return min_exceed

