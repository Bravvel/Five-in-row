# import random
# import numpy as np
# import pygame
# import sys
#
# pygame.init()
# size_block = 40
# margin = 6
# board_size = 6
# width = heigth = size_block*board_size + margin * board_size+1
# # Глубина поиска для алгоритма минимакс
# depth = 3
#
# size_window = (width, heigth)
# screen = pygame.display.set_mode(size_window)
# board = pygame.Surface(size_window)
# pygame.display.set_caption("Крестики-нолики")
#
# black = (0, 0, 0)
# red = (255, 0, 0)
# green = (0, 255, 0)
# white = (255, 255, 255)
#
# cells = np.zeros((15, 15))
#
# query = 0;
# winner = False
#
# def make_step(x_mouse,y_mouse, query, flag=False):
#     if not flag:
#         col = x_mouse // (size_block + margin)
#         row = y_mouse // (size_block + margin)
#     else:
#         col = x_mouse
#         row = y_mouse
#     if cells[row, col] == 0:
#         if query % 2 == 0:
#             cells[row, col] = 1
#         else:
#             cells[row, col] = -1
#         return True
#     return False
#
#
# def check_winner(board, query):
#     if query % 2 == 0:
#         symbol = 1
#     else:
#         symbol = -1
#     zeroes = 0
#     for row in range(board_size):
#         for col in range(board_size):
#             if board[row, col] == 0:
#                 zeroes += 1
#     # Проверка по горизонтали
#     for row in range(board_size):
#         for col in range(board_size-4):
#             if board[row, col] == symbol and board[row, col + 1] == symbol and board[row , col + 2] == symbol and \
#                     board[row , col + 3] == symbol and board[row , col + 4] == symbol:
#                 return symbol
#
#     # Проверка по вертикали
#     for col in range(board_size):
#         for row in range(board_size-4):
#             if board[row, col] == symbol and board[row + 1 , col] == symbol and board[row + 2 , col] == symbol and \
#                     board[row + 3 , col] == symbol and board[row + 4 , col] == symbol:
#                 return symbol
#
#     # Проверка по главной диагонали
#     for row in range(board_size-4):
#         for col in range(board_size-4):
#             if board[row, col] == symbol and board[row + 1 , col + 1] == symbol and board[row + 2 , col + 2] == symbol and \
#                     board[row + 3 , col + 3] == symbol and board[row + 4 , col + 4] == symbol:
#                 return symbol
#
#     # Проверка по побочной диагонали
#     for row in range(board_size-4):
#         for col in range(4, board_size):
#             if board[row, col] == symbol and board[row + 1 , col - 1] == symbol and board[row + 2 , col - 2] == symbol and \
#                     board[row + 3 , col - 3] == symbol and board[row + 4 , col - 4] == symbol:
#                 return symbol
#     if zeroes == 0:
#         return "Draw"
#     return False
#
# def get_move_computer(board):
#     empty = []
#     for row in range(board_size):
#         for col in range(board_size):
#             if board[row, col] == 0:
#                 empty.append((row, col))
#     return random.choice(empty)
#
# def computer(symbol):
#     row, col = get_move_computer(cells)
#     make_step(col, row, symbol, True)
#     winner = check_winner(cells, symbol)
#     if winner == "Draw" :
#         draw_win(winner)
#         return "Draw"
#     if winner:
#         draw_win(winner)
#         return "Computer win"
#     if winner == False:
#         draw_board()
#         human(symbol + 1)
#
# def human(symbol = 0):
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit(0)
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 x_mouse, y_mouse = pygame.mouse.get_pos()
#                 if make_step(x_mouse, y_mouse, symbol):
#                     winner = check_winner(cells, symbol)
#                     if winner == "Draw":
#                         draw_win(winner)
#                         return "Draw"
#                     if winner:
#                         draw_win(winner)
#                         return "You win"
#                     if winner == False:
#                         draw_board()
#                         # computer(symbol + 1)
#                         smart_player(symbol + 1)
#
#
#
# def human_vs_human(query = 0):
#     draw_desk()
#     winner = ''
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit(0)
#             elif event.type == pygame.MOUSEBUTTONDOWN and not winner:
#                 x_mouse, y_mouse = pygame.mouse.get_pos()
#                 if make_step(x_mouse, y_mouse, query):
#                     winner = check_winner(cells, query)
#                     if winner:
#                         draw_win(winner)
#                     else:
#                         draw_board()
#                         query += 1
#         pygame.display.update()
#
# def draw_win(winner):
#     if winner == 1:
#         winner = 'x'
#     if winner == -1 :
#         winner = 'o'
#     screen.fill(black)
#     font = pygame.font.SysFont('stxingkai', 80)
#     text1 = font.render('win ' + winner, True, white)
#     text_rect = text1.get_rect()
#     text_x = screen.get_width() / 2 - text_rect.width / 2
#     text_y = screen.get_height() / 2 - text_rect.height / 2
#     screen.blit(text1, [text_x, text_y])
#     pygame.display.update()
#
# def draw_desk():
#     for row in range(board_size):
#         for col in range(board_size):
#             color = white
#             x = col * size_block + (col + 1) * margin
#             y = row * size_block + (row + 1) * margin
#             pygame.draw.rect(screen, color, (x, y, size_block, size_block))
#
# def draw_board():
#     for row in range(board_size):
#         for col in range(board_size):
#             if cells[row, col] == 1:
#                 color = red
#             elif cells[row, col] == -1:
#                 color = green
#             else:
#                 color = white
#             x = col * size_block + (col + 1) * margin
#             y = row * size_block + (row + 1) * margin
#             pygame.draw.rect(screen, color, (x, y, size_block, size_block))
#             if color == red:
#                 pygame.draw.line(screen, white, (x + 5, y + 5),
#                                  (x + size_block - 5, y + size_block - 5), 3)
#                 pygame.draw.line(screen, white, (x + size_block - 5, y + 5),
#                                  (x + 5, y + size_block - 5), 3)
#             elif color == green:
#                 pygame.draw.circle(screen, white, (x + size_block // 2, y + size_block // 2),
#                                    size_block // 2 - 3, 3)
#
#     pygame.display.update()
#
#
# # human_vs_human()
#
# # def start_game():
# #     draw_board()
# #     human()
# #
# # start_game()
#
# ########################################################################################################################
#
#
# # Функция для оценки текущей позиции на игровом поле
# def evaluate_position(board):
#     player_lines = count_lines(board, 1)  # Подсчет линий игрока (1 - фишка игрока)
#     opponent_lines = count_lines(board, -1)  # Подсчет линий оппонента (-1 - фишка оппонента)
#
#     # В данном примере можем оценивать позицию как разницу между линиями игрока и оппонента
#     score = player_lines - opponent_lines
#
#     return score
#
# # Функция для подсчета линий на доске для конкретного игрока
# def count_lines(board, player):
#     lines = 0
#
#     rows, cols = board.shape
#
#     # Подсчет горизонтальных линий
#     for i in range(rows):
#         for j in range(cols - 4):
#             if np.all(board[i, j:j + 5] == player):
#                 lines += 1
#
#     # Подсчет вертикальных линий
#     for i in range(cols):
#         for j in range(rows - 4):
#             if np.all(board[j:j + 5, i] == player):
#                 lines += 1
#
#     # Подсчет диагональных линий (по обеим диагоналям)
#     for i in range(rows - 4):
#         for j in range(cols - 4):
#             if np.all(np.diag(board[i:i + 5, j:j + 5]) == player):
#                 lines += 1
#             if np.all(np.diag(np.rot90(board)[i:i + 5, j:j + 5]) == player):
#                 lines += 1
#
#     return lines
#
#
# # Функция минимакса с альфа-бета отсечением
# def minimax(board, depth, alpha, beta, maximizing_player):
#     if depth == 0: # ПОД ВОПРОСОМ
#         return evaluate_position(board)
#
#     if maximizing_player:
#         print('ya max')
#         max_eval = float('-inf')
#         for possible_move in get_possible_moves(board):
#             eval = minimax(make_move(board, possible_move), depth - 1, alpha, beta, False)
#             max_eval = max(max_eval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         print('ya min')
#         min_eval = float('inf')
#         for possible_move in get_possible_moves(board):
#             eval = minimax(make_move(board, possible_move), depth - 1, alpha, beta, True)
#             min_eval = min(min_eval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval
#
#
# # Функция для получения всех возможных ходов на доске
# def get_possible_moves(board):
#     possible_moves = []
#
#     for i in range(board_size):
#         for j in range(board_size):
#             if board[i, j] == 0:
#                 possible_moves.append((i, j))
#
#     return possible_moves
#
#
# # Функция для совершения хода на доске
#
# def make_move(board, move):
#     new_board = np.copy(board)
#     new_board[move[0], move[1]] = 1  # Предположим, что 1 - фишка игрока
#     return new_board
#
#
# # Функция для выбора лучшего хода для компьютера
# def get_best_move(board, depth):
#     best_move = None
#     best_eval = float('-inf')
#     for possible_move in get_possible_moves(board):
#         eval = minimax(make_move(board, possible_move), depth, float('-inf'), float('inf'), False)
#         # eval = minimax(make_move(board, possible_move), depth, -100, 100, False)
#         if eval > best_eval:
#             best_eval = eval
#             best_move = possible_move
#
#     return best_move
#
# def smart_player(symbol):
#     row, col = get_best_move(cells, 0)
#     make_step(col, row, symbol, True)
#     winner = check_winner(cells, symbol)
#     if winner == "Draw" :
#         draw_win(winner)
#         return "Draw"
#     if winner:
#         draw_win(winner)
#         return "Computer win"
#     if winner == False:
#         draw_board()
#         human(symbol + 1)
#
# def start_game():
#     draw_board()
#     human()
#
# start_game()
import random
import numpy as np
import pygame
import sys
from agent import Agent

pygame.init()
wins = 0
size_block = 40
margin = 6
board_size = 9
array_score = [0, 1, 4, 16, 64, 256]
first_value = [0, 1, 9, 81, 729, 6561]
second_value = [0, 3, 27, 243, 2187, 19683]
my_agent = Agent(None)
width = heigth = size_block*board_size + margin * board_size+1
# Глубина поиска для алгоритма минимакс
depth = 3

size_window = (width, heigth)
screen = pygame.display.set_mode(size_window)
board = pygame.Surface(size_window)
pygame.display.set_caption("Крестики-нолики")

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

cells = [[0]*board_size for i in range(board_size)]
query = 0;
winner = False

def make_step(x_mouse,y_mouse, query, flag=False):
    if not flag:
        col = x_mouse // (size_block + margin)
        row = y_mouse // (size_block + margin)
    else:
        col = x_mouse
        row = y_mouse
    if cells[row][col] == 0:
        if query % 2 == 0:
            cells[row][col] = 1
        else:
            cells[row][col] = -1
        return True
    return False


def check_winner(board, query):
    if query % 2 == 0:
        symbol = 1
    else:
        symbol = -1
    zeroes = 0
    for row in cells:
        zeroes += row.count(0)
    # Проверка по горизонтали
    for row in range(board_size):
        for col in range(board_size-4):
            if board[row][col] == symbol and board[row][col + 1] == symbol and board[row][col + 2] == symbol and \
                    board[row][col + 3] == symbol and board[row][col + 4] == symbol:
                return symbol

    # Проверка по вертикали
    for col in range(board_size):
        for row in range(board_size-4):
            if board[row][col] == symbol and board[row + 1][col] == symbol and board[row + 2][col] == symbol and \
                    board[row + 3][col] == symbol and board[row + 4][col] == symbol:
                return symbol

    # Проверка по главной диагонали
    for row in range(board_size-4):
        for col in range(board_size-4):
            if board[row][col] == symbol and board[row + 1][col + 1] == symbol and board[row + 2][col + 2] == symbol and \
                    board[row + 3][col + 3] == symbol and board[row + 4][col + 4] == symbol:
                return symbol

    # Проверка по побочной диагонали
    for row in range(board_size-4):
        for col in range(4, board_size):
            if board[row][col] == symbol and board[row + 1][col - 1] == symbol and board[row + 2][col - 2] == symbol and \
                    board[row + 3][col - 3] == symbol and board[row + 4][col - 4] == symbol:
                return symbol
    if zeroes == 0:
        return 'Draw'
    return False

