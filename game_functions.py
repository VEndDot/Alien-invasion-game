import sys
import pygame
import moveShip as move
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from time import sleep
from ship import Ship
from music_option import Music
from read_and_write_record import ReadAndWrite as RAW

def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        #Записываем новый рекорд
        RAW.write_record_to_file(stats.high_score)
        sb.prep_high_score()



def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит тоже, что и при сталкновении с кораблем
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
           move.move_run_ship(event, ai_settings, screen, ship, bullets) 
        elif event.type == pygame.KEYUP:
           move.move_stop_ship(event, ship) 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Музыка
        Music.start_music()
        # Сброс игровых настроек
        ai_settings.initialize_dynamic_settings()
        # Сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True
        
        # Сброс изображений счетов и уровня
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре 
        
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, ship, alien_number, row_number):
    # Создает пришельца и размещает его в ряду
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    
    if pygame.sprite.collide_rect(alien, ship):
        # Удаляет пришельца, если корабль находится на месте спавна, а также перемещает корабль в сейв зону
        aliens.remove(alien)
        Ship.center_ship(ship)
    else:
        aliens.add(alien)

    #aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Создание флота пришельцев
    for row_number in range(number_rows):   
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, ship, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обрабатывает столкновение коробля с пришельцем"""
    if stats.ships_left > 0:
        # Уменьшение ships_left
        stats.ships_left -= 1
        # Обновление игровой информации
        sb.prep_ships()
        # Очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        # Указатель появляется
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Проверяет, достиг ли флот края экрана,
    после чего обновляет позиции всех пришельцев во флоте
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()              
    
    #Проверка коллизий пиришелец-корабль
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    #Проверка пришельцев добравшихся до нижнего края экрана
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def get_number_stars_x(ai_settings, star_width):
    """Вычисляет количество звезд в ряду"""
    available_space_x = star_width
    number_stars_x = star_width
    return number_stars_x

def create_star(ai_settings, screen, stars, star_namber, row_number_star):
    """Создает звезду и размещает ее в ряду"""
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star.x = star_width + 2 * star_width * star_namber 
    star.rect.x = star.x
    star.rect.y = star.rect.height + 2 * star.rect.height * row_number_star
    stars.add(star)

def create_fleet_stars(ai_settings, screen, ship, stars):
    """Создает звездное пространство"""
    # Cоздание звезды и вычисление количества звезд в ряду
    # Создание первого ряда звезд
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    number_rows_star = get_number_rows_stars(ai_settings, ship.rect.height, star.rect.height)
    
    # Создание звездного пространства
    for row_number_star in range(randint(4,16)):
        for star_number in range(randint(5,13)):
            # Создание звезды и размещение ее в ряду
            create_star(ai_settings, screen, stars, star_number, row_number_star)

def get_number_rows_stars(ai_settings, ship_height, star_height):
    """Определяет количество рядов, помещающихся на экране"""
    avalable_space_y = (ai_settings.screen_height)
    number_rows_stars = star_height
    return number_rows_stars

def update_screen(ai_settings, screen, stats, sb, ship, aliens, star, bullets, play_button):
    """Обновляет изображение на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)
    # Все пули выводятся позади изображения корабля и пришельцев
    star.draw(screen)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()  
    
    # Вывод счета
    sb.show_score()

    # Кнопка Play отображается в том случае, если игра не активна
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()



def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, stars):
    """Обновляет позиции пуль и уничтожает старые пули"""
    # Обновление позиций пуль
    bullets.update()
    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, stars)
    # Отображение последнего прорисованного экрана
    
    pygame.display.flip()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, stars,):
    """Обработка коллизий пуль с пришельцами и обновление звездного неба"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
        

    if len(aliens) == 0:
        # Если весь флот уничтожен, начинается следующий уровень
        bullets.empty()
        #Увеличиваем скорость флота, после уничтожения флота
        ai_settings.increase_speed()
        #Ship.center_ship(ship)
        create_fleet(ai_settings, screen, ship,aliens)
        #Обновляет звездное небо, после уничтжения флота 
        stars.empty()
        # Увеличение уровня
        stats.level += 1
        sb.prep_level()
        create_fleet_stars(ai_settings, screen, ship, stars)
        

        

def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут"""
    if len(bullets) < ai_settings.bullet_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)  
