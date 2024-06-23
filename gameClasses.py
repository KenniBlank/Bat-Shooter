import pygame, random

class Gun(pygame.sprite.Sprite):
    pygame.init()
    display_info = pygame.display.Info()
    max_width = display_info.current_w
    max_height = display_info.current_h
    gunX = 0
    gunY = 0
    kills = 0
    timeDelayGun = 0

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
            
    def update(self, shotFired = False):
        Gun.gunX = pygame.mouse.get_pos()[0]
        Gun.gunY = pygame.mouse.get_pos()[1]
        
        if shotFired:
            self.shotFired = shotFired
        self.draw()
        
        if Gun.timeDelayGun > 0:
            Gun.timeDelayGun -= 1
    
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
        if Gun.timeDelayGun == 0:
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
        # Tmp my ass!
        tmp = self.maxBullet - self.bulletInGun
        if self.maxBullet >= 0 and tmp >= 0:
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
        self.spawnX = 0
        self.spawnY = 0
        self.spawn()

    def hitTest(self, gunCross, gunCrossX, gunCrossY):
        scaled_bat_image = pygame.transform.scale(self.batImages[self.batImageIndex], (self.scale, self.scale))
        bat_rect = scaled_bat_image.get_rect(topleft=(self.spawnX, self.spawnY))
        gunCross_rect = gunCross.get_rect(topleft=(gunCrossX, gunCrossY))
        return bat_rect.colliderect(gunCross_rect)
    
    def update(self):
        self.batdraw()
        if self.scale > 90:
            return True

    def spawn(self):
        self.spawnX = random.randint(40, Bat.max_width - 50)
        self.spawnY = random.randint(40, Bat.max_height - Bat.max_height / 3)
        self.scale = 40
    
    def batdraw(self):
        Bat.tmp += (random.randint(1, 6) / 10)
        self.scale += (0.25)
        self.batImageIndex = int(Bat.tmp) 
        self.screen.blit(pygame.transform.scale(self.batImages[self.batImageIndex], (self.scale, self.scale)), (self.spawnX, self.spawnY))
        if self.batImageIndex >= len(self.batImages) - 1:
            self.batImageIndex = 0
            Bat.tmp = 0

class Background():
    intro = True
    def __init__(self, introImages, outroImages, screen, width, height):
        self.listOfIntroImages = introImages
        self.listOfOutroImages = outroImages
        self.screen = screen
        self.width = width
        self.height = height

        self.font_size = 30
        self.text_font = pygame.font.Font('font/Pixeltype.ttf', self.font_size)
        self.textsIntro = ["Hey Hero!",
             "Apocalypse Has Hit Your City!", 
             "Bats Have OverRun Your City", 
             "The City Needs You", 
             "Start By Getting Used To Your Pistol"
             ]
        
        self.textsOutro = ["You Have Saved The City For The Night!",
                           "You Are The Unsung Hero Of This City.",
                           "You Protect From Dark When The City Rests.",
                           "You Can Rest Now!",
                           "GoodNight Hero!",
                           "Enter To Exit",
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
        # TODO: Fix aligment
        # I have no Idea how!
        clock = pygame.time.Clock()
        if num == 0:
            i = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                        self.textsIntroIndex += 1
                        i = 0

                
                text_surface = self.text_font.render(self.textsIntro[self.textsIntroIndex][:i], False, 'Black')
                self.introIndex += 1
                self.screen.blit(self.listOfIntroImages[self.introIndex], (0, 0))
                if self.introIndex >= len(self.listOfIntroImages) - 1:
                    self.introIndex = 0

                if self.textsIntroIndex >= len(self.textsIntro) - 1:
                    return
                self.screen.blit(text_surface, (self.width / 2 - len(self.textsIntro[self.textsIntroIndex] * 4), int(self.height / 2 - (1 / 4) * self.height)))
                i += 1
                pygame.display.flip()
                clock.tick(10)
        else:
            i = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                        self.textsOutroIndex += 1
                        i = 0

                text_surface = self.text_font.render(self.textsOutro[self.textsOutroIndex][:i], False, 'White')
                self.outroIndex += 1
                self.screen.blit(self.listOfOutroImages[self.outroIndex], (0, 0))
                if self.outroIndex >= len(self.listOfOutroImages) - 1:
                    self.outroIndex = 0

                if self.textsOutroIndex >= len(self.textsOutro) - 1:
                    return
                self.screen.blit(text_surface, (self.width / 2 - len(self.textsOutro[self.textsOutroIndex] * 4), int(self.height / 2 - (1 / 4) * self.height)))
                i += 1
                pygame.display.flip()
                clock.tick(10)