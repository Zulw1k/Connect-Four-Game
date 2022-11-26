import random
from tkinter import *
import tkinter as tk
import logic
import numpy as np


class Player:
    def make_move(self, rows, columns, button, valid_moves, window, var):
        for row in range(rows):
            for col in range(columns):
                button[row][col]['state'] = DISABLED
        for i in valid_moves:
            button[valid_moves[i]][i]['state'] = NORMAL
        window.wait_variable(var)


class RandomAgent:
    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        return random.choice(list(valid_moves.keys()))


class MiddleAgent:
    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        moves = list(valid_moves.keys())
        return moves[len(list(valid_moves.keys()))//2]


class LeftmostAgent:
    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        return list(valid_moves.keys())[0]


class Q1:
    def check_winning_move(self, grid, rows, columns, in_row, player_turn):
        # horizontal
        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if window.count(player_turn) == in_row:
                    return True
        # vertical
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if window.count(player_turn) == in_row:
                    return True
        # positive diagonal
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if window.count(player_turn) == in_row:
                    return True
        # negative diagonal
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if window.count(player_turn) == in_row:
                    return True
        return False

    def make_prediction_board(self, grid, player_turn, prediction_row, prediction_col):
        next_grid = grid.copy()
        next_grid[prediction_row][prediction_col] = player_turn
        return next_grid

    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        grid = np.asarray(board).reshape(rows, columns)

        for column in list(valid_moves.keys()):
            prediction_board = self.make_prediction_board(grid, player_turn, valid_moves[column], column)
            if self.check_winning_move(prediction_board, rows, columns, in_row, player_turn):
                return column
        for column in list(valid_moves.keys()):
            prediction_board = self.make_prediction_board(grid, player_turn % 2 + 1, valid_moves[column], column)
            if self.check_winning_move(prediction_board, rows, columns, in_row, player_turn%2+1):
                return column
        return random.choice(list(valid_moves.keys()))


class Heuristic:
    def count_windows(self, grid, num_discs, player_turn, rows, columns, in_row):
        num_windows = 0
        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        return num_windows

    def get_heuristic(self, grid, player_turn, rows, columns, in_row):
        num_threes = self.count_windows(grid, 3, player_turn, rows, columns, in_row)
        num_fours = self.count_windows(grid, 4, player_turn, rows, columns, in_row)
        num_threes_opp = self.count_windows(grid, 3, player_turn % 2 + 1, rows, columns, in_row)
        score = num_threes - 1e2 * num_threes_opp + 1e6 * num_fours
        return score

    def check_window(self, window, num_discs, player_turn, in_row):
        return window.count(player_turn) == num_discs and window.count(0) == in_row - num_discs

    def make_prediction_board(self, grid, player_turn, prediction_row, prediction_col):
        next_grid = grid.copy()
        next_grid[prediction_row][prediction_col] = player_turn
        return next_grid

    def score_move(self, grid, player_turn, rows, columns, in_row, prediction_row, prediction_col):
        next_grid = self.make_prediction_board(grid, player_turn, prediction_row, prediction_col)
        score = self.get_heuristic(next_grid, player_turn, rows, columns, in_row)
        return score

    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        grid = np.asarray(board).reshape(rows, columns)
        scores = {}
        for column in list(valid_moves.keys()):
            scores[column] = self.score_move(grid,player_turn, rows, columns, in_row, valid_moves[column], column)

        col_with_max_score = [key for key in scores.keys() if scores[key] == max(scores.values())]

        print(scores)
        print(col_with_max_score)
        return random.choice(col_with_max_score)


class HeuristicUpgrade:
    def count_windows(self, grid, num_discs, player_turn, rows, columns, in_row):
        num_windows = 0
        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        return num_windows

    def get_heuristic(self, grid, player_turn, rows, columns, in_row, A=1000, B=100, C=10, D=-10, E=-100):
        num_twos = self.count_windows(grid, 2, player_turn, rows, columns, in_row)
        num_threes = self.count_windows(grid, 3, player_turn, rows, columns, in_row)
        num_fours = self.count_windows(grid, 4, player_turn, rows, columns, in_row)
        num_twos_opp = self.count_windows(grid, 2, player_turn % 2 + 1, rows, columns, in_row)
        num_threes_opp = self.count_windows(grid, 3, player_turn % 2 + 1, rows, columns, in_row)
        score = A * num_fours + B * num_threes + C * num_twos + D * num_twos_opp + E * num_threes_opp
        return score

    def check_window(self, window, num_discs, player_turn, in_row):
        return window.count(player_turn) == num_discs and window.count(0) == in_row - num_discs

    def make_prediction_board(self, grid, player_turn, prediction_row, prediction_col):
        next_grid = grid.copy()
        next_grid[prediction_row][prediction_col] = player_turn
        return next_grid

    def score_move(self, grid, player_turn, rows, columns, in_row, prediction_row, prediction_col):
        next_grid = self.make_prediction_board(grid, player_turn, prediction_row, prediction_col)
        score = self.get_heuristic(next_grid, player_turn, rows, columns, in_row)
        return score

    def make_move(self):
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        valid_moves = logic.get_valid_moves(board)
        grid = np.asarray(board).reshape(rows, columns)
        scores = {}
        for column in list(valid_moves.keys()):
            scores[column] = self.score_move(grid, player_turn, rows, columns, in_row, valid_moves[column], column)

        col_with_max_score = [key for key in scores.keys() if scores[key] == max(scores.values())]
        return random.choice(col_with_max_score)


class MinMax:
    def check_window(self, window, num_discs, player_turn, in_row):
        return window.count(player_turn) == num_discs and window.count(0) == in_row - num_discs

    def count_windows(self, grid, num_discs, player_turn, rows, columns, in_row):
        num_windows = 0
        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        return num_windows

    def make_prediction_board(self, grid, playerturn, pred_row, pred_col):
        next_grid = grid.copy()
        next_grid[pred_row][pred_col] = playerturn
        return next_grid

    def score_move(self, grid, player_turn, rows, columns, in_row, prediction_row, prediction_col, n_steps):
        next_grid = self.make_prediction_board(grid, player_turn, prediction_row, prediction_col)
        score = self.minimax(next_grid, n_steps - 1, False, player_turn, rows, columns, in_row)
        return score

    def get_heuristic(self, grid, player_turn, rows, columns, in_row, A=10000, B=100, C=10, D=-100, E=-1000):
        num_twos = self.count_windows(grid, 2, player_turn, rows, columns, in_row)
        num_threes = self.count_windows(grid, 3, player_turn, rows, columns, in_row)
        num_fours = self.count_windows(grid, 4, player_turn, rows, columns, in_row)
        num_twos_opp = self.count_windows(grid, 2, player_turn % 2 + 1, rows, columns, in_row)
        num_threes_opp = self.count_windows(grid, 3, player_turn % 2 + 1, rows, columns, in_row)
        score = A * num_fours + B * num_threes + C * num_twos + D * num_twos_opp + E * num_threes_opp
        return score

    def is_terminal_window(self, window, in_row):
        return window.count(1) == in_row or window.count(2) == in_row

    def is_terminal_node(self, grid, rows, columns, in_row):
        if list(grid[0, :]).count(0) == 0:
            return True

        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.is_terminal_window(window, in_row):
                    return True
        return False

    def minimax(self, node, depth, maximizing_player, mark, rows, columns, in_row):
        valid_moves = logic.get_valid_moves(node)
        print('Valid moves: ' + str(valid_moves))
        is_terminal = self.is_terminal_node(node, rows, columns, in_row)
        if depth == 0 or is_terminal:
            return self.get_heuristic(node, mark, rows, columns, in_row)
        if maximizing_player:
            value = -np.Inf
            for column in list(valid_moves.keys()):
                prediction_board = self.make_prediction_board(node, mark, valid_moves[column], column)
                value = max(value, self.minimax(prediction_board, depth - 1, False, mark, rows, columns, in_row))
            return value
        else:
            value = np.Inf
            for column in list(valid_moves.keys()):
                prediction_board = self.make_prediction_board(node, mark % 2+1, valid_moves[column], column)
                value = min(value, self.minimax(prediction_board, depth - 1, True, mark, rows, columns, in_row))
            return value

    def make_move(self):
        n_steps = 4
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        grid = np.asarray(board).reshape(rows, columns)
        valid_moves = logic.get_valid_moves(board)
        scores = valid_moves.copy()

        for col in valid_moves.keys():
            score = self.score_move(grid, player_turn, rows, columns, in_row, valid_moves[col], col, n_steps)
            print('FOR col: ' + str(col) + ' score : ' + str(score))
            scores[col] = score
        print(scores)

        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        print(max_cols)
        return random.choice(max_cols)


class AlphaBetaMiniMax:
    def check_window(self, window, num_discs, player_turn, in_row):
        return window.count(player_turn) == num_discs and window.count(0) == in_row - num_discs

    def count_windows(self, grid, num_discs, player_turn, rows, columns, in_row):
        num_windows = 0
        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.check_window(window, num_discs, player_turn, in_row):
                    num_windows += 1
        return num_windows

    def make_prediction_board(self, grid, player_turn, predicted_row, predicted_col):
        next_grid = grid.copy()
        next_grid[predicted_row][predicted_col] = player_turn
        return next_grid

    def score_move(self, grid, player_turn, rows, columns, in_row, predicted_row, predicted_col, n_steps):
        next_grid = self.make_prediction_board(grid, player_turn, predicted_row, predicted_col)
        score = self.alphabetaminimax(next_grid, n_steps - 1, False, player_turn, rows, columns, in_row)
        return score

    def get_heuristic(self, grid, player_turn, rows, columns, in_row, A=100000, B=1000, C=10, D=-10, E=-1000000):
        num_twos = self.count_windows(grid, 2, player_turn, rows, columns, in_row)
        num_threes = self.count_windows(grid, 3, player_turn, rows, columns, in_row)
        num_fours = self.count_windows(grid, 4, player_turn, rows, columns, in_row)
        num_twos_opp = self.count_windows(grid, 2, player_turn % 2 + 1, rows, columns, in_row)
        num_threes_opp = self.count_windows(grid, 3, player_turn % 2 + 1, rows, columns, in_row)
        score = A * num_fours + B * num_threes + C * num_twos + D * num_twos_opp + E * num_threes_opp
        return score

    def is_terminal_window(self, window, in_row):
        return window.count(1) == in_row or window.count(2) == in_row

    def is_terminal_node(self, grid, rows, columns, in_row):
        if list(grid[0, :]).count(0) == 0:
            return True

        for row in range(rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[row, col:col + in_row])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(rows - (in_row - 1)):
            for col in range(columns):
                window = list(grid[row:row + in_row, col])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(rows - (in_row - 1)):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row + in_row), range(col, col + in_row)])
                if self.is_terminal_window(window, in_row):
                    return True
        for row in range(in_row - 1, rows):
            for col in range(columns - (in_row - 1)):
                window = list(grid[range(row, row - in_row, -1), range(col, col + in_row)])
                if self.is_terminal_window(window, in_row):
                    return True
        return False

    def alphabetaminimax(self, node, depth, maximizing_player, mark, rows, columns, in_row, alpha=-np.inf, beta=np.inf):
        valid_moves = logic.get_valid_moves(node)
        print('Valid moves: ' + str(valid_moves))
        is_terminal = self.is_terminal_node(node, rows, columns, in_row)
        if depth == 0 or is_terminal:
            return self.get_heuristic(node, mark, rows, columns, in_row)
        if maximizing_player:
            value = -np.Inf
            for column in list(valid_moves.keys()):
                prediction_board = self.make_prediction_board(node, mark, valid_moves[column], column)
                value = max(value, self.alphabetaminimax(prediction_board, depth - 1, False,
                                                         mark, rows, columns, in_row, alpha, beta))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = np.Inf
            for column in list(valid_moves.keys()):
                prediction_board = self.make_prediction_board(node, mark % 2+1, valid_moves[column], column)
                value = min(value, self.alphabetaminimax(prediction_board, depth - 1, True,
                                                         mark, rows, columns, in_row, alpha, beta))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value

    def make_move(self):
        n_steps = 4
        board, rows, columns, player_turn, in_row, game_button = logic.get_variables()
        grid = np.asarray(board).reshape(rows, columns)
        valid_moves = logic.get_valid_moves(board)
        scores = valid_moves.copy()

        for col in valid_moves.keys():
            score = self.score_move(grid, player_turn, rows, columns, in_row, valid_moves[col], col, n_steps)
            scores[col] = score

        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        return random.choice(max_cols)
