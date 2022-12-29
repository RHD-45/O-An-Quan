import pygame as py

py.init()
WIDTH = 800
HEIGHT = 500
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Ô Ăn Quan')
running = True
BG = py.image.load('ground.jpg')


class Square(py.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()
        self.num = num


while running:
    SCREEN.fill((244, 209, 98))  # Delete later

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    py.draw.rect(SCREEN, (255, 255, 255), (0, HEIGHT / 2, WIDTH, 1), 2)
    py.draw.rect(SCREEN, (255, 255, 255), (WIDTH / 2, 0, 1, HEIGHT), 2)
    py.draw.rect(SCREEN, 'red', (WIDTH / 2 - 80 / 2, HEIGHT / 4 + 20 + 1, 80, HEIGHT / 4 - 20), 2)
    py.draw.rect(SCREEN, 'red', (WIDTH / 2 - 80 / 2, HEIGHT / 4 + 20 + 105 - 1, 80, HEIGHT / 4 - 20), 2)
    py.display.flip()  # Delete later

py.quit()
