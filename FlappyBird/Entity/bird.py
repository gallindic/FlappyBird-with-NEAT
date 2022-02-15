from .animated_entity import AnimatedEntity
import pygame

class Bird(AnimatedEntity):
    IMAGES = ['assets/yellowbird-upflap.png', 'assets/yellowbird-midflap.png', 'assets/yellowbird-downflap.png']

    def __init__(self, x, y, animation_time):
        super().__init__(x, y, self.IMAGES, animation_time)

        self.gravity = 0.1
        self.momentum = 0
        self.upward_momentum = 4
        self.width, self.height = (30 * 1.3, 24 * 1.2)

        self.scale_bird()


    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


    def scale_bird(self):
        for i, image in enumerate(self.animation_images):
            self.animation_images[i] = pygame.transform.scale(image, (self.width, self.height))


    def move(self):
        self.update_animation()
        self.momentum += self.gravity

        if self.momentum > 5:
            self.momentum = 5

        if self.y < 0:
            self.set_pos(self.x, 0)
            self.momentum = 0

        self.update_pos(y=self.momentum)


    def draw(self, display):
        display.blit(self.get_current_image(), self.get_rect())


    def jump(self):
        self.momentum = -self.upward_momentum


    def has_passed(self, pipe):
        return self.x > pipe.x + pipe.width


    def update_animation(self):
        self.current_time += 1

        if self.current_time <= self.animation_time:
            self.index = 0
        elif self.current_time <= self.animation_time * 2:
            self.index = 1
        elif self.current_time <= self.animation_time * 3:
            self.index = 2
        elif self.current_time <= self.animation_time * 4:
            self.index = 1
        elif self.current_time == self.animation_time * 4 + 1:
            self.index = 0
            self.reset_time()


    def has_hit_celling(self):
        return self.y <= 0


    def has_collided(self, pipe):
        return self.get_rect().colliderect(pipe.get_rect())