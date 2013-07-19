#!/usr/bin/python3
#-*- coding:utf-8 -*-

from Window import Window
from Image import Image
from Label import Label
from Button import Button
from CheckBox import CheckBox
from CheckCircle import CheckCircle
from Widget import *
from Layout import Layout
from Frame import Frame
from SelectionMenu import SelectionMenu
from TextArray import TextArray
from Label import Label
from Slide import Slide

import sfml as sf
import time
import cProfile
import pstats
import io


#pro = cProfile.Profile()
#pro.enable()

window = Window(sf.VideoMode(800,600,32), "teste", backgroundColor = sf.Color.GREEN, framerateLimit=5)

#textArray = TextArray(window, label=Label(None, "coucou je viens d'écrire \n mon premier text array, j'espère qu'il vous plaira mes jeunes amis !", font=sf.Font.from_file("DejaVuSans.ttf")), alignment=Position.Center)
#textArray.setPos(sf.Vector2(150, 150))

#background0 = Image(None, "Ressources/Images/image.jpg", delTextureCreated = False)
#background1 = Image(None, "Ressources/Images/FirstMenu.jpg", delTextureCreated = False)
#window.backgroundImage = background0

slide = Slide(window, rect=sf.Rectangle(sf.Vector2(30, 30), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))


slide.clipRect = sf.Rectangle(sf.Vector2(10,0), sf.Vector2(300, 20))

#frame = Frame(window, sf.Rectangle(sf.Vector2(10, 10), sf.Vector2(400, 300)), title="frame")
#layout = SelectionMenu(window, permanentActivation=True)
#layout.spacing = sf.Vector2(10, 10)
box = CheckBox(window, sf.Rectangle(sf.Vector2(100, 100), sf.Vector2(50, 50)))
#box2 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
#box3 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(50, 50)))
#box4 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(100, 100)))
#box5 = CheckBox(None, sf.Rectangle(sf.Vector2(20, 20), sf.Vector2(100, 100)))
#layout.addWidget(box, sf.Vector2(1, 0), sf.Vector2(1, 1))
#layout.addWidget(box2, sf.Vector2(1, 1), sf.Vector2(1, 1))
#layout.addWidget(box3, sf.Vector2(0, 2), sf.Vector2(1, 1))
#layout.addWidget(box4, sf.Vector2(2, 1), sf.Vector2(1, 1))
#layout.addWidget(box5, sf.Vector2(1, 1), sf.Vector2(1, 1))
#layout.posOrigin = Position.Center
#layout.pos = sf.Vector2(400, 300)
#layout.setAllActiveMouseKeyboard(sf.Keyboard.RETURN, sf.Mouse.LEFT)
#layout.canFocus = False

#print(layout[(sf.Vector2(0, 1))])


while window.is_open:
	window.update()
#	print(slide._forground.getPos(False, True))
#	print(slide.sizeOnScreen)
#	print(Widget.widgetFocus)
#	print(slide._background.isSelect)
	#if window.event.getOnePressedKeys(sf.Keyboard.LEFT):
	#	window.backgroundImage = None
	#	window.backgroundImage = background1
	#elif window.event.getOnePressedKeys(sf.Keyboard.RIGHT):
	#	window.backgroundImage = None
	#	window.backgroundImage = background0
	

#pro.disable()
#stat = pstats.Stats(pro)
#stat.sort_stats("tottime")
#stat.print_stats()
