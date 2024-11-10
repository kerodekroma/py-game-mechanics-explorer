# how to execute it in cmd:
# python -m mechanics.01_acceleration 

import pygame

import sys

from toolbox import colors, font

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

# 
GRAVITY = 200
MAX_SPEED = 500
ACCELERATION = 50

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > acceleration")

# clock
clock = pygame.time.Clock()

# setup dude
dude = pygame.image.load('./assets/img/orangito32x32.png').convert_alpha()
dude_x = 100
dude_y = 250
dude_vel_x = 0
dude_acc_x = 0

# setup floor
tile_floor = pygame.image.load('./assets/img/bg_one.png').convert_alpha()
tile_floor_width, tile_floor_height = tile_floor.get_size()
floor_surface = pygame.Surface((screen.get_width(), tile_floor_height ), pygame.SRCALPHA)

for x in range(0, screen.get_width(), tile_floor_width):
    floor_surface.blit(tile_floor, (x, 0))

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

# Flag to run our loop, it's optional in this example but useful to get used too
while True:
    dt = clock.tick(60) / 1000
    # In this for loop is crazy! because its always listening which event is triggering
    for event in pygame.event.get():
        # And once is equal when a user closes the window
        # it will close the current window in execution 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if is_input_left_active(event, screen):
            dude_acc_x -= ACCELERATION

        if is_input_right_active(event, screen):
            dude_acc_x += ACCELERATION
            
        if event.type == pygame.KEYUP or is_button_up(event):
            dude_acc_x = 0
            dude_vel_x = 0

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the dude image
    screen.blit(dude, (dude_x, dude_y))

    dude_vel_x += dude_acc_x * dt
    dude_x += dude_vel_x

    if dude_vel_x >= MAX_SPEED:
        dude_x += MAX_SPEED
    
    # detect bounds and limiting the dude in the screen
    if(dude_y + dude.get_rect().height <= 500):
        dude_y += GRAVITY * dt

    if(dude_x <= 0):
        dude_x = 0

    if(dude_x + dude.get_rect().width >= screen.get_width()):
        dude_x = screen.get_width() - dude.get_rect().width

    # floor edge
    screen.blit(floor_surface, (0, 500))

    # floor bg
    floor_bg_rect = pygame.Rect(0, 505, screen.get_width(), 100)
    pygame.draw.rect(screen, FLOOR_COLOR, floor_bg_rect)

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 100))
    screen.blit(text_surface, text_rect)

    # Debugging
    # Velocity
    text_content = f"Velocity: {int( dude_vel_x )}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 130))
    screen.blit(text_surface, text_rect)
    # Acceleration
    text_content = f"Acceleration: {int( dude_acc_x )}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 160))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS