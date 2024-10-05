import copy
import random
import time
from math import log, sqrt

# --- constants ---

# exploration constant for ucb formula when selecting nodes
C = sqrt(2)

# --- classes ---
class MCTS:
    def __init__(self, max_iterations, ai_colour):
        self.max_iterations = max_iterations
        self.ai_colour = ai_colour

    def search(self, state):
        # creates the root node as the current game state
        self.root = Node(state, self.ai_colour)

        # performs iterations of the monte carlo tree search until maximum is reached
        for i in range(self.max_iterations):

            # performs the three stages of the monte carlo tree search: selection, rollout and
            # backpropagation
            node = self.select(self.root)
            win = self.rollout(copy.deepcopy(node.state), node.colour)
            self.backpropagate(node, win)

        # after all iterations are complete, the best child of the root node is chosen
        best_child = self.root.get_best_child(0)
        for action, child in self.root.children.items():
            if child == best_child:
                return action

    def select(self, node):
        # if a node isn't terminal then its children are evaluated
        while not node.is_terminal:
            # the program expands one child node at a time until all have been expanded
            # then it chooses the best child
            if node.is_fully_expanded:
                node = node.get_best_child(C)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        # expands a single child node from the passed node
        return node.get_child()
    
    def rollout(self, state, colour):
        # finds all valid moves for current node's game state
        actions = state.valid_moves(colour)
        
        if len(actions) == 0:
            # this is the base case of the recursive function
            # when there are no possible moves left, the winner of the simulated game is determined
            return state.get_winner() == self.ai_colour
        else:
            # performs a random possible move
            state.place_disk(random.choice(actions), colour)

            # flips colour to simulate next player's turn
            if colour == "D":
                colour = "L"
            elif colour == "L":
                colour = "D"

            # rollout function will recursively loop until a terminal node is reached
            return self.rollout(state, colour)

    def backpropagate(self, node, win):
        # program goes back up through all nodes to the root node, updating the number of times they
        # were visited and the number of times a win is reached from that node
        while node is not None:
            node.n += 1
            node.w += int(win)
            node = node.parent

class Node:
    def __init__(self, state, colour, parent=None):
        self.colour = colour # the colour of the next disk to be placed
        self.state = state # the current game state
        self.actions = self.state.valid_moves(self.colour)

        if len(self.actions) == 0:
            self.is_terminal = True
        else:
            self.is_terminal = False
            
        self.is_fully_expanded = self.is_terminal
        
        self.parent = parent # stores the reference of the parent node
        self.n = 0 # number of times node has been visited
        self.w = 0 # number of wins possible from node

        # dictionary of child nodes, the action leading to the child node is the key
        # and the child node object is the value
        self.children = {}
        
    def get_child(self):
        if self.colour == "D":
            child_colour = "L"
        elif self.colour == "L":
            child_colour = "D"

        # checks each possible valid move from this node and creates a node for one that
        # hasn't already been expanded
        for action in self.actions:
            if action not in self.children.keys():
                
                # creates a copy of the board object
                child_state = copy.deepcopy(self.state)
                
                child_state.place_disk(action, self.colour)
                self.children[action] = Node(child_state, child_colour, self)
                if len(self.actions) == len(self.children):
                    self.is_fully_expanded = True
                return self.children[action]

    def get_best_child(self, exploration_constant):
        # finds and returns the child node with the greatest UCB value
        best_child = None

        for child in self.children.values():
            child.get_score(exploration_constant)
            
            if (best_child == None) or (child.score > best_child.score):
                best_child = child
            elif child.score == best_child.score:
                best_child = random.choice([child, best_child])
                
        return best_child

    def get_score(self, exploration_constant):
        # uses the Upper Confidence Bound formula to determine a node's score
        try:
            win_ratio = self.w / self.n
            ucb = win_ratio + (exploration_constant * sqrt(log(self.parent.n) / self.n))
            self.score = ucb
        except ZeroDivisionError:
            # if value from UCB formula is infinity, then an error must be caught and
            # the score is returned as a float
            self.score = float("inf")
