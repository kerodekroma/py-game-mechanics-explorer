# how to execute it in cmd:
# python -m mechanics.23_homing_missile_explosion

import pygame
import math
import sys
from toolbox import colors, font, smoke_emitter, particle as particle_lib

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
MISSILE_SPEED = 350 # pixels per second
WOBBLE_SPEED = 2 * math.pi # radians per second (frequency of wobble)
WOBBLE_LIMIT = -35 # degrees
WOBBLE_MAGNITUDE = 10 # degrees (amplitude of wobble)
TURN_RATE = 3 # degrees per seconf

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > homing missile smoke trails")

# clock
clock = pygame.time.Clock()

# setup missile
missile = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()
init_missile_x = 100
init_missile_y = screen.get_height() / 2
missile_x = init_missile_x
missile_y = init_missile_y
missile_vel_x = 0
missile_vel_y = 0
missile_shot_time = 0
missile_angle = 0
missile_wobble = WOBBLE_LIMIT
missile_explodes = False

wobble_timer = 0
wobble_direction = -1
particles = []

smoke_emitter_instance = smoke_emitter.SmokeEmitter((missile_x, missile_y))

def get_distance(point_1, point_2):
    return math.sqrt((point_1[0] - point_2[0]) ** 2  + (point_1[1] - point_2[1]) ** 2)

def prepare_explosion(x, y):
    # Create a fountain effect at mouse position
    for _ in range(30):  # Number of particles
        particles.append(particle_lib.Particle(x, y, palette))

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

	# This is the magic sentence where our screen finally renders our DEMO_BG_COLOR, yay!
    screen.fill(BG_COLOR)

    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # calculating the angle to the target position
    target_angle = math.atan2(
        mouse_pos[1] - missile_y,
        mouse_pos[0] - missile_x,
    )
    target_angle_degrees = math.degrees(target_angle)

    # Adding the wobble effect
    wobble_timer += WOBBLE_SPEED * dt
    if wobble_timer >= 1:
        wobble_timer -= 1
        wobble_direction *= -1 

    wobble_effect = wobble_direction * (
        WOBBLE_LIMIT * math.sin(WOBBLE_SPEED * wobble_timer)
    )
    target_angle_degrees += wobble_effect

    # adjust the angle gradually towards the target
    delta_angle = target_angle_degrees - missile_angle
    # normalize to the range in degress [-180, 180]
    delta_angle = (delta_angle + 180) % 360 - 180
    if abs(delta_angle) < TURN_RATE:
        missile_angle = target_angle_degrees
    if delta_angle > 0:
        missile_angle += TURN_RATE
    if delta_angle < 0:
        missile_angle -= TURN_RATE

    # Update rotation
    missile_img_rotated = pygame.transform.rotate(missile, -missile_angle)
    missile_rect_rotated = missile_img_rotated.get_rect(center=(missile_x, missile_y))

    # calculate velocity based on current angle
    rad_angle = math.radians(missile_angle)
    missile_vel_x = math.cos(rad_angle) * MISSILE_SPEED * dt
    missile_vel_y = math.sin(rad_angle) * MISSILE_SPEED * dt

    # update position
    missile_x += missile_vel_x
    missile_y += missile_vel_y

    # check distance between mouse and explodes when the missile is closer to the cursor
    distance = get_distance([missile_x, missile_y], mouse_pos)
    if distance < 50:
        prepare_explosion(missile_x, missile_y)
        missile_x = init_missile_x
        missile_y = init_missile_y
        missile_explodes = True

    if missile_explodes:
        # Update and draw particles
        for particle in particles[:]:
            particle.update(WINDOW_WIDTH, WINDOW_HEIGHT)
            particle.draw(screen)
            if particle.lifetime <= 0 or particle.size <= 0.1:
                particles.remove(particle)
        
        if len(particles) == 0:
            missile_explodes = False


    # printing first the smoke trails
    offset_x = missile_x - math.cos(rad_angle) * 30
    offset_y = missile_y - math.sin(rad_angle) * 30
    smoke_emitter_instance.x = offset_x
    smoke_emitter_instance.y = offset_y
    smoke_emitter_instance.update()
    smoke_emitter_instance.render(screen)

    # printing the missile image
    screen.blit(missile_img_rotated, missile_rect_rotated.topleft)

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(100, 100))
    screen.blit(text_surface, text_rect)

    # distance
    fps = clock.get_fps()
    text_content = f"Distance between missile and mouse: {int(distance)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(100, 150))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS