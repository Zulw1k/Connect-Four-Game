from tkinter import *
import config
import logic
import time
import sqlite3
from datetime import datetime


# BUTTON FUNCTIONS

def new_game(game_button, button_pause, image_grid, image_player1, image_player2,
             label_move, button_move, label_scoreboard, window):
    config.board = list(0 for x in range(config.rows) for y in range(config.columns))
    config.moves = 0
    config.player_turn = 1
    config.pause = False
    label_scoreboard['text'] = str(config.player1score) + ' - ' + str(config.draw) + ' - ' + str(config.player2score)
    button_move['image'] = image_player1
    label_move['text'] = 'Current move: ' + str(config.moves)
    for row in range(config.rows):
        for col in range(config.columns):
            game_button[row][col].config(image=image_grid, state=DISABLED, bg='white')
    next_round(game_button, button_pause, image_grid, image_player1, image_player2,
               label_move, button_move, label_scoreboard, window)


def pause(button_pause):
    if config.pause:
        button_pause['text'] = 'Pause'
        config.pause = False
        config.var.set(1)
    else:
        button_pause['text'] = 'Unpause'
        config.pause = True


def autostart(button_autostart):
    if not config.autostart:
        button_autostart['bg'] = 'green'
        config.autostart = True
    else:
        button_autostart['bg'] = 'red'
        config.autostart = False


def turbo(button_turbo):
    if not config.turbo:
        button_turbo['bg'] = 'green'
        config.turbo = True
    else:
        button_turbo['bg'] = 'red'
        config.turbo = False


def exit_game(window):
    config.var.set(1)
    window.destroy()


def click(button, image_player1, image_player2):
    if config.board[int(button["text"])] == 0:
        if config.player_turn == 1:
            config.board[int(button["text"])] = 1
            button["image"] = image_player1
        else:
            config.board[int(button["text"])] = 2
            button['image'] = image_player2
    button['state'] = DISABLED


def choose_player1(event):
    config.player1score = 0
    config.player2score = 0
    config.draw = 0
    config.p1 = config.agent_dict[event.widget.get()]


def choose_player2(event):
    config.player1score = 0
    config.player2score = 0
    config.draw = 0
    config.p2 = config.agent_dict[event.widget.get()]


# def show_query():
#     conn = sqlite3.connect('connectfour_database.db')
#     c = conn.cursor()
#
#     # Query database
#     c.execute('SELECT * FROM game_history')
#     rec = c.fetchall()
#     print(rec)
#     # Commit Changes
#     conn.commit()
#
#     # Close connection
#     conn.close()

# OTHER FUNCTIONS

def next_round(game_button, button_pause, image_grid, image_player1, image_player2,
               label_move, button_move, label_scoreboard, window):
    window.update()
    valid_moves = logic.get_valid_moves(config.board)
    if config.player_turn == 1:
        if type(config.p1).__name__ == 'Player':
            config.p1.make_move(config.rows, config.columns, game_button, valid_moves, window, config.var)
            button_move['image'] = image_player2
        else:
            c = config.p1.make_move()
            r = valid_moves[c]
            click(game_button[r][c], image_player1, image_player2)
            button_move['image'] = image_player2
    else:
        if type(config.p2).__name__ == 'Player':
            config.p2.make_move(config.rows, config.columns, game_button, valid_moves, window, config.var)
            button_move['image'] = image_player1
        else:
            c = config.p2.make_move()
            r = valid_moves[c]
            click(game_button[r][c], image_player1, image_player2)
            button_move['image'] = image_player1

    if config.turbo:
        time.sleep(0.05)
    else:
        time.sleep(0.5)

    if config.pause:
        window.wait_variable(config.var)

    config.moves += 1
    label_move['text'] = 'Current move: ' + str(config.moves)

    win = logic.check_win()
    window.update()
    if win:
        if config.player_turn == 1:
            db_update(1)
            print(str(type(config.p1).__name__) + ' ' + str(config.player_turn) + ' win!')
            config.player1score += 1
        else:
            db_update(2)
            print(str(type(config.p2).__name__) + ' ' + str(config.player_turn) + ' win!')
            config.player2score += 1

        for row in range(config.rows):
            for col in range(config.columns):
                game_button[row][col]['state'] = DISABLED
        if config.autostart:
            time.sleep(0.2)
            new_game(game_button, button_pause, image_grid, image_player1, image_player2,
                     label_move, button_move, label_scoreboard, window)
        else:
            window.wait_variable(config.var)

    elif config.moves == config.rows * config.columns:
        db_update(1/2)
        if config.autostart:
            time.sleep(0.2)
            new_game(game_button, button_pause, image_grid, image_player1, image_player2,
                     label_move, button_move, label_scoreboard, window)
        else:
            window.wait_variable(config.var)

    else:
        config.player_turn = (config.player_turn % 2) + 1
        next_round(game_button, button_pause, image_grid, image_player1, image_player2,
                   label_move, button_move, label_scoreboard, window)


def db_update(winner):
    if winner == 1:
        win = str(1)
    elif winner == 1/2:
        win = str(1/2)
    else:
        win = str(2)

    conn = sqlite3.connect('connectfour_database.db')
    c = conn.cursor()

    c.execute("INSERT INTO game_history VALUES (:player1, :player2, :result, :moves, :date, :time)",
              {
                  'player1': str(type(config.p1).__name__),
                  'player2': str(type(config.p2).__name__),
                  'result': str(win),
                  'moves': int(config.moves),
                  'date': str(datetime.now().date()),
                  'time': str(datetime.now().strftime("%H:%M:%S"))
              })
    conn.commit()
    conn.close()


