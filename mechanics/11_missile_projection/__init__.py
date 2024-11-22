# how to execute it in cmd:
# python -m mechanics.10_missile_artillery

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

# 
SHOT_DELAY = 300
MISSILE_SPEED = 900
GRAVITY = 1000

is_pressing_button_down = False

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > missile projection")

# clock
clock = pygame.time.Clock()

# missile img reference
missile_img = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()

# setup initial missile position
missile_init_x = 100
missile_init_y = screen.get_height() - 100
missile_angle = math.radians(90)

# setup multiple missile
missiles = []
missile_shot_time = 0

# setup projection
trajectory_points = []

def render_trajectory(screen, x, y, angle):
    trajectory_points = []
    time_simulation = 3000

    for t in range(0, time_simulation, 50):
        t /= 1000
        dist_x = math.cos(angle) * MISSILE_SPEED * t
        dist_y = math.sin(angle) * MISSILE_SPEED * t - 0.5 * GRAVITY * t ** 2
        pos_x = x + dist_x
        pos_y = y - dist_y
        if pos_y >= WINDOW_HEIGHT - 32:
            break
        trajectory_points.append((pos_x, pos_y))

    # render the projection points
    for projection_point in trajectory_points:
        pygame.draw.circle(screen, palette[4], (int(projection_point[0]), int(projection_point[1])), 3)

def create_missile(pos, angle):
    vel_x = math.cos(angle) * MISSILE_SPEED
    vel_y = math.sin(angle) * MISSILE_SPEED
    return {'x': pos[0], 'y': pos[1], 'angle': angle, 'vel_x': vel_x, 'vel_y': vel_y}

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

        # rotation
        mouse_pos = pygame.mouse.get_pos()
        missile_angle = math.atan2(
            mouse_pos[1] - missile_init_y,
            mouse_pos[0] - missile_init_x 
        )

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # printing the missile ref image
    rotated_missile_img = pygame.transform.rotate(missile_img, -math.degrees( missile_angle ))
    missile_rect = rotated_missile_img.get_rect(center=(missile_init_x, missile_init_y))
    screen.blit(rotated_missile_img, missile_rect.topleft)

    if is_pressing_button_down and current_time - missile_shot_time > SHOT_DELAY:
        missile_shot_time = current_time # update last shot time
        missiles.append(create_missile((missile_init_x,  missile_init_y), missile_angle))

    # render the list of missiles 
    for missile in missiles[:]:
        # applying the proper direction as well
        # missile['x'] += math.cos(missile['angle']) * MISSILE_SPEED * dt
        #if missile['vel_y'] == 0:
        #    missile['vel_y'] += math.sin(missile['angle']) * MISSILE_SPEED * dt
        #    rotation_angle = missile['angle']
        missile['vel_y'] += GRAVITY * dt

        missile['x'] += missile['vel_x'] * dt
        missile['y'] += missile['vel_y'] * dt

        rotation_angle = math.atan2(missile['vel_y'], missile['vel_x'])

        # applying the current angle too
        rotated_missile = pygame.transform.rotate(missile_img, -math.degrees(rotation_angle))
        missile_rect = rotated_missile.get_rect(center=(missile['x'], missile['y']))
        screen.blit(rotated_missile, missile_rect.topleft)

        # left to right bounds
        if missile['x'] - rotated_missile.get_rect().width > screen.get_width() or missile['x'] + rotated_missile.get_rect().width < 0:
            if missile in missiles:
                missiles.remove(missile)

        # top to bottom bounds
        if missile['y'] - rotated_missile.get_rect().height > screen.get_height() or missile['y'] + rotated_missile.get_rect().height < 0:
            if missile in missiles:
                missiles.remove(missile)

    render_trajectory(screen, missile_init_x, missile_init_y, -missile_angle)

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

    # missile angle
    text_content = f"Missile angle: {missile_angle}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 180))
    screen.blit(text_surface, text_rect)

    # number of missiles
    text_content = f"Missiles : {len(missiles)}, is pressing a key/mouse: {is_pressing_button_down}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(50, 210))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS