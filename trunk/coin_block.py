import pygame
from trunk.entity import Entity
from pygame.locals import *

__author__ = 'Weekend Warriors'


class CoinBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        pygame.init()
        self.image = pygame.Surface((32, 32))
        self.circle = pygame.draw.circle(self.image, Color("#FFFF00"), (16, 16), 16)
        self.rect = Rect(x, y, 32, 32)
        self.collected = False


    def play_collect(self):
        effect = pygame.mixer.Sound('resources/sound/coin.wav')
        effect.play()