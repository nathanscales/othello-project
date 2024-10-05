import copy
from montecarlo import MCTS

# --- classes ---
class Player(object):
    def __init__(self, name):
        self.name = name
        self.colour = None
        
class AI(Player):
    def __init__(self, difficulty):
        Player.__init__(self, difficulty + " AI")
        
        self.difficulty = difficulty

        # determines how many monte carlo tree search iterations are performed
        # based on difficulty of AI
        if self.difficulty == "Easy":
            self.max_iterations = 10
        elif self.difficulty == "Normal":
            self.max_iterations = 100
        elif self.difficulty == "Hard":
            self.max_iterations = 200

    def get_move(self, state):
        # creates monte carlo tree search object
        game_tree = MCTS(self.max_iterations, self.colour)

        # uses a copy of the current board object to search for best move
        return game_tree.search(copy.deepcopy(state))
