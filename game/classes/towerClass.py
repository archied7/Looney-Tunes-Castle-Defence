import pygame
import os

class Tower():
    def __init__(self):
        self.loadImages()
        self.image = self.towerImage

    def render(self, screen, x, y):
        screen.blit(self.image, (x,y))
    
    def loadImages(self):
        pass

    def bonus(self):
        pass

    def removed(self):
        pass

class HealthTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.cost = 100
        self.name = 'healthTower'

    def bonus(self, game):
        game.castle.maxHealth += 100
        game.castle.currentHealth = game.castle.maxHealth


    def remove(self, game):
        game.castle.maxHealth -= 100
        game.castle.currentHealth = game.castle.maxHealth


    def loadImages(self):
        self.towerImage = pygame.image.load(os.getcwd() + '/assets/main game/health tower.png')
        self.towerImage = pygame.transform.scale_by(self.towerImage, 0.25)


class GoldTower(Tower):
    def __init__(self):
        Tower.__init__(self)
        self.cost = 100
        self.name = 'goldTower'

    def bonus(self, game):
        game.goldMultiplier = 1.5

    def remove(self, game):
        game.goldMultiplier = 1

    def loadImages(self):
        self.towerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold tower.png')
        self.towerImage = pygame.transform.scale_by(self.towerImage, 0.25)