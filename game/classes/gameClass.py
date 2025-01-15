from classes.towerClass import HealthTower, GoldTower
from classes.castleClass import Castle
from classes.heroes.bugsBunnyClass import BugsBunny
from classes.heroes.daffyDuckClass import DaffyDuck
from classes.heroes.tazClass import Taz
from classes.heroes.yosemiteSamClass import YosemiteSam
from classes.enemies.elmerFuddClass import ElmerFudd
from classes.enemies.sylvesterClass import Sylvester
from classes.enemies.marvinMartianClass import MarvinMartian
from classes.spriteLoader import SpriteLoader
from classes.linkedListClass import LinkedList
from classes.archersClass import Archers

import random
import os
import pygame

class Game:
    def __init__(self) -> None:
        """"
        self.currentHeroes = {hero: position
                              hero: position
                              ...}
        """""
        self.ownedTowers = []
        self.currentTower = None
        self.ownedHeroes = []
        self.currentHeroes = {1: None, 2: None, 3: None, 4: None}
        self.gold = 0
        self.paused = False
        self.pauseTick = 0
        self.round = 1
        self.roundComplete = False

        self.enemyAmount = 3
        self.enemyCounter = 0
        self.enemyFreq = 5000
        self.lastEnemy = pygame.time.get_ticks() - self.enemyFreq

        self.projectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()

        self.loadSprites()

        self.castle = Castle()
        self.archers = Archers(self.projectileGroup, self.enemyGroup)
        self.bugsBunny = BugsBunny(self.bugsSprites, self.bugsBunnyMeta)
        self.daffyDuck = DaffyDuck(self.daffySprites, self.daffyDuckMeta, self.arrowImage)
        self.taz = Taz(self.tazSprites, self.tazMeta, self.projectileGroup, self.enemyGroup)
        self.yosemiteSam = YosemiteSam(self.yosemiteSamSprites, self.yosemiteSamMeta, self.projectileGroup, self.enemyGroup)

        self.healthTower = HealthTower()
        self.goldTower = GoldTower()
        self.goldMultiplier = 1
        

    def generateEnemies(self, dt, castle) -> None:
        timeNow = pygame.time.get_ticks()
        if timeNow - self.lastEnemy > self.enemyFreq and not self.roundComplete:
            if self.enemyCounter < self.enemyAmount:
                pos = random.choice([600,500,400])
                counter = 0
                enemies = []
                while counter is not self.enemyAmount:
                    if self.round < 5:
                        enemies.append(1)
                    elif self.round < 10:
                        enemies.append(random.choice([1,2]))
                    elif self.round >= 10:
                        enemies.append(random.choice([1,2,3]))
                    
                    counter += 1


                if self.round != 1:
                    multiplier = 1 + self.round*0.1
                else:
                    multiplier = 1

                if enemies[0] == 1:
                    sylvester = Sylvester(self.sylvesterSprites, self.sylvesterMeta, pos, castle, multiplier)
                    self.enemyGroup.add(sylvester)
                    
                elif enemies[0] == 2:
                    elmer = ElmerFudd(self.elmerSprites, self.elmerFuddMeta, pos, castle, multiplier, self.enemyProjectileGroup)
                    self.enemyGroup.add(elmer)
                
                elif enemies[0] == 3:
                    marvin = MarvinMartian(self.marvinSprites, self.marvinMartianMeta, pos, castle, multiplier, self.enemyProjectileGroup)
                    self.enemyGroup.add(marvin)

                self.lastEnemy = pygame.time.get_ticks()
                enemies.pop(0)
                self.enemyCounter += 1
                    
            else:
                self.roundComplete = True
                self.enemyCounter = 0
                if self.enemyFreq >= 500:
                    self.enemyFreq -= 100
                if self.round % 3 == 1:
                    self.enemyAmount += 1


    #adds a hero object to the ownedHeroes list
    def purchaseHero(self, hero: object, position: int, type = 0) -> None:
        if type == 0:
            if self.gold >= 100:
                self.ownedHeroes.append(hero)
                self.currentHeroes[position] = hero
                self.gold -= 100
        else:
            self.ownedHeroes.append(hero)

    #modifies the currentHeroes list
    def changeHero(self, hero: object, change: str, position: int) -> None:
        if hero in self.ownedHeroes:
            if change == "remove":
                for key in self.currentHeroes:
                    if self.currentHeroes[key] == hero:
                        self.currentHeroes[key] = None
                        break

            elif change == "add":
                self.currentHeroes[position] = hero

            elif change == "replace":
                for key in self.currentHeroes:
                    if self.currentHeroes[key] == hero:
                        self.currentHeroes[key] = None
                        break
                self.currentHeroes[position] = hero
            
        
    def levelHero(self, hero: object):
        if hero.upgradePrice != 'MAX':
            if self.gold >= hero.upgradePrice:
                self.gold -= hero.upgradePrice
                hero.levelUp()
    
    #adds a tower object to the ownedTowers list
    def purchaseTower(self, tower: object) -> None:
        if tower.cost <= self.gold:
            self.ownedTowers.append(tower)
            self.currentTower = tower
            self.currentTower.bonus(self)
            self.gold -= tower.cost

    #changes the tower stored in the currentTower attribute
    def changeTower(self, tower: object, change: str) -> None:
        if tower in self.ownedTowers:
            if change == "remove":
                self.currentTower = None
            elif change == "replace":
                self.currentTower.remove(self)
                self.currentTower = tower
                self.currentTower.bonus(self)

    def changeGold(self, value: int, remove: bool) -> int:
        if remove: 
            self.gold -= value
        else:
            self.gold += value

        reward = int(self.gold * 0.1)
        if reward <= 250:
            if reward >= 1:
                return reward
            else:
                return 1
        else:
            return 250

    def getGold(self) -> int:
        return self.gold

    def changePause(self) -> None:
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def getPause(self) -> None:
        return self.paused
    
    def getCurrentHeroes(self) -> list:
        return self.currentHeroes
    
    def getCurrentTower(self) -> list:
        return self.currentTower
    
    def getEnemies(self) -> list:
        return self.enemies

    def loadSprites(self) -> None:
        #loads character sprite sheets used in main game
        self.bugsBunnySpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/bugs bunny.png')
        self.bugsBunnyMeta = os.getcwd() + '/assets/characters/bugs bunny meta.json'
        self.daffyDuckSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/daffy duck.png')
        self.daffyDuckMeta = os.getcwd() + '/assets/characters/daffy duck meta.json'
        self.elmerFuddSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/elmer fudd.png')
        self.elmerFuddMeta = os.getcwd() + '/assets/characters/elmer fudd meta.json'
        self.marvinMartianSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/marvin martian.png')
        self.marvinMartianMeta = os.getcwd() + '/assets/characters/marvin martian meta.json'
        self.sylvesterSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/sylvester pussycat.png')
        self.sylvesterMeta = os.getcwd() + '/assets/characters/sylvester pussycat meta.json'
        self.tazSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/taz.png')
        self.tazMeta = os.getcwd() + '/assets/characters/taz meta.json'
        self.yosemiteSamSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/yosemite sam.png')
        self.yosemiteSamMeta = os.getcwd() + '/assets/characters/yosemite sam meta.json'

        #loads lists containing individual sprites
        bugsSpritesObject = SpriteLoader(self.bugsBunnyMeta, self.bugsBunnySpriteSheet)
        self.bugsSprites = bugsSpritesObject.getSpritesList()

        daffyDuckSpritesObject = SpriteLoader(self.daffyDuckMeta, self.daffyDuckSpriteSheet)
        self.daffySprites = daffyDuckSpritesObject.getSpritesList()

        elmerSpritesObject = SpriteLoader(self.elmerFuddMeta, self.elmerFuddSpriteSheet)
        self.elmerSprites = elmerSpritesObject.getSpritesList()

        marvinSpritesObject = SpriteLoader(self.marvinMartianMeta, self.marvinMartianSpriteSheet)
        self.marvinSprites = marvinSpritesObject.getSpritesList()

        sylvesterSpritesObject = SpriteLoader(self.sylvesterMeta, self.sylvesterSpriteSheet)
        self.sylvesterSprites = sylvesterSpritesObject.getSpritesList()

        tazSpritesObject = SpriteLoader(self.tazMeta, self.tazSpriteSheet)
        self.tazSprites = tazSpritesObject.getSpritesList()

        yosemiteSamSpritesObject = SpriteLoader(self.yosemiteSamMeta, self.yosemiteSamSpriteSheet)
        self.yosemiteSamSprites = yosemiteSamSpritesObject.getSpritesList()

        self.arrowImage = pygame.image.load(os.getcwd() + '/assets/main game/arrow.png')
        self.arrowImage = pygame.transform.rotate(self.arrowImage, 90)
        self.arrowImage = pygame.transform.scale_by(self.arrowImage, 10)
