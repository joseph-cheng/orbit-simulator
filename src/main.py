from vec import Vec
import body
import state
import pygame
import renderer
import pickle
import os
import string
import random

#Initialise pygame and create a pygame clock, which will be used to cap the frame rate
pygame.init()
clock = pygame.time.Clock()

#Initial width and height of the screen
w = 800
h = 600

#Initialise the game state
state_obj = state.State(w, h)

#Set the window icon
icon = pygame.image.load("../res/icon.png")
pygame.display.set_icon(icon)

# Key callback function used to register inputs
def key_callback(state_obj):
    #Search through all the inputs/events
    for event in pygame.event.get():
        #Check for red cross in top right
        if event.type == pygame.QUIT:
            pygame.quit()

        #I couldn't find a good way to encapsulate naming the planet within the state so I had to do it in the main file
        if event.type == pygame.KEYDOWN:

            #Check a body is actually being created
            if state_obj.body_being_created != None:

                #The backspace key shouldn't be printed, instead it should remove the last character from the name
                if event.key == pygame.K_BACKSPACE:
                    state_obj.body_being_created.name = state_obj.body_being_created.name[:-1]

                #The return key is displayed as nothing, but still put in the name, so it should not be recognised as valid input
                elif event.key == pygame.K_RETURN:
                    pass

                #If the key is not a special character, just add the unicode to the current name
                else:
                    state_obj.body_being_created.name += event.unicode

        #Check for mouse input
        if event.type == pygame.MOUSEBUTTONDOWN:

            #We do not care where the mouse is when it is being scrolled so
            #we put all the mousewheel handling before finding the object the mouse is over
            # If mousewheel is scrolled up, zoom in
            if event.button == 4:
                state_obj.camera.zoom_at_point(0.4, Vec.from_tuple(event.pos))
                
            # If mousewheel is scrolled down, zoom out
            if event.button == 5:
                state_obj.camera.zoom_at_point(-0.4, Vec.from_tuple(event.pos))


            #Find the mouse opject that is being clicked
            for mouse_object in reversed(state_obj.mouse_objects_stack):
                if mouse_object.click_rect.collidepoint(event.pos):
                    state_obj.grabbed_mouse_object = mouse_object
                    break

            #This should never happen because the camera grabber should always be there but this is a just in case
            if state_obj.grabbed_mouse_object is None:
                break
            
            
            #If LMB is pressed, start perform the object on click function
            if event.button == 1:
                state_obj.grabbed_mouse_object.on_button_click(event.pos)




        #Check for mouse movement
        if event.type == pygame.MOUSEMOTION:

            if state_obj.grabbed_mouse_object is None:
                break
            if event.buttons[0] == 1:
                state_obj.grabbed_mouse_object.on_button_down(event.pos)

        #Check for mouse release
        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:
                if state_obj.grabbed_mouse_object is None:
                    break
                state_obj.grabbed_mouse_object.on_button_release(event.pos)
                state_obj.grabbed_mouse_object = None

        if event.type == pygame.VIDEORESIZE:
            #Set the screen size to 800x600 if it is resized smaller than this. This means that the UI will never be off the screen.
            w, h = event.size
            if w < 800:
                w = 800
            if h < 600:
                h = 600
                
            state_obj.update_resolution(w, h)


#Start the simulation with a random solar system
state_obj.generate_solar_system()


while True:


    key_callback(state_obj)
    
    #Update the state_obj
    state_obj.update()


    state_obj.update_count += 1
    if state_obj.update_count == state_obj.updates_per_render:
        #Cap the framerate at a certain fps
        clock.tick(state_obj.FPS)
        
        #Render the state_obj
        state_obj.renderer.render(state_obj)
        state_obj.update_count = 0
        pygame.display.set_caption("Orbit Simulator - FPS: " + str(round(clock.get_fps(),1)))

