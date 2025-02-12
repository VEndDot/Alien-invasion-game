from pygame.sprite import Sprite
import pygame
class HP(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализирует сердце и задает его начальную позицию"""
        super(HP, self).__init__()
        
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения сердца и получение прямоугольника
        self.image = pygame.image.load('images\HP.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()