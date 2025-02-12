import pygame

from settings import Settings
class Ship():
    def __init__(self, ai_settings, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        super(Ship, self).__init__()
        
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения корабля и получение прямоугольника
        self.image = pygame.image.load('images\shipTop.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый корабль появляется унижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра корабля 
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Флаг перемещения 
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_down = False


    def update(self):
        # Вид корабля по умолчанию
        self.image = pygame.image.load('images\shipTop.png')
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.image = pygame.image.load('images\shipRight.png')
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.image = pygame.image.load('images\shipLeft.png')
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_top and self.rect.top > 0:
            self.image = pygame.image.load('images\shipTop2.png')
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.image = pygame.image.load('images\shipBottom.png')
            self.centery += self.ai_settings.ship_speed_factor

        # Обновление атрибута rect на основании self.center
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - self.rect.height / 2
        #После смерти, скорость пришельцев становиться по дефолту
        #self.ai_settings.alien_speed_factor = 1
        
    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

