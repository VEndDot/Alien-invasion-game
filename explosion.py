import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """Класс для представления взрыва"""
    
    def __init__(self, ai_settings, screen, x, y):
        """Инициализирует взрыв в заданной позиции"""
        super(Explosion, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Загрузка изображений взрыва и получение прямоугольника
        self.images = []
        for i in range(1, 7):
            filename = f"explosion{i}.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (50, 50))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        # Установка начальной позиции взрыва
        self.rect.x = x
        self.rect.y = y
        
        self.frame = 0
        self.delay = 50
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        """Обновление взрыва"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center