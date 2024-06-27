import pytest, pygame
from projectClasses import Gun, Bat, Background
from project import loadImages


@pytest.fixture
def gunfixture():
    max_width = 1366
    max_height = 766
    screen = pygame.display.set_mode((max_width, max_height))
    return Gun(
        12, loadImages('images/handGun', (200, 250)), 
        screen, 25, 
        'images/cross.png', 
        'images/bullet.png', 
        12,
        max_width,
        max_height
    )

@pytest.fixture
def batfixture():
    max_width = 1366
    max_height = 766
    screen = pygame.display.set_mode((max_width, max_height))
    return Bat(
        loadImages('images/batHorizontal', 
        (20, 20)), 
        20, 
        screen,
        max_width,
        max_height
    )

@pytest.fixture
def backgroundfixture():
    max_width = 1366
    max_height = 766
    screen = pygame.display.set_mode((max_width, max_height))
    
    return Background(
        loadImages('images/intro', (max_width, max_height)),
        loadImages('images/outro', (max_width, max_height)),
        screen,
        max_width,
        max_height
    )


def test_Gun(gunfixture):
    gun = gunfixture
    # checking if the initialization works
    assert gun.bulletInGun == 12
    assert gun.maxBullet == 12

    # checking if image loaded to object is true
    assert gun.listOfImages is not None
    assert gun.image is not None
    assert gun.rect is not None

def test_Bat(batfixture):
    bat = batfixture
    # Checking if bat initialization is working
    assert bat.max_width == 1366
    assert bat.max_height == 766


def test_Background(backgroundfixture):
    background = backgroundfixture
    # checking if the background intro and outro images are there
    assert background.listOfIntroImages is not None
    assert background.listOfOutroImages is not None

    assert background.draw(0)

