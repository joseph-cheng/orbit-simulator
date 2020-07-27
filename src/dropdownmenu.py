import button
import pygame
from vec import Vec
import utils

# Drop down menu mouse object
class DropDownMenu:
    def __init__(self, name, pos, width, height):
        self.name = name
        self.buttons = []
        self.pos = pos
        self.width = width
        self.height = height

        self.clicked = False

        self.expanded = False

        self.click_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    
    def on_button_click(self, mouse_pos):
        self.clicked = True

    def on_button_down(self, mouse_pos):
        pass

    #When the menu is released, set all of the buttons to change from existing to not existing or vice versa, and set expanded to not expanded
    #This means that clicking the menu will either collapse or expand the menu depending on the current state
    def on_button_release(self, mouse_pos):
        self.clicked = False
        for button in self.buttons:
            button.exists = not button.exists
        self.expanded = not self.expanded

    #Takes in the name and function of a button and the stack of mouse objects and creates a but0ton with the correct position and attributes as well as adding it to the mouse objects stack
    def add_button(self, name, func, font, mouse_objects_stack, toggled_name=""):
        button_pos = (self.buttons[-1].pos + Vec(0, self.height)) if len(self.buttons) else (self.pos + Vec(0, self.height))
        b = button.Button(name, button_pos, self.width, self.height, func, font, exists=self.expanded, toggled_name=toggled_name)
        self.buttons.append(b)
        mouse_objects_stack.append(b)

    def remove_button(self, button_name, mouse_objects_stack):

        button_pos = -1

        #Find the correct button and remove it from the button list and mouse objects stack
        for it, button in enumerate(self.buttons):
            if button.name == button_name:
                button_pos = it
                del self.buttons[it]

                #Find the corresponding button in the mouse object stack
                for mouse_object in mouse_objects_stack:
                    if mouse_object == button:
                        mouse_objects_stack.remove(button)
                break
            
        #If the button does not exist, return
        if button_pos == -1:
            return
        
        #Move all the buttons below the deleted button upwards
        for button_it in range(button_pos, len(self.buttons)):
            b = self.buttons[button_it]
            b.pos.y -= self.height
            b.click_rect.y -= self.height
        
    def render(self, screen, font):
        #Render the rect around the text
        pygame.draw.rect(screen,
                         (150 if self.clicked else 255,
                         150 if self.clicked else 255,
                         150 if self.clicked else 255),
                         self.click_rect,
                         2 if self.clicked else 1)

        #Render the text in the center of the rect
        name_surf = font.render(self.name, False, (255,255,255))
        name_border_surf = font.render(self.name, False, (0,0,0))

        utils.render_bordered(screen, name_surf, name_border_surf, Vec(self.pos.x+self.width/2 - name_surf.get_width()/2, self.pos.y + self.height/2 - name_surf.get_height()/2))
        

