import pygame

# --- constants ---

# contains the vector to each possible adjacent tile
DIRECTIONS = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (22, 175, 0)
BLUE = (50, 50, 255)

# --- classes ---
class Board:
    def __init__(self):
        self.tiles = [[Tile(x, y) for x in range(8)] for y in range(8)]

        # sets up the initial board state
        self.tiles[4][3].disk = "D"
        self.tiles[3][4].disk = "D"
        self.tiles[3][3].disk = "L"
        self.tiles[4][4].disk = "L"

        # stores the number of each disk colour
        self.disk_dict = {
            "D" : 2,
            "L" : 2
        }
        
    def valid_moves(self, active_colour):
        if active_colour == "D":
            inactive_colour = "L"
        elif active_colour == "L":
            inactive_colour = "D"

        # removes all valid moves before checking for new ones
        self.reset_valid_moves()
            
        moves = []
        
        for y in range(8):
            for x in range(8):
                if self.tiles[y][x].disk == " ":
                    # checks each possible tile surrounding the empty tile that was found
                    for direction in DIRECTIONS:
                        try:
                            if self.tiles[y + direction[1]][x + direction[0]].disk == inactive_colour:
                                if self.traverse([x, y], direction, active_colour, False):
                                    # if move is valid it gets added to the 'moves' array
                                    moves.append((x, y))
                                    self.tiles[y][x].valid_move = True
                                    break
                        except IndexError:
                            # this is reached if going in a certain direction would result in going off
                            # the edge of the board
                            continue
        return moves

    def place_disk(self, move, colour):
        # places disk on chosen tile and makes it no longer a valid move
        self.tiles[move[1]][move[0]].disk = colour
        self.tiles[move[1]][move[0]].valid_move = False
        
        for direction in DIRECTIONS:
            # checks each direction from move to flip tiles
            self.traverse(move, direction, colour, True)

    def traverse(self, current_tile, direction, player_colour, flipping, traversed=0):
        try:

            # advances to the next tile and stores its disk colour
            current_tile = [current_tile[0] + direction[0], current_tile[1] + direction[1]]
            traversed += 1
            disk = self.tiles[current_tile[1]][current_tile[0]].disk
            
            if disk == " ":
                # if there is no disk then no disks can be flipped in that direction
                return False
            elif (disk == player_colour) and (traversed > 1):
                # if a disk which is the same colour as the placed disk is found AND it is at
                # least two disks away from the starting point then it is a valid move
                
                if flipping:
                    # when using the function to flip disks, a separate subroutine is called
                    self.flip_disks(current_tile, direction, player_colour, traversed)
                    
                return True

            # if a disk of the opposite colour is found then the program will recursively loop
            return self.traverse(current_tile, direction, player_colour, flipping, traversed)
        
        except IndexError:
            # this is reached if the program traverses off the edge of the board
            return False

    def flip_disks(self, current_tile, direction, colour, traversed):
        if colour == "D":
            flipping = "L"
        elif colour == "L":
            flipping = "D"
        
        for i in range(traversed):
            # travels back through all the disks the 'traverse' function went through
            current_tile = [current_tile[0] - direction[0], current_tile[1] - direction[1]]

            # if a disk is opponent's colour, it is flipped to the other colour
            if self.tiles[current_tile[1]][current_tile[0]].disk == flipping:
                self.tiles[current_tile[1]][current_tile[0]].disk = colour

    def count_disks(self, colour):
        # counts the number of disks each player controls and returns the values in a dictionary
        count = 0
        for row in self.tiles:
            for tile in row:
                if tile.disk == colour:
                    count += 1
                    
        self.disk_dict[colour] = count
        return self.disk_dict[colour]

    def get_winner(self):
        # determines the winner by finding which disk colour appears the most
        if self.disk_dict["D"] == self.disk_dict["L"]:
            return None
        else:
            return max(self.disk_dict, key=self.disk_dict.get)

    def reset_valid_moves(self):
        # removes all valid moves from the board
        for row in self.tiles:
            for tile in row:
                tile.valid_move = False
        
    def draw(self, screen):
        # iterates through each tile and draws it onto the screen
        for row in self.tiles:
            for tile in row:
                tile.draw(screen)

class Tile:
    def __init__(self, x, y):
        self.pos_x = x * 50
        self.pos_y = y * 50
        self.disk = " "
        self.valid_move = False

        self.body = pygame.Rect(self.pos_x, self.pos_y, 45, 45)

    def check_clicked(self, mouse_pos, click):
        # checks if a mouse click was within the tile
        # if it was then it returns that it was clicked
        if (self.pos_x + 45 > mouse_pos[0] > self.pos_x):
            if (self.pos_y + 45 > mouse_pos[1] > self.pos_y):
                if self.valid_move == True:
                    return True

    def draw(self, screen):
        # draws the tile as a green square
        pygame.draw.rect(screen, GREEN, self.body)

        # if tile is a valid move, a blue border appears around it
        if self.valid_move == True:
            pygame.draw.rect(screen, BLUE, self.body, 3)

        # if tile contains a disk, a circle of the disk's colour is drawn on top of it
        if self.disk == "D":
            pygame.draw.circle(screen, BLACK, (self.pos_x + 22, self.pos_y + 22), 21)
        elif self.disk == "L":
            pygame.draw.circle(screen, WHITE, (self.pos_x + 22, self.pos_y + 22), 21)