def get_move_computer(board):
    empty = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == 0:
                empty.append((row, col))
    return random.choice(empty)

def computer(symbol = 0):
    pygame.time.delay(500)
    # row, col = best_move_optimize(cells)
    # row, col = my_agent.choose_action(cells)
    # row, col = get_move_computer(cells)
    # row, col = best_move(cells)
    if symbol % 2 == 0:
        # row, col = best_move(cells)
        row, col = my_agent.choose_action(cells)
    else:
        row, col = best_move(cells)
    #     row, col = get_move_computer(cells)
    # print(esctimate_optimize(row, col, cells))
    make_step(col, row, symbol, True)
    winner = check_winner(cells, symbol)
    if winner:
        draw_win(winner)
        return "Computer win"
    else:
        draw_board()
        computer(symbol + 1)
        # human(symbol + 1)

def human(symbol = 0):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if make_step(x_mouse, y_mouse, symbol):
                    winner = check_winner(cells, symbol)
                    if winner:
                        draw_win(winner)
                        return "You win"
                    else:
                        draw_board()
                        computer(symbol + 1)


def human_vs_human(query = 0):
    draw_desk()
    winner = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and not winner:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if make_step(x_mouse, y_mouse, query):
                    print(esctimate(cells))
                    winner = check_winner(cells, query)
                    if winner:
                        draw_win(winner)
                    else:
                        draw_board()
                        query += 1

        pygame.display.update()

