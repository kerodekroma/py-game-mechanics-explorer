# how to execute it in cmd:
# python -m mechanics.23_homing_missile_explosion

import pygame
import math
import sys
import random
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
MAX_MISSILES = 3

# The screen is almost ready, this is just the definition
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Adding our awesone caption to show in the top of our fresh screen
pygame.display.set_caption("mechanics > homing missile smoke trails")

# clock
clock = pygame.time.Clock()

# setup missile
init_missile_x = 100
init_missile_y = screen.get_height() / 2
missiles = []

class Missile:

    AVOID_DISTANCE = 50 # Distance to trigger avoidance

    def __init__(self, x=100, y=100, wobble=WOBBLE_LIMIT):
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.angle = 0
        self.wobble = wobble
        self.explodes = False
        self.smoke_emitter_instance = smoke_emitter.SmokeEmitter((x, y))
        self.wobble_timer = 0
        self.wobble_direction = -1
        self.particles = []
        self.img = pygame.image.load('./assets/img/missile28x20.png').convert_alpha()
        self.missile_img_rotated = None
        self.missile_rect_rotated = None

    def get_distance(self, point_1, point_2):
        return math.sqrt((point_1[0] - point_2[0]) ** 2  + (point_1[1] - point_2[1]) ** 2)

    def avoid(self, siblings):
        avoid_angle = 0
        for m in siblings:
            if self == m: #skip itself
                continue

            # Calculate distance
            distance = self.get_distance(m)

            # If too close, set an avoidance angle
            if distance < self.AVOID_DISTANCE:
                avoid_angle = math.pi / 2  # Default to 90 degrees
                if random.random() > 0.5: # 50% chance to zig or zag
                    avoid_angle *= 1
                
                

    def prepare_explosion(self, x, y):
        # Create a fountain effect at mouse position
        for _ in range(30):  # Number of particles
            self.particles.append(particle_lib.Particle(x, y, palette))

    def update(self, mouse_pos):
        # calculating the angle to the target position
        target_angle = math.atan2(
            mouse_pos[1] - self.y,
            mouse_pos[0] - self.x,
        )
        target_angle_degrees = math.degrees(target_angle)

        # Adding the wobble effect
        self.wobble_timer += WOBBLE_SPEED * dt
        if self.wobble_timer >= 1:
            self.wobble_timer -= 1
            self.wobble_direction *= -1 

        wobble_effect = self.wobble_direction * (
            WOBBLE_LIMIT * math.sin(WOBBLE_SPEED * self.wobble_timer)
        )
        target_angle_degrees += wobble_effect

        # adjust the angle gradually towards the target
        delta_angle = target_angle_degrees - self.angle
        # normalize to the range in degress [-180, 180]
        delta_angle = (delta_angle + 180) % 360 - 180
        if abs(delta_angle) < TURN_RATE:
            self.angle = target_angle_degrees
        if delta_angle > 0:
            self.angle += TURN_RATE
        if delta_angle < 0:
            self.angle -= TURN_RATE

        # Update rotation
        self.missile_img_rotated = pygame.transform.rotate(self.img, -self.angle)
        self.missile_rect_rotated = self.missile_img_rotated.get_rect(center=(self.x, self.y))

        # calculate velocity based on current angle
        rad_angle = math.radians(self.angle)
        self.vel_x = math.cos(rad_angle) * MISSILE_SPEED * dt
        self.vel_y = math.sin(rad_angle) * MISSILE_SPEED * dt

        # update position
        self.x += self.vel_x
        self.y += self.vel_y

        # check distance between mouse and explodes when the missile is closer to the cursor
        distance = self.get_distance([self.x, self.y], mouse_pos)
        if distance < 50:
            self.prepare_explosion(self.x, self.y)
            self.x = self.init_x
            self.y = self.init_y
            self.explodes = True

        # printing first the smoke trails
        offset_x = self.x - math.cos(rad_angle) * 30
        offset_y = self.y - math.sin(rad_angle) * 30
        self.smoke_emitter_instance.x = offset_x
        self.smoke_emitter_instance.y = offset_y
        self.smoke_emitter_instance.update()

    def render(self, screen):
        self.smoke_emitter_instance.render(screen)

        if self.explodes:
            # Update and draw particles
            for particle in self.particles[:]:
                particle.update(WINDOW_WIDTH, WINDOW_HEIGHT)
                particle.draw(screen)
                if particle.lifetime <= 0 or particle.size <= 0.1:
                    self.particles.remove(particle)
        
            if len(self.particles) == 0:
                self.explodes = False

        # printing the missile image
        screen.blit(self.missile_img_rotated, self.missile_rect_rotated.topleft)

for i in range(0, MAX_MISSILES):
    rand_x = random.randint(0, 50)
    rand_y = random.randint(0, 50)
    missiles.append(Missile(rand_x, rand_y))

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

    for missile in missiles[:]:
        missile.update(mouse_pos)
        missile.render(screen)

    # FPS
    fps = clock.get_fps()
    text_content = f"FPS: {int(fps)}"
    text_surface = pixel_font.render(text_content, True, palette[2])
    text_rect = text_surface.get_rect(topleft=(100, 100))
    screen.blit(text_surface, text_rect)

	# This method refreshes all the screen, is part of a good practice keep it here
    pygame.display.flip()

    #clock
    clock.tick(60) # Limit to 60 FPS