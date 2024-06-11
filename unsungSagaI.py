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

# using os library to import all of images from specified path
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

# Load and resize background image using PIL
background = pygame.image.load('images/background.jpeg').convert()
backgroundImage = pygame.transform.scale(background, (max_width, max_height))

def main():
    start()
    gameloop()

def start():
    introOutro('images/intro', 0)   


def introOutro(folderPath , number):
    # text
    text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
    if number == 0:
        text = "Press Enter to Play"
    else:
        text = "You are the Unsung hero of this city"
    
    text_surface = text_font.render(text,False, 'White')

    Images = loadImages(folderPath, (max_width, max_height))
    Index = 0
    while True:
        if Index < len(Images) - 1:
            Index += 1
        else:
            Index = 0
        screen.blit(Images[Index], (0,0))
        screen.blit(text_surface, (max_width / 2 - 7 * len(text), max_height / 4))
        pygame.display.flip()
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_RETURN and number == 1):
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RETURN and number == 0:
                    return

            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        


def gameloop():
    shoot = False
    currentImageIndex = 0
    gunImages = loadImages('images/gun', (250, 250))
    scaleBat = 20
    batImages = loadImages('images/batHorizontal', (scaleBat, scaleBat))

    # Random class for spawning of the bats:
    x = random.randint(20, max_width - 20)
    y = random.randint(20, max_height - 300)
    batIndex = 0
    batShot = 0

    text_font = pygame.font.Font('font/Pixeltype.ttf', 30)
    foranimation = {}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        gunCrossRect = gunCross.get_rect(center=(mouse_pos[0], mouse_pos[1]))

        # Scaling the bat
        tempBatImage = pygame.transform.scale(batImages[batIndex], (scaleBat, scaleBat))
        if int(scaleBat) == 100:
            lose()
        if batIndex < len(batImages) - 1:
            batIndex += 1
        else:
            batIndex = 0

        batKilled = f"BatKilled: {batShot}"
        text_surface = text_font.render(batKilled, False, 'White')
        screen.blit(backgroundImage, (0, 0))
        screen.blit(gunCross, gunCrossRect)
        screen.blit(tempBatImage, (x, y));
        screen.blit(text_surface, (max_width - 15 * len(batKilled), 50))
        for value in list(foranimation):
            
            screen.blit(pygame.transform.scale(pygame.transform.flip(batImages[3], False, True), (foranimation[value][1],foranimation[value][1])), (value, foranimation[value][0]))
            if (foranimation[value][0] > (max_height * 0.75)):
                pass
            else:
                foranimation[value][0] += 5


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    introOutro('images/outro', 1)
                    exit()
            if event.type == pygame.MOUSEBUTTONUP:

                shoot = True
                bat_rect = tempBatImage.get_rect(topleft=(x, y))

                if bat_rect.collidepoint(mouse_pos):
                    batShot += 1
                    tempX = x
                    tempY = y
                    foranimation[x] = [y, scaleBat];
                    scaleBat = 20

                    x = random.randint(20, max_width - 20)
                    y = random.randint(20, max_height - 300)
        
        if shoot:
            currentImageIndex += 1
            if currentImageIndex >= len(gunImages):
                shoot = False
                currentImageIndex = 0

        scaleBat += random.random()

        # magic numbers for the gun image dont change 
        screen.blit(gunImages[currentImageIndex], (mouse_pos[0] - 110, max_height - 250))

        pygame.display.flip()
        clock.tick(24)


def lose():
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()