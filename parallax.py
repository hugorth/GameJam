import pygame

class ParallaxLayer:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (800, 600))
        self.x = 0
        self.speed = speed

    def set_speed(self, speed):
        self.speed = speed

    def update(self, direction):
        self.x += self.speed * direction
        if self.x <= -self.image.get_width():
            self.x = 0
        elif self.x >= self.image.get_width():
            self.x = 0

    def draw(self, window):
        window.blit(self.image, (self.x, 0))
        if self.x < self.image.get_width():
            window.blit(self.image, (self.x + self.image.get_width(), 0))
        if self.x > 0:
            window.blit(self.image, (self.x - self.image.get_width(), 0))