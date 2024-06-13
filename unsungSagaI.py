import pygame, os, random
from sys import exit

# Initialize Pygame
pygame.init()
pygame.display.set_caption("UnSung Saga: I")
clock = pygame.time.Clock()

# Get display info after initializing Pygame
display_info = pygame.display.Info()
max_width = display_info.current_w
max_height = display_info.current_h

# Set up the screen
screen = pygame.display.set_mode((max_width, max_height))
pygame.mouse.set_visible(False)

# Function to load and scale images from a specified folder
def loadImages(folderPath, imageSize):
    image_files = [imageFile for imageFile in os.listdir(folderPath) if imageFile.lower().endswith('.png')]
    images = []
    for imageFile in image_files:
        image_path = os.path.join(folderPath, imageFile)
        image = pygame.image.load(image_path).convert_alpha()
        image = pygame.transform.scale(image, imageSize)
        images.append(image)
    return images

# Load and resize gun crosshair image
gunCross = pygame.image.load('images/cross.png').convert_alpha()
gunCross = pygame.transform.scale(gunCross, (20, 20))

# Load and resize background image
background = pygame.image.load('images/backgroundRoad.jpg').convert()
backgroundImage = pygame.transform.scale(background, (max_width, max_height))

def main():
    introOutro('images/intro', 0)
    introText()
    gameloop()


def introText():
    textIndex = 0
    texts = ["Hey Hero!", "Apocalypse has Hit your city!"]
    text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text_surface = text_font.render(texts[textIndex], False, "Black")

    images = loadImages('images/textBackground', (max_width, max_height))
    bubble = pygame.image.load('images/textBubble.png').convert_alpha()
    bubble = pygame.transform.scale(bubble, (max_width / 2, max_height / 2))

    index = 0
    slowdownRate = 0
    appearingText = 0
    while True:
        text_surface = text_font.render(texts[textIndex][:appearingText], False, "White")
        if appearingText != len(texts[textIndex]):
            appearingText += 1
        if index < (len(images) - 1):
            slowdownRate += 0.02
            index += int(slowdownRate);
        else:
            slowdownRate = 0
            index = 0

        screen.blit(images[index], (0,0))
        # screen.blit(bubble, (max_width/ 5, max_height / 5))
        screen.blit(text_surface, (max_width / 2 - 7 * len(texts[textIndex]), max_height / 4))
        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if textIndex < len(texts) - 1:
                        textIndex += 1
                    elif textIndex == len(texts) - 1:
                        return
                    appearingText = 0

def introOutro(folderPath, number):
    # Text configuration
    text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    text = "Press Enter to Play" if number == 0 else "You are the Unsung hero of this city"
    text_surface = text_font.render(text, False, 'White')

    Images = loadImages(folderPath, (max_width, max_height))
    Index = 0
    while True:
        screen.blit(Images[Index], (0, 0))
        screen.blit(text_surface, (max_width / 2 - 7 * len(text), max_height / 4))
        pygame.display.flip()
        clock.tick(10)
        
        Index = (Index + 1) % len(Images)  # Loop through images

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    if event.key == pygame.K_RETURN and number == 0:
                        return
                    pygame.quit()
                    exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def gameloop():
    heart = 3
    spawnTotal = 10

    # to slow down animation:
    shoot = 0
    fly = 0
    crawl = 0

    # Gun configuration
    shoot = False
    currentImageIndex = 0
    gunImages = loadImages('images/handgun', (250, 250))
    
    # Bat configuration
    scaleBat = 20
    batImages = loadImages('images/batHorizontal', (scaleBat, scaleBat))
    batIndex = 0
    batShot = 0
    x, y = random.randint(20, max_width - int(max_width / 5)), random.randint(20, max_height - int(max_height / 4))

    # Zombie configuration
    scaleZombie = 50
    zombieImages = loadImages('images/zombie', (scaleZombie, scaleZombie))
    zombieIndex = 0
    zombieShot = 0
    zombieX, zombieY = random.randint(570, 700), 480

    # Fonts and animations
    text_font = pygame.font.Font('font/Pixeltype.ttf', 30)
    batAnimation = {}
    zombieAnimation = {}

    while True:
        mouse_pos = pygame.mouse.get_pos()

        gunCrossRect = gunCross.get_rect(center=mouse_pos)

        # Update zombie image
        zombieRect = zombieImages[zombieIndex].get_rect(midbottom = (zombieX, zombieY))
        zombieImage = pygame.transform.scale(zombieImages[zombieIndex], (scaleZombie, scaleZombie))
        if zombieIndex < len(zombieImages) - 1:
            crawl += 0.3
            zombieIndex = int(crawl)
        else:
            zombieIndex = 0
            crawl = 0
        zombieY += 0.1


        # Update bat image
        batImage = pygame.transform.scale(batImages[batIndex], (scaleBat, scaleBat))
        if batIndex < len(batImages) - 1:
            fly += 0.4
            batIndex = int(fly)
        else:
            batIndex = 0
            fly = 0

        if int(scaleBat) >= 100:
            lose()

        # Rendering the screen
        screen.blit(backgroundImage, (0, 0))
        screen.blit(gunCross, gunCrossRect)
        screen.blit(batImage, (x, y))
        screen.blit(zombieImage, (zombieX, zombieY))

        KilledText = f"Bat Killed: {batShot}"
        KilledSurface = text_font.render(KilledText, False, 'White')
        screen.blit(KilledSurface, (max_width - 10 * len(KilledText), 50))

        KilledText = f"Zombie Killed: {zombieShot}"
        KilledSurface = text_font.render(KilledText, False, 'White')
        screen.blit(KilledSurface, (max_width - 10 * len(KilledText), 30))

        KilledText = f"Left: {spawnTotal - zombieShot - batShot}"
        KilledSurface = text_font.render(KilledText, False, 'White')
        screen.blit(KilledSurface, (max_width - 10 * len(KilledText), 10))

        if (spawnTotal == (zombieShot + batShot)):
            introOutro('images/outro', 1)
        for value in list(batAnimation.keys()):
            screen.blit(pygame.transform.scale(pygame.transform.flip(batImages[3], False, True), (batAnimation[value][1], batAnimation[value][1])), (value, batAnimation[value][0]))
            if batAnimation[value][0] > max_height * 0.75:
                del batAnimation[value]
            else:
                batAnimation[value][0] += 5

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                introOutro('images/outro', 1)
            if event.type == pygame.MOUSEBUTTONUP:
                shoot = True
                if batImage.get_rect(topleft=(x, y)).collidepoint(mouse_pos):
                    batShot += 1
                    batAnimation[x] = [y, scaleBat]
                    scaleBat = 20
                    x, y = random.randint(20, max_width - int(max_width / 5)), random.randint(20, max_height - int(max_height / 4))
                if zombieImage.get_rect(topleft=(zombieX, zombieY)).collidepoint(mouse_pos):
                    zombieShot += 1
                    zombieAnimation[zombieX] = [zombieY, scaleZombie]
                    scaleZombie = 30
                    zombieX, zombieY = random.randint(570, 700), 480
            # if pygame.mouse.get_pressed()[0]:
            #     shoot = True
        
        if shoot:
            if currentImageIndex < len(gunImages) - 1:
                shoot += 0.4
                currentImageIndex = int(shoot)
            else:
                currentImageIndex = 0
                shoot = 0
            screen.blit(gunImages[currentImageIndex], (mouse_pos[0] - 110, max_height - 250))

        scaleBat += random.random()
        scaleZombie += random.random()

        pygame.display.flip()
        clock.tick(24)

def lose():
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()
