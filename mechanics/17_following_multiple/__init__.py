# how to execute it in cmd:
# python -m mechanics.17_following_multiple

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
pygame.display.set_caption("mechanics > following multiple")

# clock
clock = pygame.time.Clock()

# dude class reference
class Dude():
    def __init__(self, x= WINDOW_WIDTH / 2, y= WINDOW_HEIGHT / 2):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.img = pygame.image.load('./assets/img/orangito32x32.png').convert_alpha()

    def render(self, screen, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        screen.blit(self.img, (self.x, self.y))

dude = Dude()
dude2 = Dude()
dude3 = Dude()

def check_distance(pos_a, pos_b):
    return math.sqrt((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2)

def move(dude, target_x, target_y):
    dude_rect = dude.img.get_rect()

    center_x = dude.x + dude_rect.width / 2 
    center_y = dude.y + dude_rect.height / 2 

    if check_distance([ target_x, target_y] , [center_x, center_y]) > MIN_DISTANCE:
        dude.vx = (target_x - dude.x) * SPEED
        dude.vy = (target_y - dude.y) * SPEED

    if not check_distance([ target_x, target_y], [center_x, center_y]) > MIN_DISTANCE:
        dude.vx = 0
        dude.vy = 0

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

    mouse_pos = pygame.mouse.get_pos()


    move(dude, mouse_pos[0], mouse_pos[1])
    move(dude2, dude.x, dude.y)
    move(dude3, dude2.x, dude2.y)

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the dudes image
    dude.render(screen, dt)
    dude2.render(screen, dt)
    dude3.render(screen, dt)

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