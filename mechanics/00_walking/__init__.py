# how to execute it in cmd:
# python -m mechanics.00_walking 

import pygame

import sys

from toolbox import colors

# Initializing Pygame
pygame.init()

# Defining the dimentions for our screen
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

palette = colors.PALETTE

# Defining a color to print in all the screen
BG_COLOR = palette[0]

FLOOR_COLOR = palette[13]

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > walking")

# clock
clock = pygame.time.Clock()

# setup
dude = pygame.image.load('./assets/img/orangito32x32.png').convert_alpha()


tile_floor = pygame.image.load('./assets/img/bg_one.png').convert_alpha()
tile_floor_width, tile_floor_height = tile_floor.get_size()
floor_surface = pygame.Surface((screen.get_width(), tile_floor_height ), pygame.SRCALPHA)

for x in range(0, screen.get_width(), tile_floor_width):
    floor_surface.blit(tile_floor, (x, 0))

# Flag to run our loop, it's optional in this example but useful to get used too
while True:
    # In this for loop is crazy! because its always listening which event is triggering
    for event in pygame.event.get():
        # And once is equal when a user closes the window
        # it will close the current window in execution 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dt = clock.tick(60) / 1000
	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the dude image
    screen.blit(dude, (100, 100))

    # floor edge
    screen.blit(floor_surface, (0, 500))

    # floor bg
    floor_bg_rect = pygame.Rect(0, 505, screen.get_width(), 100)
    pygame.draw.rect(screen, FLOOR_COLOR, floor_bg_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    pygame.time.Clock().tick(60)