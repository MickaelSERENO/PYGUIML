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
layout = Layout(window, autoDefineSize =True)
layout.spacing = sf.Vector2(10, 10)
box = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
box2 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
box3 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
box4 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(100, 100)))
layout.addWidget(box, sf.Vector2(0, 0), sf.Vector2(1, 1))
layout.addWidget(box2, sf.Vector2(1, 0), sf.Vector2(3, 1))
layout.addWidget(box3, sf.Vector2(0, 1), sf.Vector2(2, 1))
layout.addWidget(box4, sf.Vector2(4, 0), sf.Vector2(1, 1))

while window.is_open:
	window.update()
#	print(box2.origin)
