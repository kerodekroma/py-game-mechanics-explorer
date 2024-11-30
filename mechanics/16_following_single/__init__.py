# how to execute it in cmd:
# python -m mechanics.16_following_single

import pygame
import math
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
SPEED = 7
MIN_DISTANCE = 50

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > following single")

# clock
clock = pygame.time.Clock()

# dude imgs reference
dude = pygame.image.load('./assets/img/orangito32x32.png').convert_alpha()
dude_x = WINDOW_WIDTH / 2
dude_y = WINDOW_HEIGHT / 2

def check_distance(pos_a, pos_b):
    return math.sqrt((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2)

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

    # rotation
    mouse_pos = pygame.mouse.get_pos()
    dude_rect = dude.get_rect()

    center_x = dude_x + dude_rect.width / 2 
    center_y = dude_y + dude_rect.height / 2 

    if check_distance(mouse_pos, [center_x, center_y]) > MIN_DISTANCE:
        vx = (mouse_pos[0] - center_x) * SPEED
        vy = (mouse_pos[1] - center_y) * SPEED

    if not check_distance(mouse_pos, [center_x, center_y]) > MIN_DISTANCE:
        vx = 0
        vy = 0

    dude_x += vx * dt
    dude_y += vy * dt

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the dude image
    screen.blit(dude, (dude_x, dude_y))

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