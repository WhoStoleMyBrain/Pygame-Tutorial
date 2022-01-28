import pygame
import os


class Settings:
    def __init__(self):
        pygame.font.init()
        pygame.mixer.init()
        self.TITLE = "First Game!"
        self.WIDTH = 900
        self.HEIGHT = 500
        self.BORDER_WIDTH = 10
        self.BORDER_HEIGHT = self.HEIGHT
        self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT = 55, 40
        self.BULLET_WIDTH, self.BULLET_HEIGHT = 10, 5

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)

        self.YELLOW_HIT = pygame.USEREVENT + 1  # Syntax for custom events: USEREVENT + X
        self.RED_HIT = pygame.USEREVENT + 2

        self.FPS = 60
        self.VEL = 5
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 3

        self.ROTATE_LEFT = 90
        self.ROTATE_RIGHT = -90

        self.RED_HEALTH = 10
        self.YELLOW_HEALTH = 10

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.BORDER = pygame.Rect((self.WIDTH - self.BORDER_WIDTH) // 2, 0, self.BORDER_WIDTH, self.HEIGHT)

        self.SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),
                                            (self.WIDTH, self.HEIGHT))

        self.YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
        self.YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            self.YELLOW_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), self.ROTATE_LEFT)

        self.RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
        self.RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            self.RED_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), self.ROTATE_RIGHT)

        self.BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
