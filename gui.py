import pygame as py

py.init()
FPS = 60
WIDTH = 800
HEIGHT = 500
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Ô Ăn Quan')
running = True
BG = py.image.load('ground.jpg')


class Square(py.sprite.Sprite):
    def __init__(self,num,rock,color):
        super(Square,self).__init__()
        self.num = num
        self.rock = rock
        self.color = color
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
        self.rect = py.draw.rect(SCREEN,'black',(self.x,self.y,*self.surf))

    def draw_square(self):
        py.draw.rect(SCREEN, self.color, (self.x, self.y, *self.surf), 2)

    @staticmethod
    def click_detection(list):
        pos = py.mouse.get_pos()
        clicked = [s for s in square_list if s.rect.collidepoint(pos)]
        if clicked and square_list.index(clicked[0]) not in (0,6):
            if clicked[0].color == 'red':
                for i in square_list: i.color = 'black'
            else:
                for i in square_list: i.color = 'black'
                clicked[0].color = 'red'
        else: return None
        return square_list.index(clicked[0])

# ----------------------------------------------------------------------------

# s0 = s1 = s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = s10 = s11 = None
square_list = []
all_sprite_list = py.sprite.Group()


j = 0
for i in range(12):
    square = Square(j,5,'black')
    square_list.append(square)
    all_sprite_list.add(square)
    j += 1


clock = py.time.Clock()
while running:
    clock.tick(FPS)
    SCREEN.fill((244, 209, 98))  # Delete later

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            print(Square.click_detection(square_list))

    py.draw.rect(SCREEN, (255, 255, 255), (0, HEIGHT / 2, WIDTH, 1), 2)
    py.draw.rect(SCREEN, (255, 255, 255), (WIDTH / 2, 0, 1, HEIGHT), 2)

    for i in square_list:
        Square.draw_square(i)



    py.display.flip()  # Delete later


py.quit()
