import pygame
import random
from main_flame import Flame
from main_flame import FlameParticle

BLUE_SQUARE_RESPAWN_EVENT = pygame.USEREVENT + 1

class BlueSquare(pygame.sprite.Sprite):
    def __init__(self, x, y, size=50):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 0, 255))  # Blue color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def follow_sprite(self, sprite):
        self.rect.topleft = sprite.rect.topleft

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

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, width, height)

def create_window():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('GameJam de la mort')

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (1280, 720))
    
    flame =  Flame(50, 50)
    
    platforms = [Platform(0, 540, 1200, 200)]
    
    sprite_images = ['assets/hero/00_hero.png', 'assets/hero/01_hero.png',
                     'assets/hero/02_hero.png', 'assets/hero/03_hero.png',
                     'assets/hero/04_hero.png', 'assets/hero/05_hero.png',
                     'assets/hero/06_hero.png', 'assets/hero/07_hero.png']
    animated_sprite = AnimatedSprite(sprite_images, 100, 100)

    fire_images = ['assets/fire/00_fire.png','assets/fire/01_fire.png','assets/fire/02_fire.png',
                     'assets/fire/03_fire.png','assets/fire/04_fire.png','assets/fire/05_fire.png',
                     'assets/fire/06_fire.png','assets/fire/07_fire.png','assets/fire/08_fire.png',
                     'assets/fire/09_fire.png','assets/fire/10_fire.png','assets/fire/11_fire.png',
                     'assets/fire/12_fire.png','assets/fire/13_fire.png','assets/fire/14_fire.png',
                     'assets/fire/15_fire.png','assets/fire/16_fire.png','assets/fire/17_fire.png',
                     'assets/fire/18_fire.png','assets/fire/19_fire.png']
    animated_fire = AnimatedSprite(fire_images, 100, 100)

    platform_x = 0
    platform_y = 540
    platform_width = 1200

    blue_squares = [BlueSquare(random.randint(platform_x, platform_x + platform_width), platform_y - 90) for _ in range(5)]

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == BLUE_SQUARE_RESPAWN_EVENT:
                new_square = BlueSquare(random.randint(platform_x, platform_x + platform_width), platform_y - 90)
                blue_squares.append(new_square)
                pygame.time.set_timer(BLUE_SQUARE_RESPAWN_EVENT, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            animated_sprite.move('left')
        if keys[pygame.K_d]:
            animated_sprite.move('right')
        if keys[pygame.K_SPACE]:
            animated_sprite.jump()

        for platform in platforms:
            if animated_sprite.rect.colliderect(platform.rect):
                animated_sprite.fall_speed = 0
                animated_sprite.rect.y = platform.rect.y - animated_sprite.rect.height

        window.blit(background, (0, -40))
        for platform in platforms:
            window.blit(platform.image, platform.rect)
            
        animated_sprite.update(blue_squares)
        window.blit(animated_sprite.image, animated_sprite.rect)
        flame.draw_flame(window)
        
        for square in blue_squares:
            animated_fire.update(blue_squares)
            window.blit(animated_fire.image, square.rect)

        animated_sprite.update(blue_squares)
        if pygame.sprite.collide_rect(animated_sprite, flame):
            for square in animated_sprite.blue_squares:
                flame.add_square(square)
                animated_sprite.blue_squares.remove(square)
        
        flame.health -= 0.2
        pygame.display.flip()
        if flame.health <= 0:
            print('Game Over')
            pygame.quit()
            break
    pygame.quit()
create_window()
