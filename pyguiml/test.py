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
from TextArray import *
from Label import Label
from Slide import Slide
from ProgressBar import ProgressBar

import sfml as sf
import time
import cProfile
import pstats
import io


#pro = cProfile.Profile()
#pro.enable()

window = Window(sf.VideoMode(800,600,32), "teste", backgroundColor = sf.Color.RED, framerateLimit=3)
#progress = ProgressBar(window, sf.Rectangle(sf.Vector2(), sf.Vector2(100, 20)))

#progress2 = ProgressBar(window, sf.Rectangle(sf.Vector2(0, 200), sf.Vector2(100, 20)))
#progress3 = ProgressBar(window, sf.Rectangle(sf.Vector2(0, 300), sf.Vector2(100, 20)))
#progress4 = ProgressBar(window, sf.Rectangle(sf.Vector2(0, 400), sf.Vector2(100, 20)))
#progress5 = ProgressBar(window, sf.Rectangle(sf.Vector2(0, 430), sf.Vector2(100, 20)))
textArray = TextArray(window, label=Label(None, "coucou je viens d'écrire mon premier text array, j'espère que tu a bien rigolé avec tes amis, parce que maintenant c'est terminé !", characterSize = 20, font=sf.Font.from_file("DejaVuSans.ttf")), alignment=Position.Center, cutStyle =Cut.Character, sizeX = 600)
#textArray.setPos(sf.Vector2(150, 150))

#background0 = Image(None, "Ressources/Images/image.jpg", delTextureCreated = False)
#background1 = Image(None, "Ressources/Images/FirstMenu.jpg", delTextureCreated = False)
#window.backgroundImage = background0

slide = Slide(window, rect=sf.Rectangle(sf.Vector2(300, 30), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))
print(slide.howActiveKeyboard)
#slide.clipRect=sf.Rectangle(sf.Vector2(), sf.Vector2(500, 10))
#slide._forground.clipRect = sf.Rectangle(sf.Vector2(7, 7), sf.Vector2(20, 15))
#slide2 = Slide(window, rect=sf.Rectangle(sf.Vector2(100, 230), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))
#slide3 = Slide(window, rect=sf.Rectangle(sf.Vector2(100, 330), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))
#slide4 = Slide(window, rect=sf.Rectangle(sf.Vector2(100, 430), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))
#slide5 = Slide(window, rect=sf.Rectangle(sf.Vector2(100, 470), sf.Vector2(500, 20)), step=1, inStep=5, values=sf.Vector2(0, 50))


#slide.clipRect = sf.Rectangle(sf.Vector2(10,10), sf.Vector2(300, 20))

#frame = Frame(window, sf.Rectangle(sf.Vector2(10, 10), sf.Vector2(400, 300)), title="frame")
#layout = SelectionMenu(window, permanentActivation=True)
#layout.spacing = sf.Vector2(10, 10)
#box = CheckBox(window, sf.Rectangle(sf.Vector2(100, 100), sf.Vector2(50, 50)))
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
	print(window.event.mousePos)
#	progress.currentValue = slide.currentValue/50
#	progress2.currentValue = slide2.currentValue/50
#	progress3.currentValue = slide3.currentValue/50
#	progress4.currentValue = slide4.currentValue/50
#	progress5.currentValue = slide5.currentValue/50
#	print(progress.forgroundWidget is progress2.forgroundWidget)
#	print(slide._forground.getPos(False, True))
#	print(slide._forground.getRectOnScreen(True))
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
