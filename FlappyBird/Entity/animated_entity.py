from abc import abstractmethod

import pygame
from .entity import Entity

class AnimatedEntity(Entity):
    def __init__(self, x, y, images, animation_time):
        super(AnimatedEntity, self).__init__(x, y)
        
        self.animation_images = list(self.load_images(images))
        self.animation_time = animation_time

        self.current_time = 0
        self.index = 0


    def load_images(self, images):
        for image in images:
            yield pygame.image.load(image)


    def reset_time(self):
        self.current_time = 0


    def get_animation_images(self):
        return self.animation_images


    def get_current_image(self):
        return self.animation_images[self.index]


    @abstractmethod
    def update_animation(self):
        raise NotImplementedError()


    
