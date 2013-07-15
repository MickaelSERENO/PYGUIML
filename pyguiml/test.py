#!/usr/bin/python3
#-*- coding:utf-8 -*-

from Window import Window
from Image import Image
from Label import Label
from Button import Button
from CheckBox import CheckBox
from CheckCircle import CheckCircle
from Widget import Position
from Layout import Layout
from Frame import Frame
import sfml as sf

window = Window(sf.VideoMode(800,600,32), "teste", backgroundColor = sf.Color.GREEN, framerateLimit=60)
#frame = Frame(window, sf.Rectangle(sf.Vector2(10, 10), sf.Vector2(400, 300)), title="frame")
box = CheckBox(window, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
box2 = CheckBox(window, sf.Rectangle(sf.Vector2(70, 20), sf.Vector2(50, 50)))
box3 = CheckBox(window, sf.Rectangle(sf.Vector2(90, 20), sf.Vector2(50, 50)))
box4 = CheckBox(window, sf.Rectangle(sf.Vector2(200, 20), sf.Vector2(50, 50)))
box5 = CheckBox(window, sf.Rectangle(sf.Vector2(300, 20), sf.Vector2(50, 50)))
box6 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 70), sf.Vector2(50, 50)))
box7 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 150), sf.Vector2(50, 50)))
box8 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 200), sf.Vector2(50, 50)))
box9 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 300), sf.Vector2(50, 50)))
box10 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 360), sf.Vector2(50, 50)))
box11 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 430), sf.Vector2(50, 50)))
box12 = CheckBox(window, sf.Rectangle(sf.Vector2(20, 500), sf.Vector2(50, 50)))

while window.is_open:
	window.update()
#	print(frame.isMoving())
