import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from star import Star 
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from raindrop import Raindrop
from raindrop import RainManager 
import game_functions as gf

def run_game():
    """Инициализирует игру и создает объекты экрана"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")

    # Cоздание экземпляров GameStats and Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Создание корабля
    ship = Ship(ai_settings, screen)

    # Создание корабля, группы пуль, пришельцев и звезд
    bullets = Group() 
    aliens = Group()
    stars = Group()

    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Создание звездного пространства 
    gf.create_fleet_stars(ai_settings, screen, ship, stars)

    rain_manager = RainManager(ai_settings, screen)
    rain_manager.create_raindrops(100)  # Создание 100 капель дождя


    # Запуск основного цикла игры
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update() 
            gf.update_bullets(ai_settings, screen, stats, sb, ship,  aliens, bullets, stars)
            rain_manager.update()
            gf.update_aliens(ai_settings, screen, stats, sb,  ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, stars, bullets, play_button)
        rain_manager.draw()  # Отображение дождя
run_game()
