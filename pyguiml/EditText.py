from Widget import *
from Active import Active
from Label import Label
from Image import Image
from Button import Button
from TextArray import TextArray
import sfml as sf
import decorator

Style = enum('MultiLines', 'OneLine')
print(Style)

class EditText(Widget, Active):
	def __init__(self, parent=None, rect = sf.Rectangle(sf.Vector2(), sf.Vector2(20, 5)), \
			defaultText=None, defaultBackground=None, \
			defaultForground=None, maxSizeX = sf.Vector2(-1,-1),\
			spacing = 0, style=Style.MultiLines, percentage=0.9):

		Widget.__init__(self, parent, rect)
		Active.__init__(self)

		self._maxSize = maxSize
		self._minSize = rect.size

		if style == Style.MultiLines and not defaultText:
			defaultText = TextArray

		if not defaultBackground:
			self._background=Image(self, sf.Image(20, 20, sf.Color.MAGENTA)) 
		else:
			self._background=defaultBackground
		if not defaultForground:
			self._forground=Button(self, None, Image(None, sf.Image(20, 20,\
					sf.Color.MAGENTA)))
		else:
			self._forground = defaultForground
		self._text = defaultText
		self._spacing = spacing
		self._cursor = sf.VertexArray(sf.PrimitiveType.LINES, 2)
		self._style = style
		self._percentage = percentage
		self.keepActivation=True

		self._howActiveKeyboard=[None, sf.Keyboard.LEFT, sf.Keyboard.RIGHT, \
				sf.Keyboard.TOP, sf.Keyboard.DOWN, sf.Keyboard.ESCAPE]
		self._howActiveMouse=[sf.Mouse.LEFT]

		self._background.rect = self.rect
		self._forground.origin = Position.CENTER
		self._forground.rect = sf.Rectangle(self.pos + self.size/2, \
				percentage*self.size)

		self._background.canFocus = False

	@decorator.forUpdate
	def update(self, render=None):
		Active.update(self)
		Widget.update(self, render)
	
	@decorator.forDrawing
	def draw(self, render=None):
		if self.isActive and render:
			render.draw(self._cursor)

	def setSize(self, size, resetOrigin=True, resetMinSize = False):
		pass

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)
		self._background.pos = self.getPos(False)
		self._forground.pos = self.getPos(False) + self.size / 2

	def howActiveIt(self):
		if self.event:
			if Widget.widgetFocus is self._forground and \
					self._event.getOneMouseClicked(self.howActiveMouse[0]) or\
					self._event.getOnePressedKeys(self.howActiveKeyboard[0]):
				pass

	def howDisactive(self):
		if self.event:
			if Widget.widgetFocus is not self._forground and \
					self._event.getOneMouseClicked(self.howDisactiveMouse[0]) or\
					self._event.getOnePressedKeys(self.howDisactiveKeyboard[-1]):
				return True
		else:
			return False

	def activeIt(self, force=False):
		if self._event:
			if self._style == Style.OneLine:
				self._event.enteredText = self._text.text.string
			else:
				self._event.enteredText = self._text._label.text.string

			if self.event.getOnePressedKeys[1]:
				self.event.textCursor -= 1
			elif self.event.getOnePressedKeys[2]:
				self.event.textCursor -= 1
			elif self.event.getOnePressedKeys[3]:
				pass #Chercher ce qu'il y a au dessus
			elif self.event.getOnePressedKeys[4]:
				pass #Chercher ce qu'il y a en dessous
			elif self.event.getOneMouseClicked:
				self.event.textCursor += self.getCharacterIndex(position)

		Active.activeIt(self, True)

	def disactiveIt(self, force=False):
		if self.isActive:
			self.event.resetText
		Active.disactiveIt(self, True)

	def getCharacterIndex(self, position):
		if self._style == Style.MultiLines:
			for label in self._text._labelList:
				pass

	def updateCursorClippingPosition(self):
		pass
