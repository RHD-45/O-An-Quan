import os.path

import pygame as py

import piece

import time

py.init()
FPS = 60
WIDTH = 800
HEIGHT = 500
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Ô Ăn Quan')
running = True

# ASSETS ----------------------------------------------
BG = py.image.load('ground.jpg')
BG_COLOR = (244, 209, 98)
FONT = py.font.Font('freesansbold.ttf', 15)
rockimage = {
    1: py.transform.scale(py.image.load(os.path.join('Assets', '1rock.png')), (80, HEIGHT // 4 - 20)),
    2: py.transform.scale(py.image.load(os.path.join('Assets', '2rock.png')), (80, HEIGHT // 4 - 20)),
    3: py.transform.scale(py.image.load(os.path.join('Assets', '3rock.png')), (80, HEIGHT // 4 - 20)),
    4: py.transform.scale(py.image.load(os.path.join('Assets', '4rock.png')), (80, HEIGHT // 4 - 20)),
    5: py.transform.scale(py.image.load(os.path.join('Assets', '5rock.png')), (80, HEIGHT // 4 - 20)),
    6: py.transform.scale(py.image.load(os.path.join('Assets', '6rock.png')), (80, HEIGHT // 4 - 20)),
    'M': py.transform.scale(py.image.load(os.path.join('Assets', 'manyrock.png')), (80, HEIGHT // 4 - 20)),
    'Q': py.transform.scale(py.image.load(os.path.join('Assets', 'quan.png')), (80, (HEIGHT // 4 - 20) // 2)),
}


# ------------------------------------------------------

def initialize():
    global game
    game = []
    for i in range(12):
        if i in (0, 6):
            # noinspection PyUnboundLocalVariable
            square = Quan(i, 0, 'black', True)
        else:
            square = Square(i, 5, 'black')
        game.append(square)
        square_list.append(square)
        all_sprite_list.add(square)
    return game


def distribute(player, idx, dir):
    direction = -1 if dir == 'L' else 1

    current = idx + direction

    rock = game[idx].rock
    print('Rocks taken:', rock)
    game[idx].rock = 0

    while game[current].rock != 0 or rock != 0:
        if rock == 0:  # If the next square of the ending square has rocks (NO ROCKS NOW)
            if current in [0, 6]: break  # And if it is not a Quan square
            rock = game[current].rock  # Take those rocks
            game[current].rock = 0
            current += direction  # Continue at the next square

        if current == -1 and direction == -1: current = 11  # Typical out-of-index check
        if current == 12 and direction == 1: current = 0

        game[current].rock += 1  # Passing rocks
        rock -= 1
        current += direction

        if current == -1 and direction == -1: current = 11  # Typical out-of-index check
        if current == 12 and direction == 1: current = 0

        # GUI UPDATES HERE --------------------------->>
        for ix, i in enumerate(square_list):
            if ix in [0, 6]:
                Quan.draw_quan(i)
            else:
                Square.draw_square(i)
        py.display.flip()
        time.sleep(0.5)

    while game[current].rock == 0 and game[(current + direction) % 12] != 0:  # Check for multiple captures

        if (current + direction) % 12 == 0:  # Quan check
            player.score += 10 * int(game[0].hasQuan) + game[0].rock
            game[0].hasQuan = False
            game[0].rock = 0
            Quan.draw_quan(game[0])
        elif (current + direction) % 12 == 6:  # Quan check
            player.score += 10 * int(game[6].hasQuan) + game[6].rock
            game[6].hasQuan = False
            game[6].rock = 0
            Quan.draw_quan(game[6])
        else:
            print((current + direction) % 12)
            player.score += game[(current + direction) % 12].rock  # Normal
            game[(current + direction) % 12].rock = 0  # Remove rock
            Square.draw_square(game[(current + direction) % 12])  # Draw

        current += 2 * direction  # Continue 2 spaces

        if current <= -1 and direction == -1: current = current % 12  # Typical out-of-index check
        if current >= 12 and direction == 1: current = current % 12

    print(f'{[game[0]]} {game[7:12][::-1]}\n      '
          f'{game[1:6]} {[game[6]]}')
    print('Score: ', end='')
    return player.score


# -----------------------------------------------------------------


class Square(py.sprite.Sprite):
    def __init__(self, num, rock, color):
        super(Square, self).__init__()
        self.num = num
        self.rock = rock
        self.color = color
        self.surf = (80, HEIGHT // 4 - 20)
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
        self.rect = py.draw.rect(SCREEN, 'black', (self.x, self.y, *self.surf))

    def draw_square(self):
        py.draw.rect(SCREEN, self.color, (self.x, self.y, *self.surf), 2)  # Square border
        text = FONT.render(str(self.rock), True, 'green')  # Number of rocks text
        SCREEN.fill(BG_COLOR, (self.x + 3, self.y + 3, self.surf[0] - 10, self.surf[1] - 10))  # Square background
        if self.rock >= 7:
            SCREEN.blit(rockimage['M'], (self.x, self.y), special_flags=py.BLEND_RGBA_MIN)
        elif self.rock != 0:
            SCREEN.blit(rockimage[self.rock], (self.x, self.y), special_flags=py.BLEND_RGBA_MIN)  # Rock image
        SCREEN.blit(text, py.Rect(self.x + 3, self.y + 3, 10, 10))  # Show text
        py.display.flip()

    @staticmethod
    def click_detection(list):
        pos = py.mouse.get_pos()
        clicked = [s for s in square_list if s.rect.collidepoint(pos)]
        if clicked and square_list.index(clicked[0]) not in (0, 6):
            if clicked[0].color == 'red':
                clicked[0].color = 'black'
            else:
                for i in square_list: i.color = 'black'
                clicked[0].color = 'red'
        else:
            for i in square_list: i.color = 'black'
            return None
        return square_list.index(clicked[0])


class Quan(Square):
    def __init__(self, num, rock, color, hasQuan):
        super().__init__(num, rock, color)
        self.hasQuan = hasQuan
        self.yQ = 255

    def draw_quan(self):
        SCREEN.fill(BG_COLOR, (self.x + 3, self.y + 3, *self.surf))  # Square background
        py.draw.rect(SCREEN, self.color, (self.x, self.y, *self.surf), 2)  # Square border
        text = FONT.render(str(self.rock + 10 * int(self.hasQuan)), True, 'green')  # Number of rocks text
        if self.hasQuan:
            SCREEN.blit(rockimage['Q'], (self.x, self.yQ), special_flags=py.BLEND_RGBA_MIN)
        if self.rock >= 7:
            SCREEN.blit(rockimage['M'], (self.x, self.y), special_flags=py.BLEND_RGBA_MIN)
        elif self.rock != 0:
            SCREEN.blit(py.transform.scale(rockimage[self.rock], (80, (HEIGHT // 4 - 20) // 2)),
                        (self.x, self.y), special_flags=py.BLEND_RGBA_MIN)  # Rock image
        SCREEN.blit(text, py.Rect(self.x + 3, self.y + 3, 10, 10))  # Show text
        py.display.flip()


# ----------------------------------------------------------------------------

# s0 = s1 = s2 = s3 = s4 = s5 = s6 = s7 = s8 = s9 = s10 = s11 = None

square_list = []
all_sprite_list = py.sprite.Group()
initialize()

clock = py.time.Clock()
while running:
    clock.tick(FPS)
    SCREEN.fill(BG_COLOR)  # Delete later

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            print(Square.click_detection(square_list))

    py.draw.rect(SCREEN, (255, 255, 255), (0, HEIGHT / 2, WIDTH, 1), 2)
    py.draw.rect(SCREEN, (255, 255, 255), (WIDTH / 2, 0, 1, HEIGHT), 2)

    for i in square_list:
        Square.draw_square(i)

    P1 = piece.Player(1, 0)
    P2 = piece.Player(2, 0)
    score = distribute(P1, 5, 'L')
    time.sleep(0.5)
    score = distribute(P2, 3, 'R')
    i = input()

    py.display.flip()  # Delete later

py.quit()
