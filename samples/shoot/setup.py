#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
sys.path.append("../../")

from Game import Game
import pyguiml

game = Game()

while game.is_open:
	game.update()
#	print(game.child)
#	print(game.event.mousePos)
#	print(game["First Menu"].child[0].pos)
#	print(game["Option"]["Layout Menu"].getChild("Selection Menu").isActive)
#	print(game["Option"]["Layout Menu"].getChild("Selection Menu").isSelect)
