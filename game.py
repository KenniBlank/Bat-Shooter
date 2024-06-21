import pygame, os, random, time
from gameClasses import Gun, Bat
 

class Background():
    intro = True
    def __init__(self, introImages, outroImages, screen):
        self.listOfIntroImages = introImages
        self.listOfOutroImages = outroImages
        self.screen = screen
        
        self.textsIntro = ["Hey Hero!",
             "Apocalypse Has Hit Your City!", 
             "Zombies And Bats Have OverRun Your City", 
             "The City Needs You", 
             "Start By Getting Used To Your Pistol"]
        
        self.textsOutro = ["You have saved the city for the night!",
                           "You are the Unsung Hero of this city.",
                           "You protect from dark, hide your identiy, no help all for this city",
                           "GoodNight Hero!",
                           "Enter to Exit",
                           ]
        self.textsIntroIndex = 0
        self.textsOutroIndex = 0

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
            if self.textsIntroIndex >= len(self.textsIntro):
                return True
            
            return False

        else:
            self.outroIndex += 1
            self.screen.blit(self.listOfOutroImages[self.outroIndex], (0, 0))
            if self.outroIndex >= len(self.listOfOutroImages) - 1:
                self.outroIndex = 0
        
        


def main():
    pygame.init()
    clock = pygame.time.Clock()

    GameScore = 0
    GameState = True

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

    # Font
    font_size = 30
    text_font = pygame.font.Font('font/Pixeltype.ttf', font_size)

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
        clock.tick(10)

    # Game
    while True:
        if Bat.batShot >= 12:
            GameState = False

        # GameState = True
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
                    bat.spawn()
                    Bat.batShot += 1
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

        text = f"You have shot {Bat.batShot} monsters"
        text_surface = text_font.render(text, False, 'White')
        screen.blit(text_surface, (len(text), font_size))

        pygame.display.flip()
        clock.tick(24)
    

    Background.intro = False
    text = f"You have shot {Bat.batShot} monsters"

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
        clock.tick(10)

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