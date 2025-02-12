import pygame
import random

class Raindrop(pygame.sprite.Sprite):
    """Класс представляющий капли дождя"""
    def __init__(self, ai_settings, screen):
        """Инициализация капли дождя"""
        super(Raindrop, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Создание изображения капли дождя
        self.image = pygame.Surface((2, 10))
        self.image.fill((0, 0, 255))  # Цвет капель дождя (голубой)
        self.rect = self.image.get_rect()

        # Установка начальной позиции капли дождя
        self.rect.x = random.randint(0, ai_settings.screen_width)
        self.rect.y = random.randint(-100, 0)

        # Установка случайной скорости падения капли дождя
        self.speed_y = random.randint(1, 5)

    def update(self):
        """Обновление позиции капли дождя"""
        self.rect.y += self.speed_y
        # Перемещение капли вверх, если она достигла нижней границы экрана
        if self.rect.top > self.ai_settings.screen_height:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, self.ai_settings.screen_width)

    def draw(self):
        """Отображение капли дождя на экране"""
        self.screen.blit(self.image, self.rect)

class RainManager:
    def __init__(self, ai_settings, screen):
        """Управление каплями дождя"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.raindrops = pygame.sprite.Group()

    def create_raindrops(self, number):
        """Создание указанного количества капель дождя"""
        for i in range(number):
            raindrop = Raindrop(self.ai_settings, self.screen)
            self.raindrops.add(raindrop)

    def update(self):
        """Обновление всех капель дождя"""
        self.raindrops.update()

    def draw(self):
        """Отображение всех капель дождя на экране"""
        for raindrop in self.raindrops.sprites():
            raindrop.draw()