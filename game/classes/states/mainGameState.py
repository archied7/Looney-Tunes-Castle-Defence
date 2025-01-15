from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.states.minigameSelectState import MinigameSelect
from classes.states.pauseState import Pause
from classes.buttonClass import Button
from classes.castleClass import Castle
from classes.archersClass import Archers
from classes.heroes.bugsBunnyClass import BugsBunny
from classes.states.intermissionMenuState import IntermissionMenu, TowerIntermissionMenu
from classes.states.daffyAbilityState import daffyAbility
import pygame
import os

class MainGame(State):
    def __init__(self, main) -> None:
        """
        currentState = 0 if intermission
                     = 1 if in round
        """
        State.__init__(self, main)
        self.currentState = 0
        self.minigameComplete = True

        self.roundStartButton = Button(1125, 781, self.roundStartImage, 2, self.roundStartHoverImage)
        self.upgradeCastleButton = Button(900, 50, self.castleUpgradeImage, 2, self.castleUpgradeHoverImage)
        self.upgradeArcherButton = Button(1150, 50, self.archerUpgradeImage, 2, self.archerUpgradeHoverImage)
        self.towerSlotButton = Button(615, 726, self.emptySlotImage, 1.5, self.emptySlotHoverImage)

        self.castleSlot1Button = Button(505, 465, self.emptySlotImage, 1, self.emptySlotHoverImage)
        self.castleSlot2Button = Button(376, 511, self.emptySlotImage, 1, self.emptySlotHoverImage)
        self.castleSlot3Button = Button(270, 403, self.emptySlotImage, 1, self.emptySlotHoverImage)
        self.castleSlot4Button = Button(355, 354, self.emptySlotImage, 1, self.emptySlotHoverImage)

        self.castleSlotButtons = [self.castleSlot1Button, self.castleSlot2Button, self.castleSlot3Button, self.castleSlot4Button]

        self.main.game.purchaseHero(self.main.game.bugsBunny, 2, 1)
        self.main.game.currentHeroes[1] = self.main.game.bugsBunny

    def update(self, dt, inputs) -> None:
        pygame.display.update()
        if self.currentState == 0:

            #handles minigame
            if self.minigameComplete == False:
                self.main.saveLoadManager.save()
                nextState = MinigameSelect(self.main)
                nextState.newState()
                self.minigameComplete = True

            else:
                for i in self.main.game.currentHeroes:
                    if self.main.game.currentHeroes[i] is not None:
                        self.castleSlotButtons[i-1].changeImage(self.main.game.currentHeroes[i].intermissionImage, 1)
                    else:
                        self.castleSlotButtons[i-1].changeImage(self.emptySlotImage, 1, self.emptySlotHoverImage)

                if self.main.game.currentTower:
                    self.towerSlotButton.changeImage(self.main.game.currentTower.image, 1)
                else:
                    self.towerSlotButton.changeImage(self.emptySlotImage, 1.5, self.emptySlotHoverImage)

        else:
            self.main.game.generateEnemies(dt, self.main.game.castle)
            self.main.game.enemyGroup.update(dt, self.main.FPS)
            self.main.game.archers.update(dt, self.main.FPS)
    
            for projectile in self.main.game.projectileGroup:
                if projectile.rect.x > 1300:
                    projectile.kill()
                projectile.update(dt, self.main.FPS)

            for projectile in self.main.game.enemyProjectileGroup:
                if projectile.rect.x < 700:
                    projectile.kill()
                    self.main.game.castle.takeDamage(projectile.damage)
                projectile.update(dt, self.main.FPS)

            for i in self.main.game.currentHeroes:
                if self.main.game.currentHeroes[i] is not None:
                    self.main.game.currentHeroes[i].update(dt, self.main.FPS, inputs)

            if self.main.game.daffyDuck.abilityInUse:
                ability = daffyAbility(self.main, 999, self.main.game.daffyDuck.arrowImage)
                ability.newState()
                self.main.game.daffyDuck.abilityInUse = False

            collided = pygame.sprite.groupcollide(self.main.game.enemyGroup, self.main.game.bugsBunny.goonGroup, False, False)
            
            for collisions in collided:
                for i in collided[collisions]:
                    i.takeDamage(collisions.stats['currentHealth'])
                    collisions.takeDamage(i.currentDamage)
                    if not collisions.alive:
                        self.main.game.gold += int(collisions.stats['value'] * self.main.game.goldMultiplier)

            collided = pygame.sprite.groupcollide(self.main.game.enemyGroup, self.main.game.projectileGroup, False, True)

            for collisions in collided:
                for i in collided[collisions]:
                    collisions.takeDamage(i.damage)
                    if not collisions.alive:
                        self.main.game.gold += int(collisions.stats['value'] * self.main.game.goldMultiplier)


            if (not self.main.game.castle.alive) or (not self.main.game.enemyGroup and self.main.game.roundComplete):
                for i in self.main.game.currentHeroes:
                    if self.main.game.currentHeroes[i] is not None:
                        self.main.game.currentHeroes[i].reset()

                for i in self.main.game.projectileGroup:
                    i.kill()
                for i in self.main.game.enemyProjectileGroup:
                    i.kill()
                
                self.currentState = 0
                self.main.game.roundComplete = False
                self.main.minigameValue = self.main.game.changeGold(0, False)

                if self.main.game.castle.alive:
                    self.main.game.round += 1
                else:
                    self.main.game.roundComplete = False
                    self.main.survivedRound = False
                    self.main.game.enemyCount = 0
                    for i in self.main.game.enemyGroup:
                        i.kill()
                
                self.main.game.archers.reset()
                self.main.game.castle.reset()


            

        #handles pausing
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()


            

            

    def render(self, screen, inputs) -> None:
        screen.fill((255,255,255))
        screen.blit(self.backgroundImage, (0,0))
        screen.blit(self.castleImage, (250, 320))
        
        self.main.drawText('GOLD: ' + str(self.main.game.getGold()), 10, 10, 30)
        self.main.drawText('HEALTH: ' + str(int(self.main.game.castle.currentHealth)), 10, 40, 30, 'red')
        self.main.drawText('ROUND: ' + str(self.main.game.round), 10, 70, 30, 'black')



        if self.currentState == 0:
            if self.minigameComplete:
                #round start button
                if self.roundStartButton.draw(screen, inputs):
                    self.currentState = 1
                    self.minigameComplete = False
                
                #castle slot buttons
                for index, i in enumerate(self.castleSlotButtons):
                    if i.draw(screen, inputs):
                        nextState = IntermissionMenu(self.main, index+1)
                        nextState.newState()

                #tower button
                if self.towerSlotButton.draw(screen, inputs):
                    nextState = TowerIntermissionMenu(self.main)
                    nextState.newState()

                #upgrade buttons
                if self.upgradeCastleButton.draw(screen, inputs):   
                    if self.main.game.getGold() >= self.main.game.castle.upgradePrice:
                        self.main.game.changeGold(self.main.game.castle.upgradePrice, True)
                        self.main.game.castle.upgrade()

                if self.upgradeArcherButton.draw(screen, inputs):
                    if self.main.game.getGold() >= self.main.game.archers.getUpgradePrice():
                        self.main.game.changeGold(self.main.game.archers.getUpgradePrice(), True)
                        self.main.game.archers.levelUp()

                self.main.drawText('COST: ' + str(self.main.game.castle.upgradePrice), 1000, 110, 15)
                self.main.drawText('LEVEL: ' + str(self.main.game.castle.level), 997, 130, 15, 'black')
                self.main.drawText('COST: ' + str(self.main.game.archers.getUpgradePrice()), 1250, 110, 15)
                self.main.drawText('LEVEL: ' + str(self.main.game.archers.getLevel()), 1247, 130, 15, 'black')

                self.main.game.archers.render(screen)

        else:
            for sprite in self.main.game.enemyGroup: 
                sprite.draw(screen)

            self.main.game.archers.render(screen)

            self.main.game.projectileGroup.draw(screen)

            self.main.game.enemyProjectileGroup.draw(screen)

            if self.main.game.currentTower is not None:
                self.main.game.currentTower.render(screen, 615, 726)

            if self.main.game.currentHeroes[1] is not None:
                if self.castleSlot1Button.draw(screen, inputs, True):
                    self.main.game.currentHeroes[1].useAbility()
                self.main.game.currentHeroes[1].render(screen, 505, 465)

            if self.main.game.currentHeroes[2] is not None:  
                if self.castleSlot2Button.draw(screen, inputs, True):
                    self.main.game.currentHeroes[2].useAbility()
                self.main.game.currentHeroes[2].render(screen, 376, 511)

            if self.main.game.currentHeroes[3] is not None:
                if self.castleSlot3Button.draw(screen, inputs, True):
                    self.main.game.currentHeroes[3].useAbility()
                self.main.game.currentHeroes[3].render(screen, 270, 403)

            if self.main.game.currentHeroes[4] is not None:
                if self.castleSlot4Button.draw(screen, inputs, True):
                    self.main.game.currentHeroes[4].useAbility()
                self.main.game.currentHeroes[4].render(screen, 355, 354)

            


    #loads images required for the main game
    def loadImages(self) -> None:
        #loads assets
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/main game/main background.png')
        self.castleImage = pygame.image.load(os.getcwd() + '/assets/main game/castle.png')
        self.goldTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/gold tower.png')
        self.healthTowerImage = pygame.image.load(os.getcwd() + '/assets/main game/health tower.png')
        self.roundStartImage = pygame.image.load(os.getcwd() + '/assets/main game/start round.png')
        self.roundStartHoverImage = pygame.image.load(os.getcwd() + '/assets/main game/start round hover.png')
        self.castleUpgradeImage = pygame.image.load(os.getcwd() + '/assets/main game/castle upgrade.png')
        self.castleUpgradeHoverImage = pygame.image.load(os.getcwd() + '/assets/main game/castle upgrade hover.png')
        self.archerUpgradeImage = pygame.image.load(os.getcwd() + '/assets/main game/archer upgrade.png')
        self.archerUpgradeHoverImage = pygame.image.load(os.getcwd() + '/assets/main game/archer upgrade hover.png')
        self.emptySlotImage = pygame.image.load(os.getcwd() + '/assets/main game/empty slot.png')
        self.emptySlotHoverImage = pygame.image.load(os.getcwd() + '/assets/main game/empty slot hover.png')

        




        

