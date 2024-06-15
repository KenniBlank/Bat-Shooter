import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self, filePath):
        super().__init__()
        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (600, 600))
        self.gravity = 0

    def update(self):
        self.applyGravity()
        self.playerInput()

    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type  == "zombie":
            zombieloadAll = ....
            

        self.image
        self.rect

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    player = pygame.sprite.GroupSingle()
    player.add(Player("images/backgroundRoad.jpg"))

    clock = pygame.time.Clock()

    while True:
        player.draw(screen)
        player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(10)
        


if __name__ == "__main__":
    main()