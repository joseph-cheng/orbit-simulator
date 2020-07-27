import pygame
from vec import Vec
import utils
from math import log

#Slider mouse object class used to alter values such as radius of body or timescale
class Slider:
    def __init__(self, variable_name, variable, min_value, max_value, default_value, pos, width, button_width, button_height, interpolation_type=0, var_formatter=lambda x: str(round(x, 3))):

        #Name of the slider is changing (e.g. radius, timescale)
        self.variable_name = variable_name
        #Actual SliderValue object that will be changed
        self.variable = variable

        #Minimum value the slider can take
        self.min_value = min_value
        #Maximum value the slider can take
        self.max_value = max_value

        #Actual value of the slider
        self.value = default_value


        #Interpolation type (linear, logarithmic, etc.)
        #0: linear
        #1: logarithmic
        self.interpolation_type = interpolation_type

        #Function that formats the variable so it can be displayed in different ways, e.g. for time you might want to change it to days, months, etc.
        #Default is just to round to 3 d.p.
        self.var_formatter = var_formatter

        #Position to draw the slider at
        self.pos = pos
        #Width of the slider
        self.width = width

        #This will store where the current button pos and mouse pos are when the slider is grabbed
        self.grabbed_mouse_pos = None
        self.grabbed_button_pos = None

        #Width and height of the button
        self.button_width = button_width
        self.button_height = button_height
        self.button_pos = self.value_to_pos(self.value)
        
        self.click_rect = pygame.Rect(self.button_pos.x - self.button_width/2, self.button_pos.y - self.button_height/2, self.button_width, self.button_height)
        

    #Takes in a value of the slider and returns the position it should be
    def value_to_pos(self, value):

        

        #Linear
        if self.interpolation_type == 0:  
            return self.pos + Vec((self.width*(value-self.min_value))/(self.max_value-self.min_value), 0)
        
        #Logarithmic
        if self.interpolation_type == 1:

            return self.pos + Vec((log(value)-log(self.min_value))/(log(self.max_value)-log(self.min_value)) * self.width , 0)

    #Takes in a button position and returns the value at this point
    def pos_to_value(self, pos):

        distance_across = pos.x-self.pos.x

        f = distance_across/self.width
        
        #Linear
        if self.interpolation_type == 0:
            return f*self.max_value + (1-f)*self.min_value
        
        #Logarithmic
        if self.interpolation_type == 1:
            return (self.max_value ** f) * self.min_value ** (1-f)

    #Getter for the value
    def get_current_value(self):
        return self.value

    #When clicked, get the grabbed positions of mouse and slider
    def on_button_click(self, mouse_pos):

        #Get the current x and mouse x when it is clicked
        self.grabbed_mouse_pos = mouse_pos[0]
        self.grabbed_button_pos = self.button_pos.x


    #When the button is held down, move the button position and click rect based on where the mouse has moved
    def on_button_down(self, mouse_pos):

        pos = (self.grabbed_button_pos + mouse_pos[0] - self.grabbed_mouse_pos)
        if pos > self.pos.x + self.width:
            pos = self.pos.x + self.width
        elif pos < self.pos.x:
            pos = self.pos.x
        self.button_pos = Vec(pos, self.button_pos.y)
        self.click_rect = pygame.Rect(self.button_pos.x - self.button_width/2, self.button_pos.y - self.button_height/2, self.button_width, self.button_height)
        self.value = self.pos_to_value(self.button_pos)
        self.variable.var = self.value
    def on_button_release(self, mouse_pos):
        pass

    def render(self, screen, font):

        #Draw the line of the slider and the clickable square
        pygame.draw.line(screen, (100,100,100), self.pos.to_tuple(), (self.pos.x+self.width, self.pos.y))
        pygame.draw.rect(screen, (255,255,255), self.click_rect)

        variable_name_surf = font.render(self.variable_name, False, (255,255,255))
        variable_name_border_surf = font.render(self.variable_name, False, (0,0,0))
        
        value_surf = font.render(self.var_formatter(self.value), False, (255,255,255))
        value_border_surf = font.render(self.var_formatter(self.value), False, (0,0,0))

        utils.render_bordered(screen, variable_name_surf, variable_name_border_surf, Vec(self.pos.x, self.pos.y+self.button_height))
        utils.render_bordered(screen, value_surf, value_border_surf, Vec(self.pos.x, self.pos.y+self.button_height+25))
        

