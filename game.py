import pygame
import random
from character import Character
from parallax import ParallaxLayer
from ennemi import Ennemi

def main_game():
    pygame.init()
    start_ticks = pygame.time.get_ticks()

    score = 0
    speed_up = 0

    window = pygame.display.set_mode((800, 600))
    global window_width, window_height
    window_width, window_height = window.get_size()
    character = Character(300, 400, 0, 'Assets/Ninja_Monk/Walk.png', 2)

    layers = [
        ParallaxLayer('Assets/Sky.png', 0),
        ParallaxLayer('Assets/BG_Decor.png', 0.5 + speed_up),
        ParallaxLayer('Assets/Middle_Decor.png', 1 + (speed_up * 2)),
        ParallaxLayer('Assets/Foreground.png', 2 + (speed_up * 4)),
        ParallaxLayer('Assets/Ground.png', 2.5 + (speed_up * 5)),
    ]

    ennemi = Ennemi(700, 375, 2, 'Assets/Ace_Sprite/', 3)
    x_ennemi = 0

    olympic_food = 10

    olympic = pygame.image.load('Assets/olympic-flame.png')
    olympic = pygame.transform.scale(olympic, (100, 500))

    olympic_flame = load_olympic_flame_frames('Assets/olympic-flame-sprite', 0, 52)
    x_olympic = 0

    flame_images = load_flame_frames('Assets/flame', 0, 48)
    flame_width = 10
    flame_height = 10

    wood_image = pygame.image.load('Assets/wood.png')
    wood_image = pygame.transform.scale(wood_image, (100, 100))

    fireballs = []

    woods = []
    x = 0
    while x < 600:
        woods.append((x, 520, True))
        x += 100 + random.randint(0, 200)

    flames = []
    x = 0
    while x < 600:
        flames.append((x, 460))
        x += 100 + random.randint(0, 200)

    while True:
        start_ticks = pygame.time.get_ticks()
        running = True
        last_decrement_time = pygame.time.get_ticks()
        last_speed_up_time = pygame.time.get_ticks()
        while running:
            current_time = pygame.time.get_ticks()
            if current_time - last_decrement_time >= 4000:
                olympic_food -= 1
                last_decrement_time = current_time
            keys = handle_events(character)
            direction = update_layers(layers, keys, character)
            draw_layers(layers, window)
            character.draw(window)
            ennemi.chase(character, direction, speed_up)
            ennemi.update(fireballs)
            x_ennemi = ennemi.draw(window, x_ennemi, direction, speed_up)
            woods = display_random_woods(window, wood_image, character, woods, direction, speed_up)
            clock = round((pygame.time.get_ticks() - start_ticks) / 1000)
            display_random_flames(window, flame_images, character, flames, direction, speed_up, clock)
            x_olympic = display_olympic_flame(window, olympic, olympic_flame, x_olympic, direction, speed_up)
            display_timer(window, olympic_food)
            time = (pygame.time.get_ticks() - start_ticks) / 1000
            add = round((pygame.time.get_ticks() - start_ticks) / 1000)
            if add % 10 == 0 and current_time - last_speed_up_time >= 10000:
                speed_up += 0.1
                last_speed_up_time = current_time
                layers[1].set_speed(0.5 + speed_up)
                layers[2].set_speed(1 + (speed_up * 2))
                layers[3].set_speed(2 + (speed_up * 4))
                layers[4].set_speed(2.5 + (speed_up * 5))
            display_score(window, time)
            display_best_score(window)
                
            font = pygame.font.Font(None, 36)
            text = font.render(f"Bois : {score}", True, (255, 255, 255))

            rect_color = (165, 42, 42)
            rect_x = window.get_width() - text.get_width() - 10
            rect_y = 0
            rect_width = text.get_width() + 20
            rect_height = text.get_height() + 10
            pygame.draw.rect(window, rect_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))

            text_x = window.get_width() - text.get_width()
            text_y = 5
            window.blit(text, (text_x, text_y))
            
            olympic_rect = pygame.Rect(575 + x_olympic, 400, 140, 200)
            if olympic_food <= 0:
                font = pygame.font.Font(None, 36)
                text = font.render("You Loose !", True, (255, 0, 0))
                text_x = window.get_width() / 2 - text.get_width() / 2
                text_y = window.get_height() / 2 - text.get_height() / 2
                window.blit(text, (text_x, text_y))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            if character.rect.colliderect(olympic_rect) and keys[pygame.K_e]:
                olympic_food += score
                score = 0
            for x, y in flames:
                if character.rect.colliderect(pygame.Rect(x + 60, y + 110, flame_width + 20, flame_height + 20)):
                    font = pygame.font.Font(None, 36)
                    text = font.render("You Loose !", True, (255, 0, 0))
                    text_x = window.get_width() / 2 - text.get_width() / 2
                    text_y = window.get_height() / 2 - text.get_height() / 2
                    window.blit(text, (text_x, text_y))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False
                    break
            for x, y, visible in woods:
                if visible:
                    wood_rect = pygame.Rect(x + 25, y + 25, 70, 70)
                    character_rect = character.rect
                    keys = pygame.key.get_pressed()
                    if character_rect.colliderect(wood_rect) and keys[pygame.K_e]:
                        score += 1
                        woods[woods.index((x, y, visible))] = (x, y, False)
            pygame.display.flip()
        score = 0
        olympic_food = 10
        with open('best-score.txt', 'r') as file:
            best_score = file.read()
        if time > float(best_score):
            replace_best_score(time)
        start_ticks = 0
        speed_up = 0
        time = 0
        x_olympic = 0
        x_ennemi = 0
        flames = []
        x = 0
        while x < 600:
            flames.append((x, 460))
            x += 100 + random.randint(0, 200)

def replace_best_score(best_score):
    seconds = int(best_score)
    with open('best-score.txt', 'w') as file:
        file.write(str(seconds))

def display_best_score(window):
    with open('best-score.txt', 'r') as file:
        best_score = file.read()
    font = pygame.font.Font(None, 36)
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    best_score_x = 350
    best_score_y = 0
    window.blit(best_score_text, (best_score_x, best_score_y))
   

def display_score(window, time):
    seconds = int(time)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {seconds}", True, (255, 255, 255))
    score_x = 575
    score_y = 0
    window.blit(score_text, (score_x, score_y))

def display_timer(window, olympic_food):
    max_width = window.get_width()
    current_width = (olympic_food / 100) * max_width
    bar_height = 20
    timer_bar = pygame.Rect(100, 0, current_width, bar_height)
    pygame.draw.rect(window, (255, 0, 0), timer_bar)

frame_counter = 0
x_olympic = 0

def display_olympic_flame(window, olympic, olympic_flame, x_olympic, direction, speed_up):
    global frame_counter

    if direction > 0:
        x_olympic += 10 + (speed_up * 20)
    if direction < 0:
        x_olympic -= 10 + (speed_up * 20)

    current_frame = olympic_flame[frame_counter % len(olympic_flame)]
    window.blit(current_frame, (500 + x_olympic, 0))
    window.blit(olympic, (600 + x_olympic, 160))
    frame_counter += 1
    return x_olympic

def load_olympic_flame_frames(path, start, end):
    return [pygame.image.load(f'{path}/{i:02d}.png') for i in range(start, end)]


def load_flame_frames(path, start, end):
    return [pygame.image.load(f'{path}/flame_{i:02d}.png') for i in range(start, end)]

frame_counter = 0

def display_random_flames(window, flame_images, character, flames, direction, speed_up, clock):
    global frame_counter
    flame_image = flame_images[frame_counter % len(flame_images)]
    frame_counter += 1
    if frame_counter >= 48:
        frame_counter = 0

    window_width, window_height = window.get_width(), window.get_height()
    flame_width, flame_height = flame_image.get_width(), flame_image.get_height()

    if flame_width > window_width or flame_height > window_height:
        scale_factor = 0.2
        flame_image = pygame.transform.scale(flame_image, (int(flame_width * scale_factor), int(flame_height * scale_factor)))
        flame_width, flame_height = flame_image.get_width(), flame_image.get_height()

    for i, (x, y) in enumerate(flames):
        if direction > 0:
            x += 10 + (speed_up * 20)
        if direction < 0:
            x -= 10 + (speed_up * 20)
        if x < character.x - window_width:
            x = character.x + window_width + random.randint(-200, 200)
            y = 460
        elif x > character.x + window_width:
            x = character.x - window_width + random.randint(-200, 200)
            y = 460

        if abs(x - character.x) < 100 and clock < 1:
            x += 200 if x < character.x else -200

        flames[i] = (x, y)
        window.blit(flame_image, (x, y))

def display_random_woods(window, wood_image, character, woods, direction, speed_up):
    window_width, window_height = window.get_width(), window.get_height()
    wood_width, wood_height = wood_image.get_width(), wood_image.get_height()

    new_woods = []
    for x, y, visible in woods:
        if direction > 0:
            x += 10 + (speed_up * 20)
        if direction < 0:
            x -= 10 + (speed_up * 20)
        if x < character.x - window_width:
            x = character.x + window_width + random.randint(-200, 200)
            y = 520
            visible = True
        elif x > character.x + window_width:
            x = character.x - window_width + random.randint(-200, 200)
            y = 520
            visible = True
        new_woods.append((x, y, visible))
        if visible:
            window.blit(wood_image, (x, y))
    return new_woods

def handle_events(character):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    character.update(keys)
    return keys

def update_layers(layers, keys, character):
    direction = 0
    if keys[pygame.K_q]:
        direction = 2
    if keys[pygame.K_d]:
        direction = -2
    if keys[pygame.K_SPACE]:
        character.jump()
    if keys[pygame.K_a]:
        exit()

    for layer in layers:
        layer.update(direction)
    return direction

def draw_layers(layers, window):
    window.fill((0, 0, 0))
    for layer in layers:
        layer.draw(window)