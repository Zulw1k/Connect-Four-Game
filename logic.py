import numpy as np
import config


def get_valid_moves(board):
    reshaped_board = np.asarray(board).reshape(config.rows, config.columns)
    cords_row = []
    cords_col = []
    valid_columns = [col for col in range(config.columns) if 0 in reshaped_board[:, col]]
    valid_moves = {}
    for col in list(valid_columns):
        for row in range(config.rows - 1, -1, -1):
            if reshaped_board[row, col] == 0:
                cords_row.append(row)
                cords_col.append(col)
    for i in range(len(cords_col)):
        if cords_col[i] != cords_col[i-1]:
            valid_moves[cords_col[i]] = cords_row[i]
        elif len(valid_columns) == 1:
            valid_moves[cords_col[i]] = cords_row[i]
            break
    return valid_moves


def check_win():
    grid = np.asarray(config.board).reshape(config.rows, config.columns)
    for row in range(config.rows):
        for col in range(config.columns - (config.in_a_row - 1)):
            window = list(grid[row,col:col+config.in_a_row])
            if window.count(config.player_turn) == config.in_a_row:
                for i in range(config.in_a_row):
                    config.game_button[row][col+i]['bg'] = 'blue'
                return True
    for row in range(config.rows - (config.in_a_row - 1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.in_a_row,col])
            if window.count(config.player_turn) == config.in_a_row:
                for i in range(config.in_a_row):
                    config.game_button[row+i][col]['bg'] = 'blue'
                return True
    for row in range(config.rows - (config.in_a_row - 1)):
        for col in range(config.columns - (config.in_a_row - 1)):
            window = list(grid[range(row, row+config.in_a_row), range(col, col+config.in_a_row)])
            if window.count(config.player_turn) == config.in_a_row:
                for i in range(config.in_a_row):
                    config.game_button[row+i][col+i]['bg'] = 'blue'
                return True
    for row in range(config.in_a_row-1, config.rows):
        for col in range(config.columns - (config.in_a_row - 1)):
            window = list(grid[range(row, row-config.in_a_row, -1), range(col, col+config.in_a_row)])
            if window.count(config.player_turn) == config.in_a_row:
                for i in range(config.in_a_row):
                    config.game_button[row-i][col+i]['bg'] = 'blue'
                return True
    return False


def get_variables():
    board = config.board
    rows = config.rows
    columns = config.columns
    player_turn = config.player_turn
    in_row = config.in_a_row
    game_button = config.game_button
    return board, rows, columns, player_turn, in_row, game_button
