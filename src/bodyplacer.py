import pygame
from vec import Vec
import tkinter as tk

#Mouse object to choose position and velocity  of body when it is being created
class BodyPlacer:
    def __init__(self, body_pos, body_vel, camera):


        # GUI objects have no update function, but when the window is resized, the click_rect of the body placer, does not change, so if you increase the size
        # of the screen, you can move the camera in the places where the window has expanded (because the camera updates its click_rect), so in order to fix
        # this, I just set the click rect to be the size of the screen

        # Get the size of the screen using tkinter
        root = tk.Tk()
        root.withdraw()
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()

        #Clickable rect for the body placer, this covers the entire screen
        self.click_rect = pygame.Rect(0, 0, w, h)

        self.body_pos = body_pos
        self.body_vel = body_vel
        
        self.pos_placing = None
        self.vel_placing = Vec(0,0)

        #Copy of the camera needed to find out where to place the body in game
        self.camera = camera

    def on_button_click(self, mouse_pos):
        self.pos_placing = self.camera.screen_to_world(Vec.from_tuple(mouse_pos))
        self.body_pos.x = self.pos_placing.x
        self.body_pos.y = self.pos_placing.y
        
    def on_button_down(self, mouse_pos):
        self.vel_placing = self.pos_placing - self.camera.screen_to_world(Vec.from_tuple(mouse_pos))

    def on_button_release(self, mouse_pos):

        self.body_vel.x = self.vel_placing.x*self.camera.zoom * 1000
        self.body_vel.y = self.vel_placing.y*self.camera.zoom * 1000

    def render(self, screen, font):

        if self.pos_placing != None and self.vel_placing != None:
        
            pygame.draw.line(screen, (255,255,255), self.camera.world_to_screen(self.pos_placing).to_tuple(), self.camera.world_to_screen(self.pos_placing+self.vel_placing).to_tuple())
        
