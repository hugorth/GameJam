import pygame

class Ennemi:
    def __init__(self, x, y, speed, sprite_sheet_path, scale_factor):
        self.x = x
        self.y = y
        self.speed = speed
        self.walking_frames = self.load_ace(sprite_sheet_path, 1, 8)
        self.walking_frames = [pygame.transform.scale(image, (image.get_width() * scale_factor, image.get_height() * scale_factor)) for image in self.walking_frames]
        self.current_frame = 0
        self.wait_counter = 0
        self.frame_counter = 0
        self.wait_delay = 30
        self.frame_delay = 5
        self.is_flipped = False
        self.total_direction = 0
        #self.rect = pygame.Rect(self.x, self.y, 100, self.sprite_sheets.get_height() - 30)

    def load_ace(self, path, start, end):
        images = [pygame.image.load(f'{path}ace_{i}.png') for i in range(start, end)]
        return images  # return the list of images

    def update(self, fireballs):
        if self.current_frame < len(self.walking_frames) - 1:  # If the animation is not finished
            self.frame_counter += 1
            if self.frame_counter > self.frame_delay:
                self.frame_counter = 0
                self.current_frame += 1
                #self.throw_fireball()
        else:  # If the animation is finished
            self.wait_counter += 1
            if self.wait_counter > self.wait_delay:  # If the wait time is over
                self.wait_counter = 0
                self.current_frame = 0  # Restart the animation

    def draw(self, window, x_ennemi, direction, speed_up):
        window.blit(pygame.transform.flip(self.walking_frames[self.current_frame], self.is_flipped, False), (self.x, self.y))
        return x_ennemi

    def chase(self, character, direction, speed_up):
        self.x += 4 * direction + (speed_up * 2)
        if abs(self.x - character.rect.x) < 50:
            return
        if self.x < character.rect.x:
            self.x += 2 + (speed_up * 2)
            self.is_flipped = False  # Face right
        elif self.x > character.rect.x:
            self.x -= 2 + (speed_up * 2)
            self.is_flipped = True  # Face left

    # def throw_fireball(self):
    #     direction = -1 if self.is_flipped else 1
    #     nouvelle_boule_de_feu = {
    #         'x': self.x,
    #         'y': self.y,
    #         'direction': direction,
    #         'sprite': pygame.image.load('Assets/Fireball/00.png')
    #     }
    #     return nouvelle_boule_de_feu