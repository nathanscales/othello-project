import easygui
import pickle
import pygame
import random
import sys
import threading
from elements import Element, Text, Button
from board import Board
from player import Player, AI

# --- constants ---

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 395
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 35, 0)
GREEN = (22, 175, 0)
GREY = (135, 135, 135)

# creating custom event for when it is an AI player's turn
GETAIMOVE = pygame.USEREVENT + 1
AI_TURN = pygame.event.Event(GETAIMOVE)

# creating custom event for when program needs to place a disk
PLACEDISK = pygame.USEREVENT + 2
MOVE_CHOSEN = pygame.event.Event(PLACEDISK)

# --- classes ---

# - state classes -

# superclass for both 'game' and 'menu' states
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

    def check_buttons(self, mouse_pos, click):
        # checks each button object to find the one that was clicked
        for element in Element._registry:
            if element.element_type == "button":
                element.check_clicked(mouse_pos, click)

    def hide_elements(self, screen):
        # clears the screen of all element objects
        for element in Element._registry:
            element.visible = False
        screen.fill(BLACK)

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = "game"

        # declaring button and text objects used in the 'game' state
        self.btn_loadgame = Button(225, 280, 150, 40, GREEN, "Load Game", self.load_game)
        self.btn_startgame = Button(225, 230, 150, 40, GREEN, "New Game", self.new_game)
        
        self.btn_playertypes = [[Button(15, 150, 100, 40, GREEN, "Human", self.change_type, arg="Human"),
                                 Button(120, 150, 100, 40, GREY, "AI", self.change_type, arg="Easy")],
                                [Button(380, 150, 100, 40, GREEN, "Human", self.change_type, arg="Human"),
                                 Button(485, 150, 100, 40, GREY, "AI", self.change_type, arg="Easy")]]

        self.btn_name = [Button(16, 220, 200, 40, WHITE, "", self.player_name, border=2),
                         Button(383, 220, 200, 40, WHITE, "", self.player_name, border=2)]

        self.btn_aidifficulties = [[Button(30, 200, 150, 40, GREEN, "Easy", self.change_type, arg="Easy"),
                                    Button(30, 250, 150, 40, GREY, "Normal", self.change_type, arg="Normal"),
                                    Button(30, 300, 150, 40, GREY, "Hard", self.change_type, arg="Hard")],
                                   [Button(415, 200, 150, 40, GREEN, "Easy", self.change_type, arg="Easy"),
                                    Button(415, 250, 150, 40, GREY, "Normal", self.change_type, arg="Normal"),
                                    Button(415, 300, 150, 40, GREY, "Hard", self.change_type, arg="Hard")]]

        self.txt_title = Text(300, 50, "Othello", 80)
        self.txt_p1 = Text(120, 140, "Player 1", 20)
        self.txt_p2 = Text(480, 140, "Player 2", 20)
        
        self.txt_name = [Text(120, 210, "Name:", 20),
                         Text(480, 210, "Name:", 20)]

        # dictionary containing settings for each player
        # both players are human by default
        self.player_dict = {
            1 : "Human",
            2 : "Human"
        }
       
    def cleanup(self):
        print("Menu Ended")
        
    def startup(self):
        print("Menu Started\n")

    def get_event(self, event):
        # this is an event unique to the 'menu' state
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            self.check_buttons(mouse_pos, click)

    def new_game(self):
        game = app.state_dict["game"]

        # creates an array within the 'game' object containing each
        # player's type
        game.players = []
        for p in range(2):
            player_type = self.player_dict.get(p+1)
            if player_type == "Human":
                game.players.append(Player(self.btn_name[p].text))
            else:
                game.players.append(AI(player_type))

        # randomly chooses who the first player will be and sets their
        # disk colour to dark disks
        game.active_player = random.choice([0, 1])
        game.players[game.active_player].colour = "D"

        # the player going second uses the light disks
        game.players[int(not bool(game.active_player))].colour = "L"

        # creates the board object
        game.b = Board()

        # sets number of possible moves to 4
        game.moves_remaining = 4

        # flips to the 'game' state
        app.flip_state()

    def load_game(self):
        game = app.state_dict["game"]
        
        while True:
            try:
                # the user is prompted to browse their local files for a valid save file
                directory = easygui.fileopenbox("Select Save File",
                            filetypes=["*.othello", "Othello Save File"])

                # file is opened and the pickle library loads the data within the file
                # to the corresponding objects
                file = open(directory, "rb")
                game.active_player = pickle.load(file)
                game.players.append(pickle.load(file))
                game.players.append(pickle.load(file))
                game.b = pickle.load(file)
            except pickle.UnpicklingError:
                # if the file is invalid then the user is told so and they are prompted to
                # search for another
                easygui.msgbox("Invalid File!")
                continue
            except TypeError:
                # this error occurs if the user closes the fileopenbox without choosing a file,
                # it will go back to the main menu without flipping the state
                return
            else:
                # if no errors occur then the while loop ends
                break

        # state flips to 'game' state
        app.flip_state()

    def change_type(self, player_type):
        # changes the player type from Human to AI or vice versa
        # uses mouse position to determine which player is being changed
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < 300:
            self.player_dict[1] = player_type
        else:
            self.player_dict[2] = player_type

    def player_name(self):
        # allows the user to change the name of a human player
        mouse_pos = pygame.mouse.get_pos()
        while True:
            try:
                # the player is prompted to enter a name
                name = easygui.enterbox("Enter Name (Max 15 Characters)")
                if len(name) > 15:
                    # if the name is greater than 15 characters an exception will be raised
                    raise
            except:
                easygui.msgbox("Name is greater than 15 characters")
                return
            else:
                break

        # uses the mouse position to determine the player being changed
        if mouse_pos[0] < 300:
            self.btn_name[0].text = name
        else:
            self.btn_name[1].text = name
           
    def update(self, screen):
        # updates screen after every event

        # hides all objects on screen
        self.hide_elements(screen)
        
        self.txt_title.show(screen)
        self.txt_p1.show(screen)
        self.txt_p2.show(screen)

        # displays buttons and text relating to each player
        for p in range(2):
            self.btn_playertypes[p][0].colour = GREY
            self.btn_playertypes[p][1].colour = GREY
            self.btn_aidifficulties[p][0].colour = GREY
            self.btn_aidifficulties[p][1].colour = GREY
            self.btn_aidifficulties[p][2].colour = GREY

            player_type = self.player_dict.get(p+1)
            if player_type == "Human":
                # if player is a Human, the Human button's colour is changed to green
                self.btn_playertypes[p][0].colour = GREEN

                # the box allowing the user to change the Human player's name is displayed
                self.txt_name[p].show(screen)
                self.btn_name[p].show(screen)
            else:
                # if player is an AI, the AI button's colour is changed to green
                self.btn_playertypes[p][1].colour = GREEN

                # button corresponding to AI's difficulty is also changed to green
                if player_type == "Easy":
                    self.btn_aidifficulties[p][0].colour = GREEN
                elif player_type == "Normal":
                    self.btn_aidifficulties[p][1].colour = GREEN
                elif player_type == "Hard":
                    self.btn_aidifficulties[p][2].colour = GREEN

                # AI difficulty buttons are all shown
                self.btn_aidifficulties[p][0].show(screen)
                self.btn_aidifficulties[p][1].show(screen)
                self.btn_aidifficulties[p][2].show(screen)

            # buttons to change a player's type are shown
            self.btn_playertypes[p][0].show(screen)
            self.btn_playertypes[p][1].show(screen)

        # displays the load game, start game and quit buttons
        self.btn_loadgame.show(screen)
        self.btn_startgame.show(screen)
        app.btn_quit.show(screen)

