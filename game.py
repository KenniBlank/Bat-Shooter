import pygame, os
from gameClasses import Gun, Bat, Background     


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Bat Shooter')

    GameScore = 0
    GameState = True

    max_width = 1366
    max_height = 766

    screen = pygame.display.set_mode((max_width, max_height))
    pygame.mouse.set_visible(False)

    gun = Gun(
        12, loadImages('images/handGun', (200, 250)), 
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
    everythingBackground.draw(0)


    # Game
    while True:
        if Bat.batShot >= 12:
            GameState = False

        # GameState = True
        screen.fill((125, 25, 25))

        # everythingBackground.update()
        extWhenLoss = bat.update()
        gun.update()
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
                if event.key == pygame.K_r:
                    if gun.bulletInGun < 12:
                        if gun.gunReload():
                            gun.update()
                            Gun.timeDelayGun = 24 * 1

        if extWhenLoss:
            while 1:
                font_size = 60
                text_font = pygame.font.Font('font/Pixeltype.ttf', font_size)
                screen.fill((0, 0, 0))
                text = "YOU DIED LOSER!"
                text_surface = text_font.render(text, False, 'Red')
                screen.blit(text_surface, (max_width / 2 - len(text) * 8, max_height / 2 - 1/8 * max_height))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            exit()
                pygame.display.flip()
                clock.tick(1)

        if not GameState:
            break
        text = f"You have shot {Bat.batShot} monsters"
        text_surface = text_font.render(text, False, 'White')
        screen.blit(text_surface, (len(text), font_size))

        pygame.display.flip()
        clock.tick(24)
    

    Background.intro = False
    text = f"You have shot {Bat.batShot} monsters"

    # Outro
    everythingBackground.draw(1)

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