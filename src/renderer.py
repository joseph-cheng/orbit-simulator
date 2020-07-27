import pygame
import math
import tkinter as tk
import body
import utils
import flags_file

#Renderer class used to render everything using pygame
class Renderer:
    def __init__(self, w, h):

        #Dimensions of screen
        self.w = w
        self.h = h

        #Resolution before going fullscreen, so if you toggle back from fullscreen the window goes back to the original size
        self.old_res = (self.w, self.h)
        
        self.fullscreen = False
        
        #Surface to render to
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)

        pygame.font.init()
        self.font_large = pygame.font.SysFont("segoeui", 30)
        self.font_medium = pygame.font.SysFont("segoeui", 16)
        self.font_small = pygame.font.SysFont("segoeui", 13)

    #Updates the screen with a new resolution to allow for fullscreen and resizing
    def update_resolution(self, new_w, new_h):
        self.w = new_w
        self.h = new_h
        self.screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE|(pygame.FULLSCREEN if self.fullscreen else 0))

    def toggle_fullscreen(self, state_obj):

        if not(self.fullscreen):
            self.old_res = (self.w, self.h)

        self.fullscreen = not self.fullscreen
        
        #I use tkinter to find the display size because all the other ways I could find required no display currently set or only worked on wither Linux or Windows platforms, but tkinter is universal
        if self.fullscreen:
            root = tk.Tk()
            root.withdraw()
            w = root.winfo_screenwidth()
            h = root.winfo_screenheight()
        else:
            w,h = self.old_res
        self.screen = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE|(pygame.FULLSCREEN if self.fullscreen else 0))
        

        state_obj.update_resolution(w,h)
    
    # Method that renders the state_obj
    def render(self, state_obj):
        
        #Fill the screen with black
        self.screen.fill((0,0,0))

        #Render each body
        for b in state_obj.bodies:
            b.render(self.screen, state_obj.camera, state_obj.flags)
        
        if state_obj.body_being_created != None:
            state_obj.body_being_created.render(self.screen, state_obj.camera, state_obj.flags)

        if state_obj.flags & flags_file.SHADOWS:
            utils.render_body_lighting(self.screen, state_obj.camera, state_obj.planet_shadow, state_obj.bodies)

        #Rendering the planet labels is moved outside the body.render function in order for them to render over other body's tracers
        if state_obj.flags & flags_file.RENDER_PLANET_LABELS:
            utils.render_body_labels(self.screen, state_obj.bodies + ([state_obj.body_being_created] if state_obj.body_being_created else []), self.font_small)
            

                
        #Render the mouse objects if you can
        for obj in state_obj.mouse_objects_stack:
            if hasattr(obj, 'render') and callable(obj.render):
                obj.render(self.screen, self.font_medium)
        for label in state_obj.infolabels:
            label.render(self.screen, self.font_medium)

        state_obj.scale.render(self.screen, self.font_medium)
        
        #Update the display
        pygame.display.update()



