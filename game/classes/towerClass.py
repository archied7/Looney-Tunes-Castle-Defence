import pygame
import os

class Tower():
    def __init__(self) -> None:
        self.loadImages()
        self.image = self.towerImage

    def render(self, screen: pygame.Surface, x: int, y: int) -> None:
        screen.blit(self.image, (x,y))
    
    #abstract function to load tower image
    def loadImages(self) -> None:
        pass

    #abstract function to add the bonus
    def bonus(self, game: object) -> None:
        pass

    def remove(self, game: object) -> None:
        pass

class HealthTower(Tower):
    def __init__(self) -> None:
        #intialise parent class
        Tower.__init__(self)

        #set variables
        self.cost = 100
        self.name = 'healthTower'

    def bonus(self, game: object) -> None:
        #increase castle health by 100
        game.castle.maxHealth += 100
        game.castle.currentHealth = game.castle.maxHealth


    def remove(self, game: object) -> None:
        #reset the castles health
        game.castle.maxHealth -= 100
        game.castle.currentHealth = game.castle.maxHealth


    def loadImages(self) -> None:
        #load tower image
        self.towerImage = pygame.image.load(os.getcwd() + '/assets/main game/health tower.png')
        self.towerImage = pygame.transform.scale_by(self.towerImage, 0.25)


class GoldTower(Tower):
    def __init__(self) -> None:
        #intialise parent class
        Tower.__init__(self)

        #initialise variables
        self.cost = 100
        self.name = 'goldTower'

    def bonus(self, game: object) -> None:
        #set gold multiplier
        game.goldMultiplier = 1.5

    def remove(self, game: object) -> None:
        #reset gold multiplier
        game.goldMultiplier = 1

    def loadImages(self) -> None:
        #load tower image
        self.towerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold tower.png')
        self.towerImage = pygame.transform.scale_by(self.towerImage, 0.25)
