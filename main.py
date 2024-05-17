import pygame

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
        self.speed = 2
        self.jumping = False
        self.jump_height = 10
        self.gravity = 1
        self.fall_speed = 0
        self.max_fall_speed = 15
        self.start_x = x
        self.start_y = y

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

    def update(self):
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

    def move(self, direction):
        if direction == 'right':
            self.rect.x += self.speed
        elif direction == 'left':
            self.rect.x -= self.speed

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))
        self.rect = pygame.Rect(x, y, width, height)

def create_window():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('GameJam de la mort')

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (1280, 720))
    
    platforms = [Platform(100, 500, 200*0.9, 10*0.9),
                Platform(400, 400, 200*0.9, 10*0.9),
                Platform(700, 300, 200*0.9, 10*0.9),
                Platform(1000, 200, 200*0.9, 10*0.9),
                Platform(1300, 100, 200*0.9, 10*0.9),
                Platform(1600, 0, 200*0.9, 10*0.9)]
    
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

        for platform in platforms:
            if animated_sprite.rect.colliderect(platform.rect):
                animated_sprite.fall_speed = 0
                animated_sprite.rect.y = platform.rect.y - animated_sprite.rect.height

        window.blit(background, (0, -40))
        for platform in platforms:
            window.blit(platform.image, platform.rect)
        animated_sprite.update()
        window.blit(animated_sprite.image, animated_sprite.rect)
        pygame.display.flip()
    pygame.quit()
create_window()
