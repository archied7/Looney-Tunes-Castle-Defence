import pygame
import sys, os
from classes import gameClass, buttonClass

#set game window
WIDTH = 1440
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Looney Tunes Castle Defence')

icon = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/misc/icon.png")
pygame.display.set_icon(icon)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 30

    running = True

    mainMenuImage = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/main menu/main menu.png")
    mainMenuButtonImage = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/main menu/main menu start.png")
    mainMenuButtonPressedImage = pygame.image.load(os.path.dirname(os.path.dirname(__file__)) + "/assets/main menu/main menu start pressed.png")
    
    #true if main menu is loaded
    mainMenuLoaded = True

    #creating events for states
    MAINGAME = pygame.event.Event(pygame.USEREVENT, attr1 = 'MAINGAME')


    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == MAINGAME:
                screen.fill((0,0,0))
                print('work')

        pygame.display.update()

        if mainMenuLoaded:
            if mainMenu(mainMenuImage, mainMenuButtonImage, mainMenuButtonPressedImage) == 1:
                pygame.event.post(MAINGAME)
                mainMenuLoaded = False

    pygame.quit()


def mainMenu(menuImage, buttonImage, buttonPressedImage, w=WIDTH, h=HEIGHT):

    screen.fill((0,0,0))
    mainMenuImage = pygame.transform.scale(menuImage, (w, h))
    screen.blit(mainMenuImage, (0,0))

    mainMenuButton = buttonClass.Button(600,750, buttonImage, 0.8, buttonPressedImage)

    if mainMenuButton.draw(screen) == 1:
        return 1
    

if __name__ == "__main__":
    main()
    

