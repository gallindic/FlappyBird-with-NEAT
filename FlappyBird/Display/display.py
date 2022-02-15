import pygame

class Display():
    def __init__(self, window_width=640, window_height=800, window_title='Pygame Window', background=None, icon=None):
        self.window_width = window_width
        self.window_height = window_height
        self.window_title = window_title
        
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (window_width, window_height))
        
        self._set_title()
        self.display = self._create_display()
        
        
        if icon:
            self._set_icon(icon)
    
    
    def _create_display(self):
        return pygame.display.set_mode((self.window_width, self.window_height), pygame.DOUBLEBUF)
    
    
    def _set_title(self):
        pygame.display.set_caption(self.window_title)
        
        
    def _set_icon(self, icon):
        display_icon = pygame.image.load(icon)
        pygame.display.set_icon(display_icon)
        
        
    def get_display(self):
        return self.display
    
    
    def get_width(self):
        return self.window_width
    
    
    def get_height(self):
        return self.window_height
    
    
    def display_background(self):
        self.display.blit(self.background, (0, 0))
    
    
    def update_display(self):
        pygame.display.flip()