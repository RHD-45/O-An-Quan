import piece as p
# THIS THING RUNS IN TERMINAL, COPY THIS TO MAKE A GRAPHICAL ONE

def printgame(current):
    print(f'{[game[0]]} {game[7:12][::-1]}\n      '
          f'{game[1:6]} {[game[6]]}')
    print(current) if current != -1 else 0

def initialize():
    global game
    game = [0.5, 1,0,0,0,0, 0.5, 0,0,0,0,0]           # If there is a Quan, the value will be a float
    return game

def draw_terminal():
    print()

def choose(player):
    # WIN / LOSS CHECK
    if ((set(game[1:6]) == {0} and player.num == 1) or (set(game[7:]) == {0} and player.num == 2)):
        if player.score >= 5:
            print('Out of moves, adding rocks...')
            if player.num == 1:
                for i in range(1, 6): game[i] = 1
            else:
                for i in range(7, 12): game[i] = 1
            printgame(-1)
        else:
            print(f'Player {1 if player.num == 1 else 2} lost!')
            return 200

    # CHOOSE SQUARE
    choice_square = [i for i in range(1,6) if game[i] != 0] if player.num == 1 else [i for i in range(7,12) if game[i] != 0]
    num = int(input(f'Player {player.num}, choose your square ({choice_square[0]}-{choice_square[-1]}): '))
    while num not in choice_square:
        num = int(input(f'Invalid square, try again: '))

    dir = input(f'Choose a direction (L/R): ').upper()
    while dir not in ['L','R']:
        dir = input(f'Invalid direction, try again (L/R): ').upper()
    return (num,dir)

def distribute(player,idx,dir):

    direction = -1 if dir == 'L' else 1

    current = idx + direction

    rock = game[idx]
    print('Rocks taken:',rock)
    game[idx] = 0

    while game[current] != 0 or rock != 0:
        if rock == 0:                               # If the next square of the ending square has rocks (NO ROCKS NOW)
            if current in [0,6]: break              # And if it is not a Quan square
            rock = game[current]                    # Take those rocks
            game[current] = 0
            current += direction                    # Continue at the next square

        if current == -1 and direction == -1: current = 11   # Typical out-of-index check
        if current == 12 and direction == 1: current = 0

        game[current] += 1                          # Passing rocks
        rock -= 1
        current += direction

        if current == -1 and direction == -1: current = 11   # Typical out-of-index check
        if current == 12 and direction == 1: current = 0

        printgame(current)


    while game[current] == 0 and game[(current + direction) % 12] != 0:    # Check for multiple captures

        if (current + direction) % 12 == 0: # Quan check
            player.score += 10*int(game[0] % 1 != 0) + (game[0] - 0.5*int(game[0] % 1 != 0))
        elif (current + direction) % 12 == 6: # Quan check
            player.score += 10*int(game[6] % 1 != 0) + (game[6] - 0.5*int(game[6] % 1 != 0))
        else: player.score += game[(current + direction) % 12] # Normal

        game[(current + direction) % 12] = 0    # Remove rock
        current += 2*direction                  # Continue 2 spaces


        if current <= -1 and direction == -1: current = current % 12  # Typical out-of-index check
        if current >= 12 and direction == 1: current = current % 12
        printgame(current)

    print(f'{[game[0]]} {game[7:12][::-1]}\n      '
          f'{game[1:6]} {[game[6]]}')
    print('Score: ',end='')
    return player.score


# ERROR CODES:
# 200 = Player won / lost

# L = Clockwise, R = Counter-clockwise

def main():
    initialize()
    P1 = p.Player(1,0)
    P2 = p.Player(2,0)
    P2.score = 5
    print(distribute(P1,1,'L'))
    c = choose(P2)
    print(distribute(P2, *c))

if __name__ == "__main__":
    main()