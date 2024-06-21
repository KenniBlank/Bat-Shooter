import pygame, os, random, time
from gameClasses import Gun, Bat, Background     


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
        screen,
        max_width,
        max_height
    )

    # Font
    font_size = 30
    text_font = pygame.font.Font('font/Pixeltype.ttf', font_size)

    # Intro 
    while True:
        everythingBackground.draw(0)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                everythingBackground.textsIntroIndex += 1

        if everythingBackground.draw(0):
            # Gun.intro = False
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
        everythingBackground.draw(1)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                everythingBackground.textsIntroIndex += 1

        if everythingBackground.draw(0):
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