import pygame, random


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
        # Arguments
        self.listOfImages = listOfImages
        self.bulletToBeInGun = bullet
        self.bulletInGun = bullet
        self.image = listOfImages[0]
        self.screen = screen
        self.delay = delay
        self.gunCrossImage = pygame.transform.scale(pygame.image.load(filePathForCross).convert_alpha(), (30, 30))
        self.bullet = pygame.transform.scale(pygame.image.load(filePathForBullet).convert_alpha(), (40, 40))
        self.maxBullet = maxBullet
        
        # Additional Arguments
        self.rect = self.image.get_rect(midbottom=(Gun.gunX, Gun.gunY))
        self.gunImageIndex = 0
        self.shotFired = False
        self.gunYTemp = Gun.max_height
            
    def update(self, shotFired = False, bullet = 0):
        Gun.gunX = pygame.mouse.get_pos()[0]
        Gun.gunY = pygame.mouse.get_pos()[1]

        if shotFired:
            self.shotFired = shotFired
        self.draw()
        if bullet > 0:
            self.updateBulletCount(bullet)
    
    def updateBulletCount(self, numberOfBullets):
        self.bulletInGun = numberOfBullets
    
    def draw(self):
        self.bulletRemaining()
        self.gunCross()
        if self.bulletInGun == 0: 
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
        if self.shotFired == True and self.bulletInGun > 0:
            pygame.time.delay(self.delay)
            self.screen.blit(tmpImage, self.rect.topleft)
            self.gunImageIndex += 1
            if self.gunImageIndex >= len(self.listOfImages):
                self.gunImageIndex = 0
                self.shotFired = False
                self.bulletInGun -= 1
            self.image = self.listOfImages[self.gunImageIndex]
        else:
            self.screen.blit(tmpImage, self.rect.topleft)

    def gunCross(self):
        self.screen.blit(self.gunCrossImage, (Gun.gunX, Gun.gunY))

    def bulletRemaining(self):
        font = pygame.font.Font('font/Pixeltype.ttf', 32)
        text = f"Bullet Left: {self.bulletInGun} X "
        textSurface = font.render(text, False, 'Black')
        if self.bulletInGun <= 12:
            for i in range(int(self.bulletInGun)):
                self.screen.blit(self.bullet, (Gun.max_width - 90 - 20 * i, 30))
                text = f"BulletInventory: {self.maxBullet}"
                textSurface = font.render(text, False, 'Black')
                self.screen.blit(textSurface, (Gun.max_width - 10 * len(text) - 60, 75))
        else:
            self.screen.blit(textSurface, (Gun.max_width - 10 * len(text) - 60, 45))
            text = f"BulletInventory: {self.maxBullet}"
            textSurface = font.render(text, False, 'Black')
            self.screen.blit(textSurface, (Gun.max_width - 10 * len(text) - 60, 75))
            self.screen.blit(self.bullet, (Gun.max_width - 90, 30)) 

    def bulletShot(self, bullet):
        if bullet > 0:
            pygame.mixer.music.load("audio/gunShot.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
    
    def gunReload(self):
        tmp = self.maxBullet - self.bulletToBeInGun
        if self.maxBullet >= 0 and self.maxBullet > 0:
            pygame.mixer.music.load("audio/gunReload.wav")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
            pygame.display.flip()
            
            self.bulletRemaining()
            pygame.display.flip()
            if tmp > 0:
                self.maxBullet = tmp
                self.bulletInGun = self.bulletToBeInGun
            else:
                self.bulletInGun = self.maxBullet
                self.maxBullet = 0
            pygame.time.wait(int(pygame.mixer.Sound("audio/gunReload.wav").get_length() * 400))
            return True
        
class Bat(pygame.sprite.Sprite):
    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h
    tmp = 0
    batShot = 0

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