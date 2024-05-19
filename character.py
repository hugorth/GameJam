import pygame

class Character:
    def __init__(self, x, y, speed, sprite_sheet_path, scale_factor):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet.get_width() * scale_factor, self.sprite_sheet.get_height() * scale_factor))  # Ajoutez cette ligne
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 5
        self.walking_frames = self.load_frames(self.sprite_sheet, 96 * scale_factor, 96 * scale_factor)
        self.running_frames = self.load_frames(self.sprite_sheet, 96 * scale_factor, 96 * scale_factor)
        self.is_running = False
        self.is_flipped = False
        self.jump_height = 15
        self.jump_speed = 5
        self.is_jumping = False
        jump_sprite_sheet = pygame.image.load('Assets/Ninja_Monk/Jump.png')
        jump_sprite_sheet = pygame.transform.scale(jump_sprite_sheet, (jump_sprite_sheet.get_width() * scale_factor, jump_sprite_sheet.get_height() * scale_factor))  # Ajoutez cette ligne
        self.jump_frames = self.load_frames(jump_sprite_sheet, 96 * scale_factor, 96 * scale_factor)
        self.jump_counter = 0
        self.rect = pygame.Rect(300, 300, 50, self.sprite_sheet.get_height() - 30)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_frame = 0

    def update(self, keys):
        self.rect.x = self.x + 75
        self.rect.y = self.y + 25
        self.is_running = keys[pygame.K_LSHIFT]

        speed_multiplier = 2 if self.is_running else 1
        if keys[pygame.K_q]:
            self.x -= self.speed * speed_multiplier
            self.is_flipped = True
        elif keys[pygame.K_d]:
            self.x += self.speed * speed_multiplier
            self.is_flipped = False

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            frames = self.running_frames if self.is_running else self.walking_frames
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_counter = 0
 
        if self.is_jumping:
            frames = self.jump_frames
            if self.jump_frame > 8:
                self.is_jumping = False
            progress = self.jump_frame / self.jump_speed
            if self.jump_frame < self.jump_height / 2 + 1:
                height = (4 * (progress - 0.5) ** 2 - 1) * -self.jump_height
            else:
                height = (4 * (progress - 0.5) ** 2 - 1) * self.jump_height
            self.y -= height
            if self.y > 400:
                self.is_jumping = False
                self.jump_frame = 0
                self.y = 400

            self.jump_counter += 1
            if self.jump_counter >= self.frame_delay:
                self.jump_frame += 1
                self.jump_counter = 0
        else:
            frames = self.running_frames if self.is_running else self.walking_frames

    def draw(self, surface):
        if self.is_jumping:
            frames = self.jump_frames if self.is_jumping else (self.running_frames if self.is_running else self.walking_frames)
            image = frames[self.current_frame]
            if self.is_flipped:
                image = pygame.transform.flip(image, True, False)
            surface.blit(image, (self.x, self.y))
        else:
            frames = self.running_frames if self.is_running else self.walking_frames
            frame = pygame.transform.flip(frames[self.current_frame], self.is_flipped, False)
            surface.blit(frame, (self.x, self.y))

    def load_frames(self, sprite_sheet, frame_width, frame_height):
        frames = []
        sprite_sheet = sprite_sheet.convert_alpha()
        sprite_sheet_width, sprite_sheet_height = sprite_sheet.get_size()
        for y in range(0, sprite_sheet_height, frame_height):
            for x in range(0, sprite_sheet_width, frame_width):
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
                frames.append(frame)
        return frames