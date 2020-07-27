import pygame
from vec import Vec
import utils

#Stores a description and IntPointer variable
class InfoLabel:
    def __init__(self, description, variable, pos):
        self.description = description

        #IntPointer
        self.variable = variable

        self.pos = pos

    #Renders the label to the screen
    def render(self, screen, font):
        description_surf = font.render(self.description, False, (255,255,255))
        description_border_surf = font.render(self.description, False, (0,0,0))

        #I round the variable so that it does not go off the screen
        var_surf = font.render(str(round(self.variable.var, 2)), False, (255,255,255))
        var_border_surf = font.render(str(round(self.variable.var, 2)), False, (0,0,0))

        #Draw the description and variable with a border
        utils.render_bordered(screen, description_surf, description_border_surf, self.pos)
        utils.render_bordered(screen, var_surf, var_border_surf, Vec(self.pos.x, self.pos.y+20))
