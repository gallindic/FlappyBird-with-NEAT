import pygame
import random
from .entity import Entity

class Pipe(Entity):
    GAP = 130

    def __init__(self, x, y, flip_vertical=False, height=None):
        super(Pipe, self).__init__(x, y)
        
        self.width = 52
        self.height = height
        self.passed = False
        self.is_top_pipe = flip_vertical

        if height is None:
            self.random_height()

        self.image = pygame.image.load('assets/pipe-green.png')

        if flip_vertical:
            self.image = pygame.transform.flip(self.image, False, True)
        else:
            self.y -= self.height
            self.pipe_pos_y = self.y
        
        
    def random_height(self):
        self.height = random.randrange(150, 320)
        self.pipe_pos_y = -(320 - self.height)
        
            
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    
    def move(self):
        self.update_pos(x=-1.5)


    def is_offscreen(self):
        return self.x + self.width < 0


    def set_passed(self):
        self.passed = True


    def draw(self, display):
        display.blit(self.image, (self.x, self.pipe_pos_y, self.width, self.height))
