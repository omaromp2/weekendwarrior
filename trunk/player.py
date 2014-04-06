import pygame
from pygame.surface import Surface
from trunk.coin_block import CoinBlock
from trunk.entity import Entity
from pygame.locals import *
from trunk.exit_block import ExitBlock
from trunk.spike_block import SpikeBlock

PLAYER_SIZE = (32, 32)
PLAYER_COLOR = "#FF0000"
#PLAYER_SURFACE = pygame.image.load('resources/images/sprites.png')

__author__ = 'Weekend Warriors'


class Player(Entity):

    def __init__(self, x, y):
        pygame.init()
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.is_dead = False
        self.next = False
        self.level = 1
        self.on_ground = False
        self.image = Surface(PLAYER_SIZE)
        self.image.convert()
        self.image.fill(Color(PLAYER_COLOR))
        #self.image.fill.blit(PLAYER_SURFACE,x,y)
        self.rect = Rect(x, y, 32, 32)
        self.check = False

    def update(self, up, down, left, right, platforms):
        if up:
            # only jump if on the ground
            if self.on_ground: self.yvel -= 7
        if down:
            pass
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.on_ground:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 30: self.yvel = 30
        if not (left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.on_ground = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def coin_check(self, platforms):
        for p in platforms:
            if isinstance(p, CoinBlock):
                return False
        return True

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    if self.coin_check(platforms):
                        self.next = True
                        self.level += 1
                if isinstance(p, SpikeBlock):
                    self.is_dead = True
                if isinstance(p, CoinBlock):
                    p.collected = True
                    continue
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.yvel = 0
                if yvel < 0: self.rect.top = p.rect.bottom