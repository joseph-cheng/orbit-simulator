import pygame
import body
import camera
import slider
import renderer
import random
import naming
from vec import Vec
from intpointer import IntPointer
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import os
import pickle
import button
import copy
import bodyplacer
import dropdownmenu
import infolabel
import scale
import flags_file
import string
import math

# State class that stores all bodies and certain mathematical constants
class State:
    
    def __init__(self, w, h):
        self.G = 6.67384 * (10**-11)
        self.bodies = []
        self.camera = camera.Camera(w,h)
        self.w = w
        self.h = h
        self.FPS = 100

        self.update_count = 0
        self.updates_per_render = 15


        #Renderer object
        self.renderer = renderer.Renderer(w, h)
        
        # dt is the timestep in seconds
        self.dt = IntPointer(30000.0 * self.FPS)

        #Stack of mouse objects. The first item in the list should be prioritised last
        self.mouse_objects_stack = [self.camera]

        #List of infolabels that exist
        self.infolabels = []

        #Add all gui elements
        self.add_gui()

        self.body_being_created = None

        self.editing_body = False

        #The current mouse object that is being clicked
        self.grabbed_mouse_object = None

        #Stores the options flags (e.g. render_tracers, render_planet_labels)
        self.flags = flags_file.RENDER_TRACERS + flags_file.RENDER_PLANET_LABELS + flags_file.SHADOWS + flags_file.REALISTIC

        self.planet_shadow = pygame.image.load("../res/shadow.png")

    #Given a new resolution, update renderer and camera res
    def update_resolution(self, new_w, new_h):
        self.camera.update_resolution(new_w, new_h)
        self.w = new_w
        self.h = new_h
        self.renderer.update_resolution(new_w, new_h)
   
        
    # Method that adds a body to the list of bodies
    def add_body_to_game(self, b):

        #Create a list of all the names of bodies
        body_names = [body.name for body in self.bodies]

        #Make sure that if the name of the body already exists, append _'s until the name is unique
        #We need to do this because parts of the code (such as removing buttons from the 'bodies' drop down list) require the names to uniquely identify a body
        while b.name in body_names:
            b.name += "_"

        self.bodies.append(b)
        
        #Find the drop down menu and add the new body
        for mouse_object in self.mouse_objects_stack:
            if isinstance(mouse_object, dropdownmenu.DropDownMenu) and mouse_object.name == "Bodies":
                mouse_object.add_button(b.name, lambda body=b: [self.camera.track_body(body), self.edit_existing_body(body)], self.renderer.font_medium, self.mouse_objects_stack)

    #Add GUI elements to start creating a new body
    def start_creating_new_body(self):

        #Make sure a body is not already being created
        if self.body_being_created != None:
             return

        self.remove_planet_info_labels()
        self.finish_editing_body()
        self.camera.stop_tracking()
        #Initialise a default body
        self.body_being_created = body.Body("", 1 * 10 **6, 1 * 10 ** 20, Vec(0,0), Vec(0,0), (100,100,100))

        #Add the 'Body Placer'
        self.mouse_objects_stack.append(bodyplacer.BodyPlacer(self.body_being_created.pos, self.body_being_created.vel, self.camera))

        #Add the GUI elements
        self.mouse_objects_stack.append(slider.Slider("Radius", self.body_being_created.radius, 1, 1 * 10 ** 10, self.body_being_created.radius.var, Vec(10, 160), 200, 10, 10, interpolation_type=1))
        self.mouse_objects_stack.append(slider.Slider("Mass", self.body_being_created.mass, 1, 1 * 10 ** 36, self.body_being_created.mass.var, Vec(10, 240), 200, 10, 10, interpolation_type=1))
        
        self.mouse_objects_stack.append(slider.Slider("Red", self.body_being_created.colour[0], 0, 255, self.body_being_created.colour[0].var, Vec(10, 320), 200, 10, 10))
        self.mouse_objects_stack.append(slider.Slider("Green", self.body_being_created.colour[1], 0, 255, self.body_being_created.colour[1].var, Vec(10, 400), 200, 10, 10))
        self.mouse_objects_stack.append(slider.Slider("Blue", self.body_being_created.colour[2], 0, 255, self.body_being_created.colour[2].var, Vec(10, 480), 200, 10, 10))

        self.mouse_objects_stack.append(button.Button("Done", Vec(10, 560), 100, 30, self.add_new_body, self.renderer.font_medium))
        self.mouse_objects_stack.append(button.Button("Cancel", Vec(130, 560), 100, 30, self.cancel_creating_new_body, self.renderer.font_medium))



    #Add the body being currently created by the start_creating_new_body function
    def add_new_body(self):



        #Remove the additional GUI elements
        for i in range(8):
            self.mouse_objects_stack.pop()
        
        #I have to make a deepcopy otherwise when it is set to None, the element in the list is set to none
        self.add_body_to_game(copy.deepcopy(self.body_being_created))
        self.body_being_created = None


    #Cancels the operations donw when creating the new body
    def cancel_creating_new_body(self):
        #Remove the body being created
        self.body_being_created = None

        #Remove the additional GUI elements
        for i in range(8):
            self.mouse_objects_stack.pop()

    #Add the GUI elements to edit an existing body
    def edit_existing_body(self, body):

        #If a body is already being edited, switch to editing the new body instead
        if self.editing_body:
            self.finish_editing_body()
        if self.infolabels:
            self.remove_planet_info_labels()
        
        self.editing_body = True
        self.mouse_objects_stack.append(slider.Slider("Radius", body.radius, 1, 1 * 10 ** 10, body.radius.var, Vec(10, 160), 200, 10, 10, interpolation_type=1))
        self.mouse_objects_stack.append(slider.Slider("Mass", body.mass, 1, 1 * 10 ** 36, body.mass.var, Vec(10, 240), 200, 10, 10, interpolation_type=1))
        
        self.mouse_objects_stack.append(slider.Slider("Red", body.colour[0], 0, 255, body.colour[0].var, Vec(10, 320), 200, 10, 10))
        self.mouse_objects_stack.append(slider.Slider("Green", body.colour[1], 0, 255, body.colour[1].var, Vec(10, 400), 200, 10, 10))
        self.mouse_objects_stack.append(slider.Slider("Blue", body.colour[2], 0, 255, body.colour[2].var, Vec(10, 480), 200, 10, 10))
        
        self.mouse_objects_stack.append(button.Button("Delete", Vec(10, 560), 100, 30, lambda body=body: self.delete_body_during_editing(body), self.renderer.font_medium))

        self.mouse_objects_stack.append(button.Button("Done", Vec(130, 560), 100, 30, self.finish_editing_body, self.renderer.font_medium))


        self.infolabels.append(infolabel.InfoLabel("Velocity (m/s)", body.vel_magnitude, Vec(640, 50)))
        self.infolabels.append(infolabel.InfoLabel("Accel (m/s^2)", body.accel_magnitude, Vec(640, 100)))

    #Remove the GUI elements to edit an existing body
    def finish_editing_body(self):

        if self.editing_body:
            self.editing_body = False

            for _ in range(7):
                self.mouse_objects_stack.pop()
                
    #Remove the curret info labels displaying about a planet
    def remove_planet_info_labels(self):
        if self.infolabels:
            for _ in range(2):
                self.infolabels.pop()
        
    #Delete a body and remove all the GUI elements that need it
    def delete_body_during_editing(self, body):

        self.finish_editing_body()
        self.bodies.remove(body)
        
        #Find the 'bodies' drop down list and remove the correct body
        for mouse_object in self.mouse_objects_stack:
            if isinstance(mouse_object, dropdownmenu.DropDownMenu) and mouse_object.name == "Bodies":
                mouse_object.remove_button(body.name, self.mouse_objects_stack)

                break
        self.remove_planet_info_labels()
        self.camera.stop_tracking()

    # Generates a random solar system, having one star and a number of planets that orbit that star
    def generate_solar_system(self):

        self.finish_editing_body()
        self.remove_planet_info_labels()
        self.camera.stop_tracking()

        #Save a backup of the old solar system just in case they clicked it by accident
        self.save_bodies(filename="..\\save_states\\backup.stt")
        #Remove the current bodies
        self.bodies = []
        
        #Reset the bodies drop down list and mouse objects stack
        #Remove all buttons from the drop down list and the mouse object stack
        #I start at 1: because i don't want to remove the 'None' button
        for mouse_object in self.mouse_objects_stack:
            if isinstance(mouse_object, dropdownmenu.DropDownMenu) and mouse_object.name == "Bodies":
                for button in mouse_object.buttons[1:]:
                    self.mouse_objects_stack.remove(button)
                    mouse_object.buttons.remove(button)

        #Create a constellation name  
        constellation = random.choice(naming.constellations)

        #Create a star name using the Bayer Designation
        star_name = random.choice(naming.greek_letters) + " " + constellation

        num_bodies = random.randint(3, 10)
        body_names = []

        #Create distinct planet names for each of the planets by the naming convention '[number] [constellation] [letter]'
        while len(body_names) < num_bodies:
            
            body_name = "%d %s %s" % (random.randint(1, 100), constellation, random.choice(string.ascii_letters))

            #Make sure if we have already generated this name, then generate a new one
            if body_name not in body_names:
                body_names.append(body_name)


        #Stars generally range from cyan to yellow, so I found that keeping green at a fixed value and keeping red and green to add to make 255 worked well to generate star colours
        star_red = random.randint(0, 255)

        #Add the star to the game
        star = body.Body(star_name, random.randint(1*10**8, 5*10**9), random.randint(1*10**27, 1*10**32), Vec(0,0), Vec(0,0), (star_red, 255, 255-star_red), emits_light=True)

        self.add_body_to_game(star)

        #Generate all of the bodies
        for body_num in range(num_bodies):
            body_mass = random.randint(1*10**22, 1*10**26)
            body_distance_from_sun = star.radius.var + random.randint(1*10**9, 1*10**12)

            """
            To calculate the velocity to keep the planet in orbit around the sun:
            G = universal gravitational constant
            M = mass of sun
            m = mass of body
            r = distance of body away from sun
            v = velocity of planet
            
            Centripetal force = GMm/r^2
            Centripetal force = mv^2/r
            GMm/r^2 = mv^2/r
            GM/r^2 = v^2/r
            GM/r = v^2
            sqrt(GM/r) = v
            """
            angle = random.uniform(0, 2*math.pi)
            body_velocity = math.sqrt(self.G * star.mass.var / body_distance_from_sun)
            self.add_body_to_game(body.Body(body_names[body_num],
                                            random.randint(1*10**6, 1*10**8),
                                            body_mass,
                                            Vec(math.cos(angle) * body_distance_from_sun, math.sin(angle) * body_distance_from_sun),
                                            Vec(math.sin(angle) * body_velocity         , -math.cos(angle) * body_velocity),
                                            (random.randint(0,255), random.randint(0, 255), random.randint(0,255))))
    
    #Given a flag, toggle that flag
    def change_flags(self, flag):
        #If flag is set, unset flag
        if self.flags & flag:
            self.flags -= flag
        #if flag is not set, set flag
        else:
            self.flags += flag
             
    # Method that updates the state
    def update(self):

        #If we are not paused, then move all of the bodies accordingly
        if not(self.flags & flags_file.PAUSED):
            
            #Find the resultant force acting on each body
            for body in self.bodies:
                body.find_force(self.bodies, self.G)

            #Move all the bodies accordingly
            for body in self.bodies:

                #dt is the number of seconds that pass for each second of simulation time, so to find the number of seconds that have passed
                #For one update, we need to divide by the fps and the number of updates per render
                body.update((self.dt.var/self.FPS)/self.updates_per_render)

        #Update the camera and scale
        #This occurs regardless of if the simulation is paused or not
        self.camera.update()
        self.scale.update_scale(1/self.camera.zoom)
    
    #Procedure that opens a file dialog box to save the current state to and then serialises the current state and saves it as a file
    def save_bodies(self, filename=""):

        if filename == "":
            #If I don't create and withdraw the root, a small Tk window opens which I don't want, so I have to create and withdraw the root
            root = tkinter.Tk()
            root.withdraw()

            #Gets the current path of this script (state.py)
            #the [-4:] is to remove the src\
            #I tried putting ..\ in the initialdir but it did not work
            root_path = os.path.dirname(os.path.realpath(__file__))[:-4]

            #Opens a diaglox box where the user is asked to save the current state object
            filename = tkinter.filedialog.asksaveasfilename(initialdir = root_path + "\\save_states", title = "Select file", filetypes = (("state files", "*.stt"), ("all files", "*.*")))
            
            #If filename is an empty string, the file dialog was closed
            if filename == "":
                return

            #Make sure that if they manually enter .stt, .stt is not appended
            if filename[-4:] != ".stt":
                filename += ".stt"

        #Open the selected file
        file = open(filename, "wb")
        #Serialise the current bodies and camera to the correct file
        pickle.dump([self.bodies, self.camera], file)

    #Procedure that opens a file dialog box and opens a state file and deserialises it and returns the state object
    def load_bodies(self, filename=""):

        if filename == "":
            #If I don't create and withdraw the root, a small Tk window opens which I don't want, so I have to create and withdraw the root
            root = tkinter.Tk()
            root.withdraw()

            #Gets the current path of this script (state.py)
            #the [-4:] is to remove the src\
            #I tried putting ..\ in the initialdir but it did not work
            root_path = os.path.dirname(os.path.realpath(__file__))[:-4]

            #Opens a diaglox box where the user is asked to open a state object
            filename = tkinter.filedialog.askopenfilename(initialdir = root_path + "\\save_states", title = "Select file", filetypes = (("state files", "*.stt"), ("all files", "*.*")))

            #If filename is an empty string, the file dialog was closed
            if filename == "":
                return


        self.finish_editing_body()
        self.camera.stop_tracking()
        #Open the selected file
        file = open(filename, "rb")
        
        #Deserialise and load the bodies and camera
        try:
            bodies, self.camera = pickle.load(file)
        #If the unpickling fails, we know we have an invalid state file, so display an error message.
        except pickle.UnpicklingError:
            tkinter.messagebox.showerror("Error", "Invalid state file")
            return
            


        #Reset the bodies drop down list and mouse objects stack
        #Remove all buttons from the drop down list and the mouse object stack
        #I start at 1: because i don't want to remove the 'None' button
        for mouse_object in self.mouse_objects_stack:
            if isinstance(mouse_object, dropdownmenu.DropDownMenu) and mouse_object.name == "Bodies":
                for button in mouse_object.buttons[1:]:
                    self.mouse_objects_stack.remove(button)
                    mouse_object.buttons.remove(button)

        #Remove all current info labels
        self.infolabels = []
        #Reset the bodies list and add the new bodies
        self.bodies = []
        
        for body in bodies:
            self.add_body_to_game(body)
        

        #When the new camera is loaded, the old camera at mouse_objects_stack[0] does not point to the new camera, so we need to update it
        self.mouse_objects_stack[0] = self.camera
        self.camera.update_resolution(self.w, self.h)

    #Procedure that adds all the static GUI elements to the screen
    def add_gui(self):

        #Quick function to format the time in the speed multiplier
        def format_time(x):
            if x > 31557600:
                return str(round(x/31557600, 3)) + " years/s"
            if x > 2592000:
                return str(round(x/2592000, 3)) + " months/s"
            if x > 604800:
                return str(round(x/604800, 3)) + " weeks/s"
            if x > 86400:
                return str(round(x/86400, 3)) + " days/s"
            if x > 3600:
                return str(round(x/3600, 3)) + " hours/s"
            if x > 60:
                return str(round(x/60, 3)) + " minutes/s"
            return str(round(x, 3)) + " seconds/s"

        # Add the GUI objects
        self.mouse_objects_stack.append(slider.Slider("Speed multiplier", self.dt, 1, 50000000, self.dt.var, Vec(410, 10), 200, 10, 10, var_formatter=format_time, interpolation_type=1))
        self.scale = scale.Scale(Vec(630, 10), 150, 10, 1/(self.camera.zoom))

        self.mouse_objects_stack.append(dropdownmenu.DropDownMenu("File", Vec(0,0), 100, 30))
        self.mouse_objects_stack[-1].add_button("Save", self.save_bodies, self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-2].add_button("Load", self.load_bodies, self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-3].add_button("Random", self.generate_solar_system, self.renderer.font_medium, self.mouse_objects_stack)

        self.mouse_objects_stack.append(dropdownmenu.DropDownMenu("Options", Vec(297,0), 100, 30))
        self.mouse_objects_stack[-1].add_button("Tracers", lambda: self.change_flags(flags_file.RENDER_TRACERS), self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-2].add_button("Labels", lambda: self.change_flags(flags_file.RENDER_PLANET_LABELS), self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-3].add_button("Shadows", lambda: self.change_flags(flags_file.SHADOWS), self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-4].add_button("Unrealistic", lambda: self.change_flags(flags_file.REALISTIC), self.renderer.font_medium, self.mouse_objects_stack, toggled_name="Realistic")
        self.mouse_objects_stack[-5].add_button("Pause", lambda: self.change_flags(flags_file.PAUSED), self.renderer.font_medium, self.mouse_objects_stack, toggled_name="Unpause")
        self.mouse_objects_stack[-6].add_button("Fullscreen", lambda: self.renderer.toggle_fullscreen(self), self.renderer.font_medium, self.mouse_objects_stack)
        self.mouse_objects_stack[-7].add_button("Quit", pygame.quit, self.renderer.font_medium, self.mouse_objects_stack)
        
        self.mouse_objects_stack.append(button.Button("Add body", Vec(99, 0), 100, 30, self.start_creating_new_body, self.renderer.font_medium))
        
        self.mouse_objects_stack.append(dropdownmenu.DropDownMenu("Bodies", Vec(198, 0), 100, 30))
        self.mouse_objects_stack[-1].add_button("None", lambda: [self.camera.stop_tracking(), self.finish_editing_body(), self.remove_planet_info_labels()], self.renderer.font_medium, self.mouse_objects_stack)
        for body in self.bodies:
                self.mouse_objects_stack[-1].add_button(body.name, lambda body=body: [self.camera.track_body(body), self.edit_existing_body(body)], self.renderer.font_medium, self.mouse_objects_stack)


