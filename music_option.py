import pygame

class Music:
    def __init__(self):
        self.start_music()
        self.sound_gunshot()

    def start_music(music_volume=0.2):
        """Воспроизводит саундтрек игры"""
        pygame.mixer.music.load('musics\\anamnez-vremja.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(music_volume)

    def sound_gunshot(sound_volume=0.4):
        """Воспроизводит звуки выстрелов"""
        gunshot_sound = pygame.mixer.Sound('musics/laser-blast_zjrhvyvd.mp3')
        gunshot_sound.set_volume(sound_volume)
        gunshot_sound.play()