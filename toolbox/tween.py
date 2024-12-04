import math

class Tween:
    def __init__(self, surface, steps, durations, loop_mode=True):
        self.surface = surface
        self.steps = steps
        self.durations = durations
        self.loop_mode = loop_mode

        self.current_step = 0
        self.elapsed_time = 0
        self.total_time = sum(durations)

        self.rect = self.surface.get_rect(topleft=steps[0])

    def get_rect(self):
        return self.rect

    def sinusoidal_in_out(self, t):
        """ Easing function: Sinusoidal In/Out """
        return -0.5 * (math.cos(math.pi * t) - 1)

    def interpolation_easing(self, start, end, time):
        """ Linear inteporlation with easing"""
        return start + (end - start) * self.sinusoidal_in_out(time)

    def update(self, dt):
        """ Updating the animation state """
        self.elapsed_time += dt
        while self.elapsed_time > self.durations[self.current_step]:
            self.elapsed_time -= self.durations[self.current_step]
            self.current_step = (self.current_step + 1) % len(self.steps)
            if not self.loop_mode and self.current_step == 0:
                return
        t = self.elapsed_time / self.durations[self.current_step]
        start_step = self.steps[self.current_step]
        end_step = self.steps[(self.current_step + 1) % len(self.steps)]
        self.rect.x = self.interpolation_easing(start_step[0], end_step[0], t)
        self.rect.y = self.interpolation_easing(start_step[1], end_step[1], t)

    def render(self, screen):
        """ Render the tweened surface """
        screen.blit(self.surface, self.rect)