import pygame, os, random
from gameClasses import Gun

class Bat(pygame.sprite.Sprite):
    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h
    tmp = 0

    def __init__(self, listOfBatImages, scale, screen):
        super().__init__()
        self.batImages = listOfBatImages
        self.scale = scale 
        self.screen = screen

        self.batImageIndex = 0
        self.spawnX = Bat.max_width / 2
        self.spawnY = Bat.max_height / 2
        self.spawn()

    def hitTest(self, gunCross, gunCrossX, gunCrossY):
        scaled_bat_image = pygame.transform.scale(self.batImages[self.batImageIndex], (self.scale, self.scale))
        bat_rect = scaled_bat_image.get_rect(topleft=(self.spawnX, self.spawnY))
        gunCross_rect = gunCross.get_rect(topleft=(gunCrossX, gunCrossY))
        
        return bat_rect.colliderect(gunCross_rect)
    
    def update(self):
        self.batdraw()

    def spawn(self):
        self.spawnX = random.randint(10, Bat.max_width - 50)
        self.spawnY = random.randint(10, Bat.max_height - Bat.max_height / 3)
        self.scale = 40
    
    def batdraw(self):
        Bat.tmp += (random.randint(1, 6) / 10)
        self.scale += (random.randint(1, 5) / 10)
        self.batImageIndex = int(Bat.tmp) 
        self.screen.blit(pygame.transform.scale(self.batImages[self.batImageIndex], (self.scale, self.scale)), (self.spawnX, self.spawnY))
        if self.batImageIndex >= len(self.batImages) - 1:
            self.batImageIndex = 0
            Bat.tmp = 0

    def downfall(self):
        self.batImageIndex = len(self.batImages) - 1
        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.batImages[self.batImageIndex], (self.scale, self.scale)), False, True), (self.spawnX, self.spawnY))
        self.spawnY += 9
        if self.spawnY >= Bat.max_height:
            # health
            self.spawn()

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
    
    bat = Bat(loadImages('images/batHorizontal', (20, 20)), 20, screen)

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
                if bat.hitTest(gun.gunCrossImage, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    GameScore += 1
                    gun.maxBullet += 1;
                    bat.spawn()
                gun.update(True)
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:
                    if gun.bulletInGun < 12:
                        bulletReloadedAmount = 12
                        if gun.gunReload():
                            gun.update(12, bulletReloadedAmount)

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