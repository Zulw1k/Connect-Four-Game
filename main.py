from tkinter import *
from tkinter import ttk
import buttonfunctions
import config
import sqlite3

# FRONT

# window options

root = Tk()
root.resizable(False, False)
root.title("Connect Four Game")
grid = Frame(root)
grid.grid(sticky=N + S + E + W, column=0, row=7, padx=40, pady=20)
config.var = IntVar()

# images
red = PhotoImage(file='images/red50x50.png')
yellow = PhotoImage(file='images/yellow50x50.png')
white = PhotoImage(file='images/white50x50.png')
gray = PhotoImage(file='images/gray50x50.png')

# init game buttons
for row in range(config.rows):
    for col in range(config.columns):
        config.game_button[row][col] = Button(grid, image=gray, text=str(config.counter))
        config.game_button[row][col].grid(row=row, column=col)
        config.game_button[row][col]["state"] = DISABLED
        config.counter += 1

# other buttons
Label(root, text='Player 1').place(x=40, y=0)
Label(root, text='Player 2').place(x=340, y=0)
Label(root, text='SCORE').place(x=250, y=0)
Label(root, text='Player turn:', bd=1, relief='ridge').place(x=60, y=75)
button_move = Button(root, image=red)
label_moves = Label(root, text='Current move: ' + str(config.moves), bd=1, relief='ridge')
label_scoreboard = Label(root, text=str(config.player1score) + ' - ' +
                                    str(config.draw) + ' - ' +
                                    str(config.player2score),
                         bd=1, relief='ridge', height=1, width=10)

button_newgame = Button(root, text='New game', height=1, width=10,
                        command=lambda: buttonfunctions.new_game
                        (config.game_button, button_pause, white, red, yellow,
                         label_moves, button_move, label_scoreboard, root))

button_turbo = Button(root, text='Turbo', bg='red', height=1, width=10,
                      command=lambda: buttonfunctions.turbo(button_turbo))

button_autostart = Button(root, text='Autostart', bg='red', height=1, width=10,
                          command=lambda: buttonfunctions.autostart(button_autostart))

button_pause = Button(root, text='Pause', height=1, width=10,
                      command=lambda: buttonfunctions.pause(button_pause))

button_exit = Button(root, text='Exit', height=1, width=10, command=lambda: buttonfunctions.exit_game(root))

combobox_player1 = ttk.Combobox(root, values=list(config.agent_dict.keys()), state='readonly', height=5, width=20)
combobox_player1.current(0)
combobox_player1.bind("<<ComboboxSelected>>", buttonfunctions.choose_player1)

combobox_player2 = ttk.Combobox(root, values=list(config.agent_dict.keys()), state='readonly', height=5, width=20)
combobox_player2.current(1)
combobox_player2.bind("<<ComboboxSelected>>", buttonfunctions.choose_player2)

# buttons placing
label_moves.place(x=290, y=75)
button_move.place(x=140, y=60)
label_scoreboard.place(x=235, y=21)
combobox_player1.place(x=40, y=21)
combobox_player2.place(x=330, y=21)


Label(root, text='', height=1, width=10).grid(row=4, column=config.columns + 1) # space column
button_newgame.grid(row=1, column=config.columns + 2)
button_autostart.grid(row=6, column=config.columns + 2)
button_turbo.grid(row=5, column=config.columns + 2)
button_pause.grid(row=2, column=config.columns + 2)
button_exit.grid(row=3, column=config.columns + 2)

##Database init
# statisticsbutton = Button(root, text='Statistics', height=1, width=10, command=buttonfunctions.showquery)
# statisticsbutton.grid(row=4, column=config.columns + 2)

# conn = sqlite3.connect('connectfour_database.db')
#
# # Create cursor
# c = conn.cursor()
#
# # Create table game_id INTEGER NOT NULL PRIMARY KEY,
# c.execute("""
# CREATE TABLE game_history (
# player1 TEXT NOT NULL,
# player2 TEXT NOT NULL,
# result TEXT NOT NULL,
# moves INTEGER NOT NULL,
# date TEXT NOT NULL,
# time TEXT NOT NULL
# )""")
#
# # Commit Changes
# conn.commit()
#
# # Close connection
# conn.close()

root.mainloop()
