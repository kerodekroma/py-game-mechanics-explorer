# how to execute it in cmd:
# python -m mechanics.19_following_groups

import pygame
import math
import sys
from toolbox import colors, font, tween

from collections import deque

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
SPEED = 300
MIN_DISTANCE = 25

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > following groups")

# clock
clock = pygame.time.Clock()

# setup flag
flag_img = pygame.image.load('./assets/img/flag32x32.png').convert_alpha()
# tween params
flag_steps = [
    (WINDOW_WIDTH - 50, 50),
    (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50),
    (50, WINDOW_HEIGHT - 50),
    (50, 50)
]
flag_durations = [
    2000, 1200, 2000, 1200
]
flag_tween = tween.Tween(flag_img, flag_steps, flag_durations, True)

# dude class reference
class Dude():
    def __init__(self, x= WINDOW_WIDTH / 2, y= WINDOW_HEIGHT / 2):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.img = pygame.image.load('./assets/img/orangito32x32.png').convert_alpha()
        # it will memorize the steps of the next dudes and the max length
        # self.memory_max_length = 3
        # self.memory = []

        # in this mode is more optimized
        self.memory = deque(maxlen=3)
        self.target_is_moving = False

    def render(self, screen, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        screen.blit(self.img, (self.x, self.y))

dude1 = Dude()
dude2 = Dude()
dude3 = Dude()

# dude followers to the flag
dude_flag_1 = Dude()
dude_flag_2 = Dude()
dude_flag_3 = Dude()

def check_distance(pos_a, pos_b):
    return math.sqrt((pos_a[0] - pos_b[0]) ** 2 + (pos_a[1] - pos_b[1]) ** 2)

def angle_between(pos_a, pos_b):
    return math.atan2(pos_b[1] - pos_a[1], pos_b[0] - pos_a[0])

def move(dude, dude_target):
    dude_rect = dude.img.get_rect()

    # calculating the center position of the dude
    center_x = dude.x + dude_rect.width / 2 
    center_y = dude.y + dude_rect.height / 2 

    if dude_target:
        if isinstance(dude_target, Dude) and dude_target.memory:
            target_x, target_y = dude_target.memory[0]
        if not isinstance(dude_target, Dude):
            target_x, target_y = dude_target[0], dude_target[1]
        
        # Calculate distance to target
        dist = check_distance(( dude.x, dude.y ), ( target_x, target_y ))
        if dist > MIN_DISTANCE:
            # Move towards the target
            angle = angle_between(( dude.x, dude.y ), ( target_x, target_y ))
            dude.vx = math.cos(angle) * SPEED
            dude.vy = math.sin(angle) * SPEED

        if not dist > MIN_DISTANCE:
            dude.vx = 0
            dude.vy = 0

    dude.memory.append((dude.x, dude.y))

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

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    move(dude1, (mouse_pos[0], mouse_pos[1]))
    move(dude2, dude1)
    move(dude3, dude2)


    # printing the dudes image
    dude1.render(screen, dt)
    dude2.render(screen, dt)
    dude3.render(screen, dt)

    # printing the flag and its dude followers
    delta_time = clock.get_time()
    flag_tween.update(delta_time)
    flag_tween.render(screen)

    flag_rect = flag_tween.get_rect()
    move(dude_flag_1, (flag_rect.x, flag_rect.y))
    move(dude_flag_2, dude_flag_1)
    move(dude_flag_3, dude_flag_2)

    # printing the dudes image
    dude_flag_1.render(screen, dt)
    dude_flag_2.render(screen, dt)
    dude_flag_3.render(screen, dt)

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(center=(100, 100))
    screen.blit(text_surface, text_rect)

    # Debugging mouse position
    text_content = f"mouse_pos[0] aka mouse X: { mouse_pos[0] }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 130))
    screen.blit(text_surface, text_rect)

    text_content = f"mouse_pos[1] aka mouse Y: { mouse_pos[1] }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 160))
    screen.blit(text_surface, text_rect)

    # Debugging dude 1

    text_content = f"| dude 1"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 220))
    screen.blit(text_surface, text_rect)

    text_content = f"- x: { int(dude1.x) }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 260))
    screen.blit(text_surface, text_rect)

    text_content = f"- y: { int(dude1.y) }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 300))
    screen.blit(text_surface, text_rect)

    text_content = f"- target_is_moving: { dude1.target_is_moving }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 340))
    screen.blit(text_surface, text_rect)

    text_content = f"- memory: { len(dude1.memory) }"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 380))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS