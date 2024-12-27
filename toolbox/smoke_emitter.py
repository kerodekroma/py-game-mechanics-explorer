from toolbox import smoke_particle
import pygame

class SmokeEmitter:
    def __init__(self, pos, max_particles=100, interval=50, lifetime=1000):
        self.x, self.y = pos
        self.max_particles = max_particles
        self.interval = interval # Emission interval in milliseconds
        self.lifetime = lifetime # Emission lifetime in milliseconds
        self.particles = []
        self.time_since_last_emit = 0

    def emit(self):
        """Emit particles at regular intervals."""
        current_time = pygame.time.get_ticks() 
        if current_time - self.time_since_last_emit >= self.interval:
            if len(self.particles) < self.max_particles:
                self.particles.append(smoke_particle.SmokeParticle((self.x, self.y), self.lifetime))
            self.time_since_last_emit = current_time # Resets the event emitter
        
    def update(self):
        """Update all particles and remove expired ones"""
        self.emit()
        self.particles = [p for p in self.particles if p.update()]
    
    def render(self, screen):
        """Draw all active particles"""
        for particle in self.particles:
            particle.render(screen)

