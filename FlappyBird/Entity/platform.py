from .entity import Entity
import pygame

class Platform(Entity):
    def __init__(self, y):
        super(Platform, self).__init__(0, y)
        
        self.width, self.height = 420, 112
        self.platform1_x = self.x
        self.platform2_x = self.x + self.width

        self.image = pygame.transform.scale(pygame.image.load('assets/base.png'), (self.width, self.height))
    
    
    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width * 2, self.height)


    def move(self):
        self.platform1_x -= 1.5
        self.platform2_x -= 1.5

        if self.platform1_x + self.width < 0:
            self.platform1_x = self.platform2_x + self.width

        if self.platform2_x + self.width < 0:
            self.platform2_x = self.platform1_x + self.width


    def draw(self, display):
        display.blit(self.image, (self.platform1_x, self.y))
        display.blit(self.image, (self.platform2_x, self.y))