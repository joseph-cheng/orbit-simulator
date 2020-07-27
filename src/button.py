import pygame
import utils
from vec import Vec

#Clickable button class with custom function on click
class Button:
    def __init__(self, name, pos, width, height, func, font, exists=True, toggled_name=""):
        #Text displayed within button
        self.name = name

        
        self.name_to_render = self.name
        #If the button name is too long, we want to truncate the text (the - 4 is to ensure the border of text does not make it too big)
        if font.size(self.name_to_render)[0] >= width - 4:

            # To truncate the text, I remove one letter at a time and check if the new name + a ... will fit within the button
            for it in range(1, len(self.name_to_render)):
                if font.size(self.name_to_render[0:-it] + "...")[0] < width:
                    self.name_to_render = self.name_to_render[0:-it] + "..."
                    break

        #This is the same as above but with the toggled text
        #If the toggled_name is an empty string, then it sets the toggled name to be the regular name
        self.toggled_name_to_render = toggled_name if toggled_name else self.name_to_render
        if font.size(self.toggled_name_to_render)[0] >= width - 4:
            for it in range(1, len(self.toggled_name_to_render)):
                if font.size(self.toggled_name_to_render[0:-it] + "...")[0] < width:
                    self.toggled_name_to_render = self.toggled_name_to_render[0:-it] + "..."
                    break
        
        self.displayed_name = self.name_to_render
                  
        #Top left of button
        self.pos = pos

        #Size of button
        self.width = width
        self.height = height

        #Function to be called on click
        self.func = func


        #Variable to check if clicked (will be rendered differently when clicked)
        self.clicked = False
        
        self.click_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

        #If a button is in a drop down menu, it will not 'exist' until the menu is opened, but almost all buttons will exist constantly
        #When a button does not exist, it will have no functionality
        self.exists = exists
        
    def on_button_click(self, mouse_pos):
        if not self.exists:
            return
        self.clicked = True
        


    #When the button is held down, move the button position and click rect based on where the mouse has moved
    def on_button_down(self, mouse_pos):
        
        pass
    
    def on_button_release(self, mouse_pos):
        if not self.exists:
            return
        self.clicked = False
        self.func()
        if self.displayed_name == self.name_to_render:
            self.displayed_name = self.toggled_name_to_render
        else:
            self.displayed_name = self.name_to_render

    def render(self, screen, font):

        if not self.exists:
            return
        
        #Draw a rect for the button with a larger width if clicked
        pygame.draw.rect(screen,
                         (150 if self.clicked else 255,
                         150 if self.clicked else 255,
                         150 if self.clicked else 255),
                         self.click_rect,
                         2 if self.clicked else 1)

        #Draw the text of the button


        
        name_surf = font.render(self.displayed_name, False, (255,255,255))

        name_border_surf = font.render(self.displayed_name, False, (0,0,0))

        utils.render_bordered(screen, name_surf, name_border_surf, Vec(self.pos.x+self.width/2 - name_surf.get_width()/2, self.pos.y + self.height/2 - name_surf.get_height()/2))
        
