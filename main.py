# Code taken from: https://www.geeksforgeeks.org/tic-tac-toe-gui-in-python-using-pygame/
# Code taken from: https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/

import pygame as pg
import sys
import time
import random
from pygame.locals import *

WIDTH, HEIGHT = 400, 400
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
MAX_SCORE, MIN_SCORE = 1000, -1000
FPS = 30

pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")
initiating_window = pg.transform.scale(pg.image.load("modified_cover.png"), (WIDTH, HEIGHT + 100))
x_img = pg.transform.scale(pg.image.load("X_modified.png"), (80, 80))
o_img = pg.transform.scale(pg.image.load("o_modified.png"), (80, 80))

current_turn = 'x'
winner = None
draw = None
board = [[None] * 3 for _ in range(3)]
minimax_iterations = 0

def main():
    games_played = 0
    game_initiating_window()

    while games_played < 200:
        for event in pg.event.get():
            if event.type == QUIT:
                quit_game(games_played)
            elif event.type == MOUSEBUTTONUP and current_turn == 'x':
                user_click()
                if winner or draw:
                    games_played += 1
                    reset_game()
                elif current_turn == 'o' and not winner and not draw:
                    computer_move()
                    if winner or draw:
                        games_played += 1
                        reset_game()

        pg.display.update()
        CLOCK.tick(FPS)

    quit_game(games_played)


def game_initiating_window():
    screen.blit(initiating_window, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(WHITE)
    pg.event.clear()

    for i in range(1, 3):
        pg.draw.line(screen, LINE_COLOR, (WIDTH / 3 * i, 0), (WIDTH / 3 * i, HEIGHT), 7)
        pg.draw.line(screen, LINE_COLOR, (0, HEIGHT / 3 * i), (WIDTH, HEIGHT / 3 * i), 7)
    draw_status()


def draw_status():
    global draw
    message = f"{current_turn.upper()}'s Turn" if winner is None else f"{winner.upper()} won!"
    if draw:
        message = "Game Draw!"
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, WHITE)
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    screen.blit(text, text.get_rect(center=(WIDTH / 2, 500 - 50)))
    pg.display.update()


def check_win():
    global winner, draw
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6), 4)
            return
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            return
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
        return
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
        return
    if all([all(row) for row in board]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):
    global current_turn
    posx = (col - 1) * WIDTH // 3 + (WIDTH // 6 - 40)
    posy = (row - 1) * HEIGHT // 3 + (HEIGHT // 6 - 40)
    board[row - 1][col - 1] = current_turn
    screen.blit(x_img if current_turn == 'x' else o_img, (posx, posy))
    current_turn = 'o' if current_turn == 'x' else 'x'
    pg.display.update()


def user_click():
    x, y = pg.mouse.get_pos()
    col = (x // (WIDTH // 3)) + 1
    row = (y // (HEIGHT // 3)) + 1
    if row <= 3 and col <= 3 and board[row - 1][col - 1] is None:
        drawXO(row, col)
        check_win()


def computer_move():
    global minimax_iterations
    minimax_iterations = 0
    valid_moves = [(row, col) for row in range(1, 4) for col in range(1, 4) if board[row - 1][col - 1] is None]
    if not valid_moves:
        return
    best_val, best_move = MIN_SCORE, (-1, -1)
    for row, col in valid_moves:
        board[row - 1][col - 1] = 'o'
        move_val = minimax(board, 0, False, MIN_SCORE, MAX_SCORE)
        board[row - 1][col - 1] = None
        if move_val > best_val:
            best_move = (row, col)
            best_val = move_val
    if best_move != (-1, -1):
        drawXO(best_move[0], best_move[1])
        check_win()
    print(minimax_iterations)


def minimax(board, depth, isMax, alpha, beta):
    global minimax_iterations
    minimax_iterations += 1
    score = evaluate(board)

    if score == 10 or score == -10:
        return score
    if not isMovesLeft(board):
        return 0

    if isMax:
        best = MIN_SCORE
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'o'
                    val = minimax(board, depth + 1, not isMax, alpha, beta)
                    best = max(best, val)
                    alpha = max(alpha, best)
                    board[i][j] = None
                    if beta <= alpha:
                        break
        return best
    else:
        best = MAX_SCORE
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'x'
                    val = minimax(board, depth + 1, not isMax, alpha, beta)
                    best = min(best, val)
                    beta = min(beta, best)
                    board[i][j] = None
                    if beta <= alpha:
                        break
        return best


def isMovesLeft(board):
    return any(None in row for row in board)


def evaluate(b):
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2]:
            if b[row][0] == 'o':
                return 10
            elif b[row][0] == 'x':
                return -10
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col]:
            if b[0][col] == 'o':
                return 10
            elif b[0][col] == 'x':
                return -10
    if b[0][0] == b[1][1] == b[2][2]:
        if b[0][0] == 'o':
            return 10
        elif b[0][0] == 'x':
            return -10
    if b[0][2] == b[1][1] == b[2][0]:
        if b[0][2] == 'o':
            return 10
        elif b[0][2] == 'x':
            return -10
    return 0


def reset_game():
    global board, winner, current_turn, draw
    time.sleep(1)
    current_turn, winner, draw = 'x', None, None
    board = [[None] * 3 for _ in range(3)]
    game_initiating_window()


def quit_game(games_played):
    print(f"Games played: {games_played}")
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()