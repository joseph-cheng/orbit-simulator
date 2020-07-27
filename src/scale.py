import pygame
import utils
from vec import Vec

# Scale class to display the current scale of the system in kilometers per pixel
class Scale:
    def __init__(self, pos, width, height, scale):
        
        #Scale in meters per pixel for ease of use
        self.scale = scale
        self.pos = pos
        self.width = width
        self.height = height

    #Setter for scale
    def update_scale(self, new_scale):
        self.scale = new_scale

    #Renders the scale on the screen
    def render(self, screen, font):

        #Draw the line between the start and end
        pygame.draw.line(screen, (255,255,255), (self.pos.x, self.pos.y), (self.pos.x+self.width, self.pos.y))

        #Draw the small lines at either end of the scale
        pygame.draw.line(screen, (255,255,255), (self.pos.x, self.pos.y+self.height//2), (self.pos.x, self.pos.y-self.height//2))
        pygame.draw.line(screen, (255,255,255), (self.pos.x+self.width, self.pos.y+self.height//2), (self.pos.x+self.width, self.pos.y-self.height//2))

        #Convert the scale to km/pixel when displaying it because it makes more sense
        scale_surf = font.render(str(round(self.scale/1000) * self.width) + " km", False, (255,255,255))
        scale_border_surf = font.render(str(round(self.scale/1000) * self.width) + " km", False, (0,0,0))
        utils.render_bordered(screen, scale_surf, scale_border_surf, Vec(self.pos.x+self.width/2 - scale_surf.get_width()/2, self.pos.y+self.height))
        
