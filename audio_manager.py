import pygame


class AudioManager:
    @staticmethod
    def init():
        pygame.mixer.init()

    @staticmethod
    def loop_music(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def play_audio(audio_path, volume=1.0):
        sound = pygame.mixer.Sound(audio_path)
        sound.set_volume(volume)
        sound.play()