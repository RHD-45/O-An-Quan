import pygame as py

py.init()
WIDTH = 800
HEIGHT = 500
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Ô Ăn Quan')
running = True
BG = py.image.load('ground.jpg')


class Square(py.sprite.Sprite):
    def __init__(self,num,rock):
        super(Square,self).__init__()
        self.num = num
        self.rock = rock
        self.surf = (80, HEIGHT / 4 - 20)
        match num:
            case 1 | 11:
                self.x = 200
            case 2 | 10:
                self.x = 280
            case 3 | 9:
                self.x = 360
            case 4 | 8:
                self.x = 440
            case 5 | 7:
                self.x = 520
            case 0:
                self.x = 120
            case 6:
                self.x = 600
        match num:
            case 7 | 8 | 9 | 10 | 11:
                self.y = 146
            case 1 | 2 | 3 | 4 | 5:
                self.y = 250
            case 6 | 0:
                self.y = 198





while running:
    SCREEN.fill((244, 209, 98))  # Delete later

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    py.draw.rect(SCREEN, (255, 255, 255), (0, HEIGHT / 2, WIDTH, 1), 2)
    py.draw.rect(SCREEN, (255, 255, 255), (WIDTH / 2, 0, 1, HEIGHT), 2)

    s0 = s1 = s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = s10 = s11 = None
    squares = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11]
    j = 0
    for i in range(len(squares)):
        squares[i] = Square(j,5)
        j += 1
    for i in squares:
        py.draw.rect(SCREEN,'red',(i.x,i.y,*i.surf),2)
    py.display.flip()  # Delete later


py.quit()
