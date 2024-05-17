import pygame
import random

BLUE_SQUARE_RESPAWN_EVENT = pygame.USEREVENT + 1

class FlameParticle:
    alpha_layer_qty = 2
    alpha_glow_difference_constant = 2

    def __init__(self, x=1280 // 2, y=720 // 2, r=5):
        self.x = x
        self.y = y
        self.r = r
        self.original_r = r
        self.alpha_layers = FlameParticle.alpha_layer_qty
        self.alpha_glow = FlameParticle.alpha_glow_difference_constant
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        self.burn_rate = 0.1 * random.randint(1, 4)

    def update(self):
        self.y -= 7 - self.r
        self.x += random.randint(-self.r, self.r)
        self.original_r -= self.burn_rate
        self.r = int(self.original_r)
        if self.r <= 0:
            self.r = 1

    def draw(self, screen):
        max_surf_size = 2 * self.r * self.alpha_layers * self.alpha_layers * self.alpha_glow
        self.surf = pygame.Surface((max_surf_size, max_surf_size), pygame.SRCALPHA)
        for i in range(self.alpha_layers, -1, -1):
            alpha = 255 - i * (255 // self.alpha_layers - 5)
            if alpha <= 0:
                alpha = 0
            radius = self.r * i * i * self.alpha_glow
            if self.r == 4 or self.r == 3:
                r, g, b = (255, 0, 0)
            elif self.r == 2:
                r, g, b = (255, 150, 0)
            else:
                r, g, b = (50, 50, 50)
            #r, g, b = (0, 0, 255)  # uncomment this to make the flame blue
            color = (r, g, b, alpha)
            pygame.draw.circle(self.surf, color, (self.surf.get_width() // 2, self.surf.get_height() // 2), radius)
        screen.blit(self.surf, self.surf.get_rect(center=(self.x, self.y)))


class Flame:
    def __init__(self, width, height, x=1280 - 100, y=720 - 200):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 0, 0))  # Remplir la surface de rouge
        self.rect = self.image.get_rect()  # Ajoutez cette ligne
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.flame_intensity = 10
        self.flame_particles = []
        self.squares = []
        self.health = 100

        for i in range(self.flame_intensity * 40):
            self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 10)))

    def draw_flame(self, screen):
        for i in self.flame_particles:
            if i.original_r <= 0:
                self.flame_particles.remove(i)
                self.flame_particles.append(FlameParticle(self.x + random.randint(-5, 5), self.y, random.randint(1, 5)))
                del i
                continue
            i.update()
            i.draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.rect.height - 20, 100, 10))  # Dessinez la barre de vie en rouge
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.rect.height - 20, self.health, 10))  # Dessinez la santé actuelle en vert

        
    def add_square(self, square):
        self.squares.append(square)
        self.health += 10

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

    platform_x = 0
    platform_y = 540
    platform_width = 1200

    blue_squares = [BlueSquare(random.randint(platform_x, platform_x + platform_width), platform_y - 50) for _ in range(5)]

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == BLUE_SQUARE_RESPAWN_EVENT:
                new_square = BlueSquare(random.randint(platform_x, platform_x + platform_width), platform_y - 50)
                blue_squares.append(new_square)
                pygame.time.set_timer(BLUE_SQUARE_RESPAWN_EVENT, 0)
          # Mettre à jour l'écran

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
            window.blit(square.image, square.rect)

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
    pygame.quit()
create_window()