# class containing functions, objects and variables used by the 'game' state
class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = "menu"

        # declaring button and text objects used in the 'game' state
        self.btn_save = Button(415, 295, 170, 40, GREEN, "Save Game", self.save)
        self.btn_concede = Button(415, 340, 170, 40, RED, "Concede Game", self.concede)
        
        self.txt_darkdisks = Text(460, 20, "Dark Disks:", 20)
        self.txt_darkdiskcount = Text(500, 50, "2", 30)
        self.txt_lightdisks = Text(460, 90, "Light Disks:", 20)
        self.txt_lightdiskcount = Text(500, 120, "2", 30)
        self.txt_player = Text(495, 160, "", 30)
        self.txt_turn = Text(495, 200, "Turn", 30)
        self.txt_playernum = Text(495, 230, "", 20)
        self.txt_message = Text(495, 270, "Place a Dark Disk", 20)

        self.players = []
        self.conceded = False
        self.move = None
        
    def cleanup(self):
        print("Game Ended")

    def startup(self):
        # finds the initial valid moves
        self.actions = self.b.valid_moves(self.players[self.active_player].colour)
        self.conceded = False
        
        if isinstance(self.players[self.active_player], AI):
            pygame.event.post(AI_TURN)

    def get_event(self, event):
        # these are events unique to the 'game' state

        # this happens whenever the 'AI_TURN' event is posted
        if event.type == GETAIMOVE:
            # the AI uses a thread to find their move so that the user can still interact with buttons
            # while AI is finding best move
            threading.Thread(target=self.get_ai_move).start()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # if mouse click is anywhere from (0, 0) to (400, 400), then each board tile is checked
            # otherwise, mouse click was outside the board so all active buttons are checked
            if (0 <= mouse_pos[0] <= 400) and (0 <= mouse_pos[1] <= 400):

                # only continues if active player is a Human
                if not isinstance(self.players[self.active_player], AI):

                    # checks each available move to find the one the user clicked
                    for action in self.actions:
                        if self.b.tiles[action[1]][action[0]].check_clicked(mouse_pos, click):
                            self.move = action
                            pygame.event.post(MOVE_CHOSEN)
                            break
            else:
                self.check_buttons(mouse_pos, click)

        # this happens whenever the 'MOVE_CHOSEN' event is posted
        elif event.type == PLACEDISK:
            # places a disk in the position the active player chose
            self.b.place_disk(self.move, self.players[self.active_player].colour)

            # changes the active player and finds their valid moves
            self.active_player = int(not bool(self.active_player))
            self.actions = self.b.valid_moves(self.players[self.active_player].colour)

            # if the new active player is an AI and the game isn't over then the 'AI_TURN' event is posted
            if isinstance(self.players[self.active_player], AI):
                if self.actions and not self.conceded:
                    pygame.event.post(AI_TURN)

    def get_ai_move(self):
        # passes board object to player object so AI can determine its best move
        self.move = self.players[self.active_player].get_move(self.b)
        pygame.event.post(MOVE_CHOSEN)

    def save(self):
        try:
            # prompts user to choose a directory to save their file
            directory = easygui.filesavebox("Save Game", filetypes=["*.othello", "Othello Save File"])
            file = open(directory, "wb")

            # pickle library dumps all data needed to reload the current game state into the save file
            pickle.dump(self.active_player, file)
            pickle.dump(self.players[0], file)
            pickle.dump(self.players[1], file)
            pickle.dump(self.b, file)
        except:
            # if the user closes the filesavebox then nothing happens and the game continues as normal
            pass
        else:
            # after saving, the program returns to the 'menu' state
            app.flip_state()
        
    def concede(self):
        self.conceded = True

    def update(self, screen):
        # this performs the same purpose as the update subroutine in the 'menu' state
        
        self.hide_elements(screen)

        # displays each player's disk count
        self.txt_darkdiskcount.text = str(self.b.count_disks("D"))
        self.txt_lightdiskcount.text = str(self.b.count_disks("L"))

        if self.actions and not self.conceded:

            
            # displays who the active player is
            self.txt_player.text = "{0}'s".format(self.players[self.active_player].name)
            self.txt_turn.text = "Turn"
            self.txt_playernum.text = "(Player {0})".format(self.active_player + 1)

            # instructs the user what to do based on their disk colour
            if self.players[self.active_player].colour == "D":
                self.txt_message.text = "Place a Dark Disk"
            elif self.players[self.active_player].colour == "L":
                self.txt_message.text = "Place a Light Disk"

            # displays the save game and concede buttons
            self.btn_save.show(screen)
            self.btn_concede.show(screen)

        else:

            # if the game is over, this displays the winner

            self.b.reset_valid_moves()
            self.txt_turn.text = "Wins"
            self.txt_message.text = ""
            self.txt_playernum.text = ""
            
            if self.conceded:
                # if a player conceded, the opponent is the winner
                self.txt_player.text = self.players[int(not bool(self.active_player))].name
            else:
                # if no valid moves remain, the player with the most disks wins
                winning_colour = self.b.get_winner()
                if self.players[0].colour == winning_colour:
                    self.txt_player.text = self.players[0].name
                elif self.players[1].colour == winning_colour:
                    self.txt_player.text = self.players[1].name
                else:
                    self.txt_player.text = "Draw"
                    self.txt_turn.text = ""

            # displays the return to menu button
            app.btn_return.show(screen)

        # displays all remaining text objects
        self.txt_darkdisks.show(screen)
        self.txt_darkdiskcount.show(screen)
        self.txt_lightdisks.show(screen)
        self.txt_lightdiskcount.show(screen)
        self.txt_player.show(screen)
        self.txt_turn.show(screen)
        self.txt_playernum.show(screen)
        self.txt_message.show(screen)
                
        self.b.draw(screen)

# - application class -
class Application:
    def __init__(self, state_dict, **settings):
        self.__dict__.update(settings)
        self.done = False

        self.btn_quit = Button(225, 330, 150, 40, RED, "Quit", self.quit)
        self.btn_return = Button(415, 340, 170, 40, GREEN, "Return to Menu", self.flip_state)

        # create game window and set caption
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Othello")

        # declare clock variable
        self.clock = pygame.time.Clock()

        pygame.init()

        # setting up states
        self.state_dict = state_dict
        self.state_name = "menu"
        self.state = self.state_dict[self.state_name]

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        
        # performs cleanup procedure for the state that is about to be exited
        self.state.cleanup()
        
        # sets stored class as the one that corresponds to new state
        self.state = self.state_dict[self.state_name]
        
        # performs startup procedure for new state
        self.state.startup()
        
        self.state.previous = previous

    def update(self):
        # checks if state needs to be changed then updates active state
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen)

    def event_loop(self):
        # gets all inputs that have occured since last frame
        # all inputs are within the class of the active state except quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self.state.get_event(event)

    def main_loop(self):
        # this will be looped repeatedly until user quits
        while not self.done:
            self.event_loop()
            self.update()

            # update game screen
            pygame.display.update()

            #
            self.clock.tick(self.fps)

    def quit(self):
        self.done = True

# --- main ---
if __name__ == "__main__":
    
    settings = {
        "size" : SCREEN_SIZE,
        "fps"  : FPS
    }

    # dictionary containing names of possible states and their corresponding class                  
    state_dict = {
        "menu" : Menu(),
        "game" : Game()
    }

    # declares application object and starts game
    app = Application(state_dict, **settings)
    app.main_loop()

    # exits the program
    pygame.quit()
    sys.exit()
