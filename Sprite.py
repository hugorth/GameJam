import pygame
import random
from main_flame import Flame
from main_flame import FlameParticle

BLUE_SQUARE_RESPAWN_EVENT = pygame.USEREVENT + 1

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = [pygame.image.load(img) for img in images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.counter = 0
        self.delay = 10
        self.speed = 5
        self.jumping = False
        self.jump_height = 10
        self.gravity = 1
        self.fall_speed = 0
        self.max_fall_speed = 15
        self.start_x = x
        self.start_y = y
        self.blue_squares = []
        self.carried_squares = []

    def reset(self):
        self.index = 0
        self.image = self.images[self.index]
        self.rect.topleft = (self.start_x, self.start_y)
        self.counter = 0
        self.jumping = False
        self.jump_height = 10
        self.fall_speed = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True

    def update(self, blue_squares):
        self.counter += 1
        if self.counter >= self.delay:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.counter = 0
        if self.jumping:
            self.rect.y -= self.jump_height
            self.jump_height -= self.gravity
            if self.jump_height < -10:
                self.jumping = False
                self.jump_height = 15
        if not self.jumping:
            self.fall_speed = min(self.fall_speed + self.gravity, self.max_fall_speed)
            self.rect.y += self.fall_speed
        if self.rect.y > 550:
            self.reset()
        for square in blue_squares:  # Assuming blue_squares is a list of BlueSquare instances
            if self.rect.colliderect(square.rect):
                square.follow_sprite(self)
        for square in blue_squares:
            if self.rect.colliderect(square.rect):
                square.follow_sprite(self)
                self.blue_squares.append(square)  # Ajoutez le carré bleu à la liste des carrés ramassés
                blue_squares.remove(square)
                pygame.time.set_timer(BLUE_SQUARE_RESPAWN_EVENT, 300)

    def move(self, direction):
        if direction == 'right':
            self.rect.x += self.speed
        elif direction == 'left':
            self.rect.x -= self.speed