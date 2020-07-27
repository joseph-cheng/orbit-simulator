from vec import Vec
import pygame

#Camera class with a zoom scale and a position vector (works in simulation coords)
class Camera:
    def __init__(self, w, h):
        # Zoom scale
        self.zoom = 0.000000001
        self.target_zoom = self.zoom

        #Actual width and height of the screen
        self.screen_size = Vec(w,h)
        
        #Width and height of the current viewport
        self.size = Vec(w/self.zoom, h/self.zoom)
        self.target_size = self.size
        
        # Top left of camera
        self.pos = Vec((-w/2)/self.zoom, (-h/2)/self.zoom)
        self.target_pos = self.pos

        # Factor to tween the towards the target position/size/zoom
        self.tween_factor = 0.01

        # Start position of mouse and camera when it is grabbed
        self.grabbed_mouse_pos = None
        self.grabbed_camera_pos = None

        self.click_rect = pygame.Rect(0,0, w, h)

        self.tracked_body = None

    # Update all the aspects of the camera that depend on the resolution (screen_size, click_rect, etc.)
    def update_resolution(self, new_w, new_h):
        self.screen_size.x = new_w
        self.screen_size.y = new_h
        self.size.x = new_w/self.zoom
        self.size.y = new_h/self.zoom
        self.click_rect.width = new_w
        self.click_rect.height = new_h
        self.target_size = self.size
        
    def on_button_click(self, mouse_pos):
        self.grabbed_mouse_pos = Vec.from_tuple(mouse_pos)
        self.grabbed_pos = self.pos

    def on_button_down(self, mouse_pos):
        self.target_pos = self.grabbed_pos + (self.grabbed_mouse_pos - Vec.from_tuple(mouse_pos))/self.zoom
    
    def on_button_release(self, mouse_pos):
        pass

    # Converts a world coordinate into where it should exist on the screen
    def world_to_screen(self, point):
        return (point-self.pos)*self.zoom

    # Converts a screen coordinate to where it exists in the world
    def screen_to_world(self, point):
        
        return point/self.zoom + self.pos

    #Takes in a point (as a Vec) and returns True if it is visible on the screen and False if not
    def point_on_screen(self, point):
        screen_point = self.world_to_screen(point)

        if screen_point.x < 0 or screen_point.x > self.screen_size.x or screen_point.y < 0 or screen_point.y > self.screen_size.y:
            return False
        return True

    # Zooms at a point either in or out and moves the camera accordingly so the point stays in the same place on the screen
    def zoom_at_point(self, delta, point):

        # Calculate the new zoom and viewport size
        new_zoom = self.zoom + delta*self.zoom

        #Cap the zoom: There is a bug which I cannot currently fix where if you zoom in too far, the bodies stop rendering
        #if new_zoom > 1/23000:
        #    return
        new_size = self.screen_size / new_zoom

        # Calculates how far right and down the point is on the screen as a percentage
        point_screen_proportions = point.divide_by_vec(self.screen_size)


        #Set the target position to where it should be
        self.target_pos = self.pos - point_screen_proportions.multiply_vec(new_size - self.size)
        self.target_zoom = new_zoom
        self.target_size = new_size
        
    # Setter for target pos
    def set_target_pos(self, target_pos):
        self.target_pos = target_pos

    #Setter for tracked_body
    def track_body(self, body):
        self.tracked_body = body

    #Stops tracking 
    def stop_tracking(self):
        self.tracked_body = None

    # Updates the camera towards the target zoom and position
    def update(self):

        self.pos += (self.target_pos - self.pos) * self.tween_factor
        self.zoom += (self.target_zoom - self.zoom) * self.tween_factor


        self.size += (self.target_size - self.size) * self.tween_factor

        #If we are tracking a body, set the centre of the camera to the pos of the tracked body
        if self.tracked_body:
            self.pos = self.tracked_body.pos - self.size/2
        


