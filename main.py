import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.images = [pygame.image.load(img) for img in images]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.counter = 0
        self.delay = 15
        self.speed = 2
        self.jumping = False
        self.jump_height = 10
        self.gravity = 1
        self.fall_speed = 0
        self.max_fall_speed = 15

    def jump(self):
        if not self.jumping:
            self.jumping = True

    def update(self, platforms):
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
                self.jump_height = 10
        if not self.jumping:
            self.fall_speed = min(self.fall_speed + self.gravity, self.max_fall_speed)
            self.rect.y += self.fall_speed
            if pygame.sprite.spritecollide(self, platforms, False):
                self.rect.y -= self.fall_speed
                self.fall_speed = 0

    def move(self, direction):
        if direction == 'right':
            self.rect.x += self.speed
        elif direction == 'left':
            self.rect.x -= self.speed

def create_window():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('GameJam de la mort')

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (1280, 720))

    platforms = pygame.sprite.Group()
    platform1 = Platform(100, 500, 300, 20, (255, 0, 0))  # Crée une plateforme rouge plus grande
    platform2 = Platform(400, 400, 300, 20, (0, 255, 0))  # Crée une plateforme verte plus grande
    platforms.add(platform1, platform2)
    
    sprite_images = ['assets/hero/00_hero.png', 'assets/hero/01_hero.png',
                     'assets/hero/02_hero.png', 'assets/hero/03_hero.png',
                     'assets/hero/04_hero.png', 'assets/hero/05_hero.png',
                     'assets/hero/06_hero.png', 'assets/hero/07_hero.png']
    animated_sprite = AnimatedSprite(sprite_images, 100, 100)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            animated_sprite.move('left')
        if keys[pygame.K_d]:
            animated_sprite.move('right')
        if keys[pygame.K_SPACE]:
            animated_sprite.jump()

        window.blit(background, (0, -40))
        platforms.draw(window)
        animated_sprite.update(platforms)
        window.blit(animated_sprite.image, animated_sprite.rect)

        pygame.display.flip()

    pygame.quit()
create_window()