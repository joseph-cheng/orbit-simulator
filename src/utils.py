import pygame
from vec import Vec
import math

#Render a certain surface with a border around
#This works by blitting 8 of the border surfaces around the inner surf
def render_bordered(screen, inner_surf, border_surf, pos):
    screen.blit(border_surf, (pos.x-1, pos.y))
    screen.blit(border_surf, (pos.x-1, pos.y-1))
    screen.blit(border_surf, (pos.x, pos.y-1))
    screen.blit(border_surf, (pos.x+1, pos.y-1))
    screen.blit(border_surf, (pos.x+1, pos.y))
    screen.blit(border_surf, (pos.x+1, pos.y+1))
    screen.blit(border_surf, (pos.x, pos.y+1))
    screen.blit(border_surf, (pos.x-1, pos.y+1))

    
    screen.blit(inner_surf, (pos.x, pos.y))
    
#Render lighting effects for all the bodies
def render_body_lighting(screen, camera, shadow, bodies):

    #The shadow texture is a square, so I can just take the width and assume it is the height
    shadow_size = shadow.get_size()[0]
    #Create a surface that has the same size as the screen to blit the shadow textures to
    shadow_layer = pygame.Surface(camera.screen_size.to_tuple())

    window_radius = camera.screen_size.magnitude()/2

    
    for body in bodies:
        
        #Make sure that if the body is off the screen, don't render a shadow
        if (Vec.from_tuple(body.screen_coords)-camera.screen_size/2).magnitude() < window_radius + body.screen_radius:

            
            for light_body in bodies:
                #Find the bodies that emit light
                if light_body.emits_light and light_body.name != body.name:
                    #Find the angle between the two bodies and convert it to degrees
                    angle = -(math.atan2((light_body.pos - body.pos).y, (light_body.pos - body.pos).x)) * 180 / math.pi

                    #Rotate and scale the shadow image so that it overlays the body and faces the light body
                    #If you do the maths, you would think it should be body.screen_radius*2 not body.screen_radius*2.05, but without the extra .05, there is a ring of unshadowed pixels around the planet
                    transformed_shadow = pygame.transform.rotozoom(shadow, angle, (body.screen_radius*2.05)/shadow_size)
                    new_shadow_size = transformed_shadow.get_size()[0]/2

                    #Blit the shadow of the body to the shadow layer
                    shadow_layer.blit(transformed_shadow, (body.screen_coords[0]-new_shadow_size, body.screen_coords[1] - new_shadow_size))
                    
    #Blit the shadow layer to the screen but blend the shadows on to the body
    screen.blit(shadow_layer, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

#Draw the labels (i.e. names) of each body
def render_body_labels(screen, bodies, font):
    for body in bodies:
        name_surf = font.render(body.name, False, (255,255,255))
        name_border_surf = font.render(body.name, False, (0,0,0))
        render_bordered(screen, name_surf, name_border_surf, Vec(body.screen_coords[0] - name_surf.get_width()/2, body.screen_coords[1]+body.screen_radius))
    
