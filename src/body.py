from vec import Vec
import math
import pygame
from state import State
from intpointer import IntPointer
import flags_file

# Body class used to represent celestial bodies such as moons, planets, etc.
class Body:
    def __init__(self, name, radius, mass, pos, vel, colour, emits_light=False):


        self.name = name
        
        self.radius = IntPointer(radius)
        self.mass = IntPointer(mass)

        self.pos = pos
        self.vel = vel
        self.vel_magnitude = IntPointer(vel.magnitude())
        self.accel = Vec(0,0)
        self.old_accel = Vec(0,0)
        self.accel_magnitude = IntPointer(self.accel.magnitude())
        self.force = Vec(0,0)

        self.emits_light = emits_light

        # list of previous coordinates in order to draw a tracer behind
        self.previous_coords = []

        # Maximum length of tracer
        self.tracer_length = 250

        
        self.updates_since_tracer_added = 0
        self.updates_since_tracer_added_limit = 10

        # Colour of planet and trail
        self.colour = (IntPointer(colour[0]), IntPointer(colour[1]), IntPointer(colour[2]))

        self.screen_radius = None
        self.screen_coords = None

    # Method that finds the force applied on the body based on gravitational force between all other bodies
    def find_force(self, bodies, G):
        # Simulate interaction with all other bodies

        self.force = Vec(0, 0)
        
        for other in bodies:
            # We don't want to interact with ourself
            if other == self:
                continue
            
            # Equation from here to calculate force https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

            #If two planets end up being in the exact same location, you end up dividing by zero when finding the magnitude,
            #So I check if the two bodies are at the same place, and if they are, then I said the foce magnitude to be -inf
            if (self.pos - other.pos).magnitude2() == 0:
                force_magnitude = -9e9999999
            else:
                force_magnitude = -((self.mass.var * other.mass.var) / (self.pos - other.pos).magnitude2()) * G
            force_angle = math.atan2(self.pos.y-other.pos.y, self.pos.x-other.pos.x)
            self.force += Vec(force_magnitude*math.cos(force_angle), force_magnitude*math.sin(force_angle))


    # Applies the current force and moves the body accordingly
    def update(self, dt):

        #If needed, remove the oldest element in the tracer
        if len(self.previous_coords) > self.tracer_length:
            self.previous_coords.pop(0)

        # Verlet integration to calculate acceleration, velocity, and position

        self.old_accel = self.accel.copy()
        self.accel = self.force / self.mass.var
        self.vel += (self.old_accel + self.accel) * dt * 0.5
        self.pos += self.vel * dt + (self.old_accel + self.accel) * 0.25 * dt**2


        #Update the magnitudes of velocity and accel
        self.vel_magnitude.var = self.vel.magnitude()
        self.accel_magnitude.var = self.accel.magnitude()

        #Add the current position to the list of previous positions, but we only want to do this every so often to increase tracer length and reduce lag
        if self.updates_since_tracer_added == self.updates_since_tracer_added_limit:
            self.previous_coords.append(self.pos)
            self.updates_since_tracer_added = 0
  
        self.updates_since_tracer_added += 1
        
    def render(self, screen, camera, flags):

        col = (self.colour[0].var, self.colour[1].var, self.colour[2].var)


        if flags & flags_file.REALISTIC:
            self.screen_radius = int(self.radius.var * camera.zoom)
        else:
            self.screen_radius = int(math.log(self.radius.var))
        self.screen_coords = camera.world_to_screen(self.pos).int_cast().to_tuple()

        #Optimisation - if the body is not in the frame then do not render it
        window_radius = camera.screen_size.magnitude()/2

        if (Vec.from_tuple(self.screen_coords)-camera.screen_size/2).magnitude() < window_radius + self.screen_radius:

            pygame.draw.circle(screen,
                                col,
                                self.screen_coords,
                                self.screen_radius)

        if flags & flags_file.RENDER_TRACERS:

            # Create a list with all the points that should be drawn. I apply a map to them that converts them to
            # world coordinates, converts them to integeres and then to a tuple

            

            lines_to_draw = list(map(lambda pos: camera.world_to_screen(pos).int_cast().to_tuple(),
                                     self.previous_coords + [self.pos]))


            #Render a tracer behind each body, it can only be drawn with more than one point
            if len(lines_to_draw) > 1:
                
                pygame.draw.lines(screen,
                                  col,
                                  False,
                                  lines_to_draw)