def draw_win(winner):
    if winner == 1:
        winner = "X"
    if winner == -1:
        winner = "O"
    screen.fill(black)
    font = pygame.font.SysFont('stxingkai', 80)
    text1 = font.render('win ' + winner, True, white)
    text_rect = text1.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text1, [text_x, text_y])
    pygame.display.update()

def draw_desk():
    for row in range(board_size):
        for col in range(board_size):
            color = white
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, size_block, size_block))

def draw_board():
    for row in range(board_size):
        for col in range(board_size):
            if cells[row][col] == 1:
                color = red
            elif cells[row][col] == -1:
                color = green
            else:
                color = white
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, size_block, size_block))
            if color == red:
                pygame.draw.line(screen, white, (x + 5, y + 5),
                                 (x + size_block - 5, y + size_block - 5), 3)
                pygame.draw.line(screen, white, (x + size_block - 5, y + 5),
                                 (x + 5, y + size_block - 5), 3)
            elif color == green:
                pygame.draw.circle(screen, white, (x + size_block // 2, y + size_block // 2),
                                   size_block // 2 - 3, 3)

    pygame.display.update()


# human_vs_human()

def esctimate(cells1):
    score = 0
    i = 0
    for row in range(board_size):
        for col in range(board_size):
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if not (a == 0 and b == 0):
                        score += first_value[score_(row, col, a, b, 1, cells1)] - second_value[score_(row, col, a, b, -1, cells1)]
                        # score += first_value[score_(row, col, a, b, -1, cells1)] - second_value[score_(row, col, a, b, 1, cells1)]
    return score

# def esctimate_optimize(row, col, cells1):
#     score = 0
#
#     for a in range(-1, 2):
#         for b in range(-1, 2):
#             if not (a == 0 and b == 0):
#                 score += first_value[score_(row, col, a, b, 1, cells1)] - second_value[score_(row, col, a, b, -1, cells1)]
#                 # score += first_value[score_(row, col, a, b, -1, cells1)] - second_value[score_(row, col, a, b, 1, cells1)]
#     print(row, col)
#     print(score)
#     return score

def score_(x, y, a, b, symbol, cells1):
    score = 0
    for i in range(5):
        flag = border(x+a*i, y+b*i)
        if flag == -1 or (cells1[x+a*i][y+b*i] != symbol and cells1[x+a*i][y+b*i] != 0):
            return 0
        else:
            if cells1[x+a*i][y+b*i] == symbol:
                score += 1
    return score

def border(x, y):
    if x >= 0 and x < board_size and y >= 0 and y < board_size:
        return True
    return -1

def best_move(cells1):
    tmp_cells = cells1.copy()
    score = -100000
    maxScore = -100000
    best_row = -1
    best_col = -1
    for row in range(board_size):
        for col in range(board_size):
            if tmp_cells[row][col] == 0:
                # tmp_cells[row][col] = -1
                tmp_cells[row][col] = 1
                score = esctimate(tmp_cells)
                if score > maxScore:
                    maxScore = score
                    best_row = row
                    best_col = col
                tmp_cells[row][col] = 0
    return (best_row, best_col)

# def best_move_optimize(cells1):
#     tmp_cells = cells1.copy()
#     score = -100000
#     maxScore = -100000
#     best_row = -1
#     best_col = -1
#     for row in range(board_size):
#         for col in range(board_size):
#             if tmp_cells[row][col] == 0:
#                 # tmp_cells[row][col] = -1
#                 tmp_cells[row][col] = 1
#                 score = esctimate_optimize(row, col, tmp_cells)
#                 if score > maxScore:
#                     maxScore = score
#                     best_row = row
#                     best_col = col
#                 tmp_cells[row][col] = 0
#     return (best_row, best_col)
def start_game():
    my_agent.epsilon = 0
    draw_board()
    computer()

start_game()


