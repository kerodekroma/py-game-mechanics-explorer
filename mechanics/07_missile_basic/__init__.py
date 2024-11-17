# how to execute it in cmd:
# python -m mechanics.07_missile_basic

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
SHOT_DELAY = 500
MISSILE_SPEED = 1200

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > missile basic")

# clock
clock = pygame.time.Clock()

# setup missile
missile_static = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()
missile_static_x = 100
missile_static_y = screen.get_height() / 2

missile = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()
missile_x = 100
missile_y = screen.get_height() / 2
missile_vel_x = 0
missile_shot_time = 0

# adding the defs to check if the input is to the left/right
def is_button_down(event):
    return event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN

def is_button_up(event):
    return event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP

def is_input_tap_active(event):
    if is_button_down(event):
        return True 
    return event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE

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

        if is_input_tap_active(event):
            if current_time - missile_shot_time > SHOT_DELAY:
                missile_vel_x = MISSILE_SPEED 
                missile_shot_time = current_time # update last shot time

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    missile_x += missile_vel_x * dt

    if(missile_x - missile.get_rect().width > screen.get_width()):
        missile_x = missile_static_x
        missile_y = missile_static_y
        missile_vel_x = 0
        missile_shot_time = 0

    # printing the missile image
    screen.blit(missile, (missile_x, missile_y))

    # printing the missile ref image
    screen.blit(missile_static, (missile_static_x, missile_static_y))

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 100))
    screen.blit(text_surface, text_rect)

    # next shot in ...
    time_since_last_shot = current_time - missile_shot_time
    time_until_next_shot = max(0, SHOT_DELAY - time_since_last_shot)
    text_content = f"Next shot in: {time_until_next_shot // 1000}.{time_until_next_shot % 1000:03d} s"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 250))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS