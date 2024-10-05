import pygame
from math import floor

# --- constants ---

WHITE = (255, 255, 255)

# --- classes ---

# superclass for all interface elements
class Element(object):
    # the registry is used to iterate through all interface elements
    _registry = []
    
    def __init__(self, element_type, x, y):
        self._registry.append(self)
        
        self.x = x
        self.y = y
        self.element_type = element_type
        
        self.visible = False

    def show(self, screen):
        # displays an interface element
        self.visible = True
        self.draw(screen)

class Text(Element):
    def __init__(self, x, y, text, size):
        Element.__init__(self, "text", x, y)
        
        self.text = text
        self.size = size

    def draw(self, screen):
        # declares font type, size and colour
        font = pygame.font.Font("freesansbold.ttf", self.size)
        text_surface = font.render(self.text, True, WHITE)

        text_surf, text_rect = text_surface, text_surface.get_rect()
        text_rect.center = (self.x, self.y)

        # draws text onto the screen
        screen.blit(text_surf, text_rect)

class Button(Element):
    def __init__(self, x, y, width, height, colour, text, action, **kwargs):
        Element.__init__(self, "button", x, y)
        
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.action = action

        self.border = None
        self.arg = None
        for key, value in kwargs.items():
            if key == "border":
                self.border = value
            elif key == "arg":
                self.arg = value

        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_clicked(self, mouse_pos, click):
        # if the button is visible and the mouse position is somewhere inside the button then the button's
        # action is performed
        if self.visible == True:
            if (self.x + self.width > mouse_pos[0] > self.x) and (self.y + self.height > mouse_pos[1] > self.y):
                if self.arg != None:
                    self.action(self.arg)
                else:
                    self.action()

    def draw(self, screen):
        # button can either be drawn as a solid rectangle or a border with no fill
        if self.border == None:
            pygame.draw.rect(screen, self.colour, self.body)
        else:
            pygame.draw.rect(screen, self.colour, self.body, self.border)

        # if the button has text on it, the position and size of it is determined based on the size of
        # the button
        if self.text != "":
            text_x = self.x + (self.width / 2)
            text_y = self.y + (self.height / 2)
            text_size = floor(self.height / 2)
            Text(text_x, text_y, self.text, text_size).show(screen)
