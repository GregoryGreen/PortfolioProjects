import numpy as np
import pygame
import sys
import math
Blue = (0, 0, 225)
Black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
ROW_COUNT = 9
COLUMN_COUNT = 8


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check for horizontal locations for the win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] == piece and board[r][c+5] == piece:
                return True

    # Check for vertical locations for the win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece and board[r][c+4] == piece and board[r][c+5] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] == piece and board[r+5][c+5] == piece:
                return True

     # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(5, ROW_COUNT-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] == piece and board[r-5][c+5] == piece:
                return True

# Creates the Red and Yellow pieces and Blue board


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, Blue, (c * SQUARESIZE, r *
                             SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))

            pygame.draw.circle(screen, Black, (int(
                c * SQUARESIZE+SQUARESIZE/2), int(r * SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, Red, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, Yellow, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
# Shapes the board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2-5)

screen = pygame.display.set_mode(size)
draw_board(board)


myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, Red, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, Yellow, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Plyer 1 wins!!", 1, Red)
                        screen.blit(label, (40, 10))
                        game_over = True

            # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, Yellow)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            pygame.display.update()

            # Alternate between player 1 turn and player 2 turn
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
