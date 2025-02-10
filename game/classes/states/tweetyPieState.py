from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.buttonClass import Button
from classes.states.pauseState import Pause
import pygame
import os
import random

class TweetyPie(State):
    def __init__(self, main: object) -> None:
        #initialise parent class
        State.__init__(self, main)

        #create exit button
        self.exitButton = Button(538, 660, self.main.exitImage, 2.5, self.main.exitHoverImage)

        #set game variables
        self.passPipe = False
        self.scrollSpeed = 14
        self.alive = True
        self.groundScroll = 0
        self.pipeFreq = 1000
        self.lastPipe = pygame.time.get_ticks() - self.pipeFreq
        self.score = 0
        self.counter = 0
        self.result = False
        self.goldAdded = False
        self.currentTickDifference = 0

        #calculate the amount of pipes in the game
        if self.main.game.round <= 20:
            if self.main.game.round == 1:
                self.pipeTotal = 1
            else:
                self.pipeTotal = self.main.game.round - 1
        else:
            self.pipeTotal = 20

        #create objects and sprite group
        self.tweety = Tweety(200, ((self.main.HEIGHT / 2) - 100 ))
        self.pipeGroup = pygame.sprite.Group()

    def update(self, dt: float, inputs: dict) -> None:
        pygame.display.update()

        #check if the game has been completed
        if self.score >= self.pipeTotal:
            self.alive = False
            self.result = True

        #check if tweety pie has died and update
        if self.tweety.update(dt, inputs, self.main.FPS) == 1:
            self.alive = False

        if self.alive and self.main.game.paused == False:
            #during minigame being played
            if self.tweety.flying:
                timeNow = pygame.time.get_ticks()
                self.pipeGroup.update(dt, self.main.FPS, self.scrollSpeed)

                #checks for passing the pipes
                if len(self.pipeGroup) > 0:
                    if self.tweety.rect.left > self.pipeGroup.sprites()[0].rect.left\
                        and self.tweety.rect.right < self.pipeGroup.sprites()[0].rect.right\
                        and self.passPipe == False:
                            self.passPipe = True

                    if self.passPipe:
                        if self.tweety.rect.left > self.pipeGroup.sprites()[0].rect.right:
                            self.score += 1
                            self.passPipe = False

                #checks for collisions
                if pygame.sprite.spritecollideany(self.tweety, self.pipeGroup):
                    self.tweety.flying = False
                    self.alive = False

                #generates pipes
                if timeNow - self.lastPipe > self.pipeFreq and self.counter < self.pipeTotal:
                    height = random.randint(-175,150)

                    bottomPipe = Pipe(self.main.WIDTH, self.main.HEIGHT/2 + height, 0, self.pipeImage)
                    topPipe = Pipe(self.main.WIDTH, self.main.HEIGHT/2 + height, 1, self.pipeImage)
                    self.pipeGroup.add(bottomPipe)
                    self.pipeGroup.add(topPipe)
                    self.lastPipe = pygame.time.get_ticks()
                    self.counter += 1

                #scrolls the ground
                self.groundScroll -= self.scrollSpeed * self.main.FPS * dt
                if abs(self.groundScroll) > 35:
                    self.groundScroll = 0

        #handles ticks when game ispaused
        elif self.main.game.paused:
                self.lastPipe = pygame.time.get_ticks() - self.currentTickDifference
                self.main.game.changePause()

        #handles if the game was successful, as well as adding rewards
        else:
            if self.result:
                if self.goldAdded == False:
                    self.main.minigameValue = self.main.game.changeGold(self.main.minigameValue, False)
                    self.goldAdded = True


    def render(self, screen: pygame.Surface, inputs: dict) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))

        self.tweety.render(screen)
        self.pipeGroup.draw(screen)
        
        screen.blit(self.groundImage, (self.groundScroll,800))
        self.main.drawText(str(self.score), 10, 10, 60)

        if self.tweety.flying == False and self.alive:
            screen.blit(self.tutorialImage, (self.main.WIDTH/2 - self.tutorialImage.get_width()/2, self.main.HEIGHT/2
                                              - self.tutorialImage.get_height()/2))

        #handles pausing
        if inputs['escape'] == True:
            nextState = Pause(self.main)
            self.currentTickDifference = pygame.time.get_ticks() - self.lastPipe
            nextState.newState()

        #draws button if game is over
        if self.alive == False:
            if self.exitButton.draw(screen, inputs) == 1:
                self.leaveState()

    def loadImages(self) -> None:
        #loads images needed for game
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/tweety pie background.png')
        self.groundImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/ground.png')
        self.pipeImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/pipe.png')
        self.tutorialImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/tweety tutorial.png')
        self.tutorialImage = pygame.transform.scale_by(self.tutorialImage, 2.5)

class Tweety():
    def __init__(self, x: int, y: int) -> None:
        self.loadSprites()
        self.currentFrameNum = 1

        #create current rect
        self.rect = self.tweetyFrames[self.currentFrameNum%2].get_rect()
        self.rect.center = ((x,y))

        self.lastUpdate = 0
        self.velocity = 0
        self._flying = False

        #set current image
        self.currentFrame = self.tweetyFrames[0]

    def update(self, dt: float, inputs: dict, fps: int) -> int:
        if self._flying:
            self.animate(dt)

            #increase the speed of the bird
            self.velocity += 2 * dt * fps
            if self.velocity > 20 * dt * fps:
                self.velocity = 20 * dt * fps

        if self.rect.y < 720:
            #move the bird up and down
            self.rect.y += self.velocity
        else:
            #if the bird hit the ground
            self._flying = False
            return 1

        if self.rect.y < -250:
            #if the bird if too far above the screen
            self._flying = False
            return 1

        if inputs['click'] == True:
            #starts the game
            if self._flying == False:
                self._flying = True

            #moves the bird up
            self.velocity = -20 * dt * fps
            
    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.currentFrame, (self.rect.x, self.rect.y))

    def animate(self, dt: float) -> None:
        self.lastUpdate += dt

        if self.lastUpdate > 0.15:
            self.lastUpdate = 0
            self.currentFrameNum += 1
            self.currentFrame = self.tweetyFrames[(self.currentFrameNum % 2)]

    def loadSprites(self) -> None:
        #loads sprites
        tweetyPieSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/tweety pie.png')
        tweetyPieSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/tweety pie meta.json'), tweetyPieSpriteSheet, True)
        self.tweetyFrames = tweetyPieSpritesObject.getSpritesList()

    @property
    def flying(self) -> bool:
        return self._flying
    
    @flying.setter
    def flying(self, val: bool) -> None:
        self._flying = val

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, orientation: int, image: pygame.Surface) -> None:
        """
        orientation = 0 is from top
        orientation = 1 is from bottom
        """

        pygame.sprite.Sprite.__init__(self)

        #sets current rect
        self.image = image
        self.rect = self.image.get_rect()

        self.gapLength = 250

        #places the pipe's initial position
        if orientation == 0:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = ((x,y - self.gapLength / 2))

        if orientation == 1:
            self.rect.topleft = ((x,y + self.gapLength / 2))

    def update(self, dt: float, fps: int, scrollSpeed:int) -> None:
        #moves the pipe to the left
        self.rect.x -= scrollSpeed * dt * fps
        if self.rect.right < 0:
            self.kill()



        