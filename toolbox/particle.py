import random
import pygame

# Gravity
GRAVITY = 0.2

# Particle class
class Particle:
    def __init__(self, x, y, colors = []):
        self.x = x
        self.y = y
        self.size = random.uniform(10, 20)  # Random initial size
        self.color = random.choice(colors)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-5, -3)  # Upward velocity
        self.lifetime = random.randint(60, 120)  # Frames to live
        self.bound_cooldown = 0  # Time to persist after hitting a boundary

    def update(self, width, height):
        if self.bound_cooldown > 0:
            self.bound_cooldown -= 1
            return  # Stop movement if in cooldown

        # Apply gravity
        self.speed_y += GRAVITY

        # Update position
        self.x += self.speed_x
        self.y += self.speed_y

        # Shrink over time
        self.size *= 0.97
        self.lifetime -= 1

        # Boundary collision check
        if self.x <= 0 or self.x >= width:  # Horizontal bounds
            self.speed_x *= -0.9  # Reflect and reduce speed
            self.speed_y *= 0.1
            self.bound_cooldown = 3  # Persist briefly
        if self.y >= height:  # Bottom bound
            self.speed_y = -self.speed_y * 0.7  # Reflect and reduce speed
            self.bound_cooldown = 15
        if self.y <= 0:  # Top bound
            self.speed_y = 0.5  # Slight bounce downwards

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))