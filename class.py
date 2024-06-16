import pygame, os

class Gun(pygame.sprite.Sprite):
    pygame.init()
    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h
    gunX = 0
    gunY = 0
    kills = 0

    def __init__(self, bullet, listOfImages, screen, delay = 50, filePathForCross = "images/cross.png", filePathForBullet = "images/bullet.png", maxBullet = 12):
        super().__init__()
        self.listOfImages = listOfImages
        self.image = listOfImages[0]
        self.screen = screen
        self.rect = self.image.get_rect(midbottom=(Gun.gunX, Gun.gunY))
        self.gunImageIndex = 0
        self.shotFired = False
        self.bulletLeft = bullet
        self.delay = delay
        self.gunYTemp = Gun.max_height
        self.gunCrossImage = pygame.transform.scale(pygame.image.load(filePathForCross).convert_alpha(), (30, 30))
        self.bullet = pygame.transform.scale(pygame.image.load(filePathForBullet).convert_alpha(), (40, 40))
        self.maxBullet = maxBullet
    
    def update(self, shotFired = False, bullet = 0):
        Gun.gunX = pygame.mouse.get_pos()[0]
        Gun.gunY = pygame.mouse.get_pos()[1]

        if shotFired:
            self.shotFired = shotFired
        self.draw()
        if bullet > 0:
            self.updateBulletCount(bullet)
    
    def updateBulletCount(self, numberOfBullets):
        self.bulletLeft = numberOfBullets
    
    def draw(self):
        self.bulletRemaining()
        self.gunCross()
        if self.bulletLeft == 0: 
            self.gunReload()
        else:
            self.gunAnimation()
        
    def gunAnimation(self):
        # Check and change hand for gun
        if Gun.gunX > ((Gun.max_width / 2) + 50):
            self.rect = self.image.get_rect(midbottom = (Gun.gunX + 30, self.gunYTemp))
            tmpImage = pygame.transform.flip(self.image, False, False)
            tmpImage = pygame.transform.rotate(tmpImage, -25)
        elif Gun.gunX < ((Gun.max_width / 2) - 50):
            self.rect = self.image.get_rect(midbottom = (Gun.gunX - 60, self.gunYTemp))
            tmpImage = pygame.transform.flip(self.image, True, False)
            tmpImage = pygame.transform.rotate(tmpImage, 25)
        else:
            self.rect = self.image.get_rect(midbottom = (Gun.gunX, self.gunYTemp))
            tmpImage = pygame.transform.flip(self.image, False, False)
        
        # if shotfired what to do.
        if self.shotFired == True and self.bulletLeft > 0:
            pygame.time.delay(self.delay)
            self.screen.blit(tmpImage, self.rect.topleft)
            self.gunImageIndex += 1
            if self.gunImageIndex >= len(self.listOfImages):
                self.gunImageIndex = 0
                self.shotFired = False
                self.bulletLeft -= 1
            self.image = self.listOfImages[self.gunImageIndex]
        else:
            self.screen.blit(tmpImage, self.rect.topleft)

    def gunCross(self):
        self.screen.blit(self.gunCrossImage, (Gun.gunX, Gun.gunY))

    def bulletRemaining(self):
        if self.bulletLeft <= 12:
            for i in range(int(self.bulletLeft)):
                self.screen.blit(self.bullet, (Gun.max_width - 90 - 20 * i, 30))
        else:
            font = pygame.font.Font('font/Pixeltype.ttf', 32)
            text = f"Bullet Left: {self.bulletLeft} X "
            textSurface = font.render(text, False, 'Black')
            self.screen.blit(textSurface, (Gun.max_width - 10 * len(text) - 60, 45))
            self.screen.blit(self.bullet, (Gun.max_width - 90, 30)) 

    def bulletShot(self, bullet):
        if bullet > 0:
            pygame.mixer.music.load("audio/gunShot.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
    
    def gunReload(self):
        pygame.mixer.music.load("audio/gunReload.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        pygame.display.flip()
        self.bulletRemaining()
        pygame.display.flip()
        tmp = self.maxBullet - self.bulletLeft
        self.bulletLeft = 6
        pygame.time.wait(int(pygame.mixer.Sound("audio/gunReload.wav").get_length() * 400))
        return True


def main():
    pygame.init()
    clock = pygame.time.Clock()

    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h

    screen = pygame.display.set_mode((max_width, max_height))
    pygame.mouse.set_visible(False)

    gun = Gun(20, loadImages('images/handGun', (200, 250)), screen, 25, 'images/cross.png', 'images/bullet.png', 100)
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                gun.bulletShot(gun.bulletLeft)
                gun.update(True)
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                if gun.bulletLeft < 6:
                    bulletReloadedAmount = 6
                    if gun.gunReload():
                        gun.update(6, bulletReloadedAmount)

        gun.update()
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