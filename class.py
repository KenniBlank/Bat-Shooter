import pygame, os
from gameClasses import Gun

class Bat(pygame.sprite.Sprite):
    def __init__(self, listOfBatImages, scale, screen):
        super().__init__()
        self.batImages = listOfBatImages
        self.scale = scale # Is a tupple of X, Y so change accordingly
        self.screen = screen

        self.batImageIndex = 0
        self.spawnX = 40
        self.spawnY = 40

    def hitTest(self):
        pass

    def update(self):
        self.draw()

    def spawn(self):
        pass

    def sound(self):
        pass

    def shot(self):
        pass

    def draw(self):
        self.batImageIndex += 1
        self.screen.blit(self.batImages[self.batImageIndex], (self.spawnX, self.spawnY))
        if self.batImageIndex >= len(self.batImages) - 1:
            self.batImageIndex = 0
        self.spawnX += 1
        self.spawnY += 1
        

class Background():
    intro = True
    def __init__(self, introImages, outroImages, screen):
        self.listOfIntroImages = introImages
        self.listOfOutroImages = outroImages
        self.screen = screen

        self.introIndex = 0
        self.outroIndex = 0

    def update(self):
        if Background.intro == True:
            # 0 for intro
            self.draw(0)
        else:
            # 1 for outro
            self.draw(1)

    def draw(self, num):
        if num == 0:
            self.introIndex += 1
            self.screen.blit(self.listOfIntroImages[self.introIndex], (0, 0))
            if self.introIndex >= len(self.listOfIntroImages) - 1:
                self.introIndex = 0
        else:
            self.outroIndex += 1
            self.screen.blit(self.listOfOutroImages[self.outroIndex], (0, 0))
            if self.outroIndex >= len(self.listOfOutroImages) - 1:
                self.outroIndex = 0

class Scene():
    pass


def main():
    pygame.init()
    clock = pygame.time.Clock()

    GameScore = 0

    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h

    screen = pygame.display.set_mode((max_width, max_height))
    pygame.mouse.set_visible(False)

    gun = Gun(
        10, loadImages('images/handGun', (200, 250)), 
        screen, 25, 'images/cross.png', 'images/bullet.png', 12
    )
    
    bat = Bat(loadImages('images/batVertical', (20, 20)), (20, 20), screen)

    everythingBackground = Background(
        loadImages('images/intro', (max_width, max_height)),
        loadImages('images/outro', (max_width, max_height)),
        screen
    )
    # Intro 
    while True:
        exitLoop = False
        everythingBackground.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                exitLoop = True

        if exitLoop == True:
            Gun.intro = False
            break

        pygame.display.flip()
        clock.tick(24)
    

    # Game
    while True:
        GameState = True
        screen.fill((125, 25, 25))
        # everythingBackground.update()
        bat.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                gun.bulletShot(gun.bulletInGun)
                gun.update(True)
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:
                    if gun.bulletInGun < 6:
                        bulletReloadedAmount = 6
                        if gun.gunReload():
                            gun.update(6, bulletReloadedAmount)

        if GameState == False:
            break
        gun.update()
        pygame.display.flip()
        clock.tick(24)
    
    # Outro
    while True:
        exitLoop = False
        everythingBackground.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                exitLoop = True
        if exitLoop == True:
            Gun.intro = False
            break
        pygame.display.flip()
        clock.tick(24)

def loadImages(folderPath, imageSize):
    image_files = [imageFile for imageFile in os.listdir(folderPath) if imageFile.lower().endswith('.png')]
    images = []
    for imageFile in image_files:
        image_path = os.path.join(folderPath, imageFile)
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, imageSize)
        images.append(image)
    return images

if __name__ == "__main__":
    main()