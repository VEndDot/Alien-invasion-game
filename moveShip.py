import sys
import pygame
from bullet import Bullet
import game_functions as gf
from music_option import Music

def move_run_ship(event, ai_settings, screen, ship, bullets):
    """Движение корабля, если клавиша нажата"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_top = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        Music.sound_gunshot()
        # Создание новой пули и включение ее в группу bullets
        gf.fire_bullet(ai_settings, screen, ship, bullets)
    # Завершает игру клавишей ESC
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def move_stop_ship(event, ship):
    """Остановка корабля, если клавиша отжата"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_top = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False