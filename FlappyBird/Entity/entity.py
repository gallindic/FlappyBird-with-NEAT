from abc import abstractmethod
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Entity, self).__init__()
        self.x, self.y = x, y

    
    def get_pos(self):
        return (self.x, self.y)
    
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        
        
    def update_pos(self, x=0, y=0):
        self.x += x
        self.y += y


    def get_rect(self):
        return self.rect


    @abstractmethod
    def move(self):
        raise NotImplementedError()

    
    @abstractmethod
    def draw(self, display):
        raise NotImplementedError()