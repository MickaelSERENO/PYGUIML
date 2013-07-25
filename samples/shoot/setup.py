#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
sys.path.append("../../")

from Game import Game
import pyguiml

game = Game()

while game.is_open:
	game.update()
