import random
import pygame

class SmokeParticle:
    def __init__(self, pos, lifetime=60, max_radius=6):
        self.x, self.y = pos
        self.lifetime = lifetime # Lifetime in frames
        self.age = 0 
        # self.radius = random.randint(2, max_radius)
        self.radius = max_radius
        self.alpha = 255
        self.start_time = pygame.time.get_ticks()
        self.size = random.randint(2, 6)
        self.velocity = [random.uniform(-1, 1), random.uniform(-2, -1)]

    def update(self):
        """Update the smoke particle's state"""
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.lifetime:
            return False #Indicates the particle should be removed

        # Gradually fade out decreasing alpha
        alpha = max(0, 255 - int((elapsed_time / self.lifetime) * 255))
        self.color = (255, 255, 255, alpha)
        return True

    def render(self, screen):
        """Draw the smoke particle as a fading circle."""
        # Create a surface for transparency
        smoke_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(smoke_surface, self.color, (self.radius, self.radius), self.radius)

        # Blit the smoke surface to the main screen
        screen.blit(smoke_surface, (self.x - self.radius, self.y - self.radius))
            
