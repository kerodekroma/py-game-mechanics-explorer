# how to execute it in cmd:
# python -m mechanics.08_missile_consecutive

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
SHOT_DELAY = 300
MISSILE_SPEED = 500

is_pressing_button_down = False

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > missile consecutive")

# clock
clock = pygame.time.Clock()

# missile img reference
missile_img = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()

# setup initial missile position
missile_init_x = 100
missile_init_y = screen.get_height() / 2

# setup multiple missile
missiles = []
missile_shot_time = 0

def create_missile(pos):
    return {'x': pos[0], 'y': pos[1], 'vel_x': MISSILE_SPEED}

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
            is_pressing_button_down = True

        if is_button_up(event) or event.type == pygame.KEYUP:
            is_pressing_button_down = False

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the missile ref image
    screen.blit(missile_img, (missile_init_x, missile_init_y))

    if is_pressing_button_down and current_time - missile_shot_time > SHOT_DELAY:
        missile_vel_x = MISSILE_SPEED 
        missile_shot_time = current_time # update last shot time
        missiles.append(create_missile((missile_init_x,  missile_init_y)))

    # render the list of missiles 
    for missile in missiles[:]:
        missile['x'] += missile['vel_x'] * dt
        screen.blit(missile_img, (missile['x'], missile['y']))

        if missile['x'] - missile_img.get_rect().width > screen.get_width():
            missiles.remove(missile)

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
    text_rect = text_surface.get_rect(topleft=(50, 150))
    screen.blit(text_surface, text_rect)

    # number of missiles
    text_content = f"Missiles : {len(missiles)}, is pressing a key/mouse: {is_pressing_button_down}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 180))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS