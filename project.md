## This is my documentation/ note of all that I used to create the game.

 * import pygame &&
from sys import exit

* Initiates the whole process, on top:
    ```py
    pygame.init()
    ``` 

* To set the window height; accepts a tupple
    ```py
    pygame.display.set_mode((x,y)):  
    ```

* Title of the game: 
    ```py
    pygame.display.set_caption("PlaceHolder")
    ```

* Set the loop's update limit per second; inside the loop
    ```py 
    clock.tick(30) 
    ``` 

* Setting image like background:
    ```py
    image = pygame.image.load(imageLocation).convert()
    ```
    
* Setting the font:
    ```py
    text_font = pygame.font.Font('font/Pixeltype.ttf', font_size)
    text_surface = text_font.render(text_to_display, False, 'color')
    ```

* displaying image/ text:
    ```py
    screen.blit(text/ image, (X,Y))
    ```

* setting characters:
    ```py
    player = pygame.image.load(imageLocation).convert_alpha()
    
    # creating player rectangle 
    playerRect = player.get_rect(midbotton = (40, 300))
    
    # additionally you can use pygame.draw.rect()
    ```

* displaying player:
    ```py
    screen.blit(player, playerRect)
    ```

* detecting collision between two rectangle:
    ```py
    if (playerRect.colliderect(anotherRect)):
        pass

    # additionally we can set the events
    # if player.right <= 0: pass

    # check if the point x,y is in playerRect:
    # explained further in mouse section
    if (playerRect.collidepoint((x,y))):
        pass
    ```

* Updating the game:
    ```py
    pygame.display.update()
    ```

* Quit the Game On Window Close:
    ```py
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    ```

*  Mouse:
    ```py
    pygame.mouse

    # Method No.1
    # returns a tupple containing mouse position on screen
    mouse_position = pygame.mouse.get_pos()

    if (playerRect.collidepoint(mouse_position)):
        # return a (false, false, false) for each of mouse button until click
        pygame.mouse.get_pressed()


    ## Method No.2
    # another is to use the existing Quit event for loop:
    if event.type = pygame.MOUSEPOSITION:
        print(event.position)

    # intresting
    if event.type == pygame.MOUSEBUTTONDOWN/ MOUSEBUTTONUP:
        print('clicked button')
    ```

* Player Character Settings:
    ```py
    ## keyboard input

    # Method No.1
    # only need keys once for the whole program in loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass
    # Method No.2
    # event in for loop mensioned in quit game
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            pass
    
    ## JUMPING AND FALLING:
    # gravity:
    gravity = 0 # initialize
    gravity += 1 # update every loop
    # gravity is increased exponently:
    playerRect.y += gravity
    # Jumping Theory:
    gravity = -20 on space press

    ## Adding in a platform:
    if playerRect.bottom >= number: playerRect.bottom = number
    ```

* Transform: READ THE DOC

* SPRITE Class: Default by pygame, Inherit 
    ```py
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image;
            self.rect;

    ```