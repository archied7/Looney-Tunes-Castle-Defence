from classes.states.stateClass import State
from classes.spriteLoader import SpriteLoader
from classes.buttonClass import Button
from classes.states.pauseState import Pause
import pygame
import os
import random

class TweetyPie(State):
    def __init__(self, main) -> None:
        State.__init__(self, main)
        self.exitButton = Button(538, 660, self.main.exitImage, 2.5, self.main.exitHoverImage)

        #set game variables
        self.passPipe = False
        self.scrollSpeed = 4
        self.alive = True
        self.groundScroll = 0
        self.pipeFreq = 3000
        self.lastPipe = pygame.time.get_ticks() - self.pipeFreq
        self.score = 0
        self.counter = 0

        self.tweety = Tweety(200, ((self.main.HEIGHT / 2) - 100 ))
        self.pipeGroup = pygame.sprite.Group()

    def update(self, dt, inputs) -> None:
        pygame.display.update()

        if self.score >= 5:
            self.alive = False

        if self.tweety.update(dt, inputs, self.main.FPS) == 1:
            self.alive = False

        if self.alive:
            if self.tweety.getFlying():
                #generates pipes
                timeNow = pygame.time.get_ticks()
                self.pipeGroup.update(dt, self.main.FPS, self.scrollSpeed)

                if len(self.pipeGroup) > 0:
                    if self.tweety.rect.left > self.pipeGroup.sprites()[0].rect.left\
                        and self.tweety.rect.right < self.pipeGroup.sprites()[0].rect.right\
                        and self.passPipe == False:
                            self.passPipe = True

                    if self.passPipe:
                        if self.tweety.rect.left > self.pipeGroup.sprites()[0].rect.right:
                            self.score += 1
                            self.passPipe = False

                if pygame.sprite.spritecollideany(self.tweety, self.pipeGroup):
                    self.alive = False

                if timeNow - self.lastPipe > self.pipeFreq and self.counter < 5:
                    height = random.randint(-100,100)

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

    def render(self, screen, inputs) -> None:
        screen.fill((0,0,0))
        screen.blit(self.backgroundImage, (0,0))
        self.tweety.render(screen)
        self.pipeGroup.draw(screen)
        screen.blit(self.groundImage, (self.groundScroll,800))
        self.drawText(str(self.score), 10, 10, screen)

        if inputs['escape'] == True:
            nextState = Pause(self.main)
            nextState.newState()

        #draws button if game is over
        if self.alive == False:
            if self.exitButton.draw(screen, inputs) == 1:
                self.leaveState()

    def loadImages(self) -> None:
        self.backgroundImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/tweety pie background.png')
        self.groundImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/ground.png')
        self.pipeImage = pygame.image.load(os.getcwd() + '/assets/tweety pie minigame/pipe.png')

    def drawText(self, text, x, y, screen):
        image = pygame.font.Font(os.getcwd() + '/assets/misc/font.ttf', 60).render(text, True, (255, 215, 0))
        screen.blit(image, (x,y))

class Tweety():
    def __init__(self, x, y):
        self.loadSprites()
        self.currentFrameNum = 1

        self.rect = self.tweetyFrames[self.currentFrameNum%2].get_rect()
        self.rect.center = ((x,y))

        self.lastUpdate = 0
        self.velocity = 0
        self.flying = False

        self.currentFrame = self.tweetyFrames[0]

    def update(self, dt, inputs, fps):
        if self.flying:
            self.animate(dt)
            self.velocity += 2 * dt * fps
            if self.velocity > 20 * dt * fps:
                self.velocity = 20 * dt * fps

        if self.rect.y < 720:
            self.rect.y += self.velocity
        else:
            self.flying = False
            return 1

        if inputs['click'] == True:
            if self.flying == False:
                self.flying = True

            self.velocity = -20 * dt * fps
            
    def render(self, screen):
        screen.blit(self.currentFrame, (self.rect.x, self.rect.y))

    def animate(self, dt):
        self.lastUpdate += dt

        if self.lastUpdate > 0.15:
            self.lastUpdate = 0
            self.currentFrameNum += 1
            self.currentFrame = self.tweetyFrames[(self.currentFrameNum % 2)]

    def loadSprites(self):
        self.tweetyPieSpriteSheet = pygame.image.load(os.getcwd() + '/assets/characters/tweety pie.png')
        tweetyPieSpritesObject = SpriteLoader((os.getcwd() + '/assets/characters/tweety pie meta.json'), self.tweetyPieSpriteSheet)
        self.tweetySprites = tweetyPieSpritesObject.getSprites()

        self.tweetyFrames = []
        for i in self.tweetySprites:
            self.tweetyFrames.append(self.tweetySprites[i])

    def getFlying(self):
        return self.flying

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, orientation, image):
        """
        orientation = 0 is from top
        orientation = 1 is from bottom
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.gapLength = 250

        if orientation == 0:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = ((x,y - self.gapLength / 2))

        if orientation == 1:
            self.rect.topleft = ((x,y + self.gapLength / 2))

    def update(self, dt, fps, scrollSpeed):
        self.rect.x -= scrollSpeed * dt * fps
        if self.rect.right < 0:
            self.kill()



        