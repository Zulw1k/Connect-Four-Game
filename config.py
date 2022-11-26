from tkinter import *
from tkinter import ttk
import Agents
import numpy as np


# config variables
columns = 7
rows = 6
in_a_row = 4
player_turn = 1

# game variables
player1score = 0
player2score = 0
draw = 0
moves = 0
counter = 0
var = 0
turbo = False
pause = False
autostart = False
board = list(0 for x in range(rows) for y in range(columns))
game_button = [[0 for i in range(columns)] for j in range(rows)]

agent_dict = {
    'player': Agents.Player(),
    'bot_random': Agents.RandomAgent(),
    'bot_middle': Agents.MiddleAgent(),
    'bot_leftmost': Agents.LeftmostAgent(),
    'bot_q1': Agents.Q1(),
    'bot_heuristic ': Agents.Heuristic(),
    'bot_heuristic_upgraded ': Agents.HeuristicUpgrade(),
    'bot_MinMax ': Agents.MinMax(),
    'bot_AlphaBetaPrunning': Agents.AlphaBetaMiniMax()
}

p1 = Agents.Player()
p2 = agent_dict['bot_q1']
