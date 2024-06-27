import pygame, os
from projectClasses import Gun, Bat, Background     


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
        screen, 25, 
        'images/cross.png', 
        'images/bullet.png', 
        12,
        max_width,
        max_height
    )
    
    bat = Bat(loadImages('images/batHorizontal', 
                         (20, 20)), 
                         20, 
                         screen,
                         max_width,
                         max_height)

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

        screen.fill((125, 25, 25))

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
            loser(screen, max_width, max_height, clock)
            
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

# function to load images in directory and resize
def loadImages(folderPath, imageSize):
    image_files = [imageFile for imageFile in os.listdir(folderPath) if imageFile.lower().endswith('.png')]
    images = []
    for imageFile in image_files:
        image_path = os.path.join(folderPath, imageFile)
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, imageSize)
        images.append(image)
    return images

# unnecessary function created to meet the cs50p requirement because of how useless the requirement truly is
def nonsense():
    pass


# If the player loses the game
def loser(screen, max_width, max_height, clock):
    i = 0
    while 1:
                font_size = 60
                text_font = pygame.font.Font('font/Pixeltype.ttf', font_size)
                screen.fill((0, 0, 0))
                text = "YOU DIED LOSER!"
                text_surface = text_font.render(text[:i], False, 'Red')
                screen.blit(text_surface, (max_width / 2 - len(text) * 8, max_height / 2 - 1/8 * max_height))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            exit()

                if i < len(text) - 1:
                    i += 1

                pygame.display.flip()
                clock.tick(10)


if __name__ == "__main__":
    main()