# how to execute it in cmd:
# python -m mechanics.15_spaceship_lander

import pygame
import math
import sys
from toolbox import colors, font, particle as particle_lib

# Initializing Pygame
pygame.init()

# Defining the dimentions for our screen
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

palette = colors.PALETTE
pixel_font = font.pixel_font()

# Defining the color to print in the screen
BG_COLOR = palette[0]
FLOOR_COLOR = palette[13]

# CONSTANTS
GRAVITY = 10

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > spaceship lander")

# clock
clock = pygame.time.Clock()

# spaceship imgs reference
spaceship_img = pygame.image.load('./assets/img/spaceship32x32_lr-idle.png').convert_alpha()
spaceship_img_fire = pygame.image.load('./assets/img/spaceship32x32_lr-fire.png').convert_alpha()

# setup floor
tile_floor = pygame.image.load('./assets/img/bg_one.png').convert_alpha()
tile_floor_width, tile_floor_height = tile_floor.get_size()
floor_surface = pygame.Surface((screen.get_width(), tile_floor_height ), pygame.SRCALPHA)

for x in range(0, screen.get_width(), tile_floor_width):
    floor_surface.blit(tile_floor, (x, 0))

# setup spaceship settings
spaceship_rotation = math.degrees(0)
value_rotation = 0
ship_trust = 0
ship_drag = 0.9
spaceship_x = WINDOW_WIDTH / 2
spaceship_y = WINDOW_HEIGHT / 2
spaceship_vel_x = 0
spaceship_vel_y = 0
spaceship_fire = False
spaceship_explodes = False

particles = []

# adding the defs to check if the input is to the left/right
def is_button_down(event):
    return event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN

def is_button_up(event):
    return event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP

def is_input_left_active(event, screen):
    mouse_pos = pygame.mouse.get_pos()
    if is_button_down(event):
        return  mouse_pos[0] < screen.get_width() / 4
    return event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT)
        
def is_input_right_active(event, screen):
    mouse_pos = pygame.mouse.get_pos()
    if is_button_down(event):
        return mouse_pos[0] > ( screen.get_width() / 4 ) * 3
    return event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT)

def is_input_top_active(event, screen):
    mouse_pos = pygame.mouse.get_pos()
    screen_width = screen.get_width()
    if is_button_down(event):
        return mouse_pos[0] > (screen_width / 4) or mouse_pos[0] < ( screen_width/2 ) + ( screen_width/4 ) 
    return event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP)

# Flag to run our loop, it's optional in this example but useful to get used too
while True:
    dt = clock.tick(60) / 1000
    current_time = pygame.time.get_ticks()

    # In this for loop is crazy! because its always listening which event is triggering
    for event in pygame.event.get():
        # And once is equal when a user closes the window
        # it will close the current window in execution 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if is_input_left_active(event, screen):
            value_rotation = -9

        if is_input_right_active(event, screen):
            value_rotation = 9

        if is_input_top_active(event, screen):
            ship_trust = 20
            spaceship_fire = True
        
        if event.type == pygame.KEYUP or is_button_up(event):
            ship_trust = 0
            value_rotation = 0
            spaceship_fire = False

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the missile ref image
    img = spaceship_img_fire if spaceship_fire == True else spaceship_img

    spaceship_rotation += math.radians(value_rotation)
    spaceship_vel_x += math.cos(spaceship_rotation) * ship_trust 
    spaceship_vel_y += math.sin(spaceship_rotation) * ship_trust 

    spaceship_vel_x *= ship_drag
    spaceship_vel_y *= ship_drag

    # detect bounds and limiting the spaceship in the screen
    if(spaceship_y + img.get_rect().height <= 500) and not spaceship_fire:
        spaceship_vel_y += GRAVITY

    spaceship_x += spaceship_vel_x * dt
    spaceship_y += spaceship_vel_y * dt


    rotated_img = pygame.transform.rotate(img, -math.degrees(spaceship_rotation))
    spaceship_rect = rotated_img.get_rect(center=(spaceship_x, spaceship_y))
    screen.blit(rotated_img, spaceship_rect.topleft)

    # wrapping
    if spaceship_x - spaceship_rect.width > WINDOW_WIDTH:
        spaceship_x = 0

    if spaceship_x + spaceship_rect.width < 0:
        spaceship_x = WINDOW_WIDTH

    if spaceship_y + spaceship_rect.height/3 >= 500:
        spaceship_y = 10
        spaceship_explodes = True
        # Create a fountain effect at mouse position
        for _ in range(30):  # Number of particles
            particles.append(particle_lib.Particle(spaceship_x, 500, palette))
        
    if spaceship_y + spaceship_rect.height < 0:
         spaceship_y = 500 - spaceship_rect.height * 2

    # floor edge
    screen.blit(floor_surface, (0, 500))

    # floor bg
    floor_bg_rect = pygame.Rect(0, 505, screen.get_width(), 100)
    pygame.draw.rect(screen, FLOOR_COLOR, floor_bg_rect)

    # explotion
    if spaceship_explodes:
        # Update and draw particles
        for particle in particles[:]:
            particle.update(WINDOW_WIDTH, 500)
            particle.draw(screen)
            if particle.lifetime <= 0 or particle.size <= 0.1:
                particles.remove(particle)
        
        if len(particles) == 0:
            spaceship_explodes = False

    # Draw rotation indicator line and angle
    line_length = 50  # Length of the line in pixels
    line_start = spaceship_rect.center
    line_end = (
        line_start[0] + math.cos(spaceship_rotation) * line_length,
        line_start[1] + math.sin(spaceship_rotation) * line_length
    )
    pygame.draw.line(screen, palette[2], line_start, line_end, 1)
    text_content = f"{int(math.degrees( spaceship_rotation ) % 360 )}°"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(spaceship_rect.left, spaceship_rect.bottom + 20))
    screen.blit(text_surface, text_rect)

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 100))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS