from Widget import *
from Active import Active
from Label import Label
from Image import Image
from sfml import sfml
import decorator

class EditText(Widget, Active):
	def __init__(self, parent=None, rect = sf.Rectangle(), \
			defaultLabel=Label(), defaultBackground=Image(), \
			defaultForground=Image(), maxSize = sf.Vector2(-1,-1),\
			spacing = sf.Vector2(0,0))

		Widget.__init__(self, parent, rect)
		Active.__init__(self)

		self._maxSize = maxSize

		self._background=defaultBackground
		self._forground = defaultForground
		self._label = list()
		self._spacing = spacing
		self._cursorPosition = sf.Vector2(0,0)

		#AddFeature for many Label

		self.setSize(self._label.virtualSize)

		self._minSize = rect.size

		self._background.rect = self.virtualRect
		self._forground.origin = 0.1*self.virtualSize
		self._forground.rect = self.virtualRect + sf.Rectangle(sf.Vector2(), \
				0.8*self.virtualSize)

		self._background.canFocus = self._forground.canFocus = False
		self.howDisactiveKeyboard = sf.Keyboard.ESCAPE
		self.howDisactiveMouse = sf.Mouse.LEFT

	@decorator.forUpdate
	def update(self, render=None):
		Active.update(self)
		if self.isActive and self._event:
			if self._event.getOnePressedKeys(sf.Keyboard.LEFT):


		Widget.update(self, render)

	def setSize(self, size, resetMinSize = False):
		pass

	def setPos(self, pos, withOrigin=True):
		pass

	def howActiveIt(self):
		if self._event:
			if Widget.widgetFocus is not in self._labelList and \
					self._event.getOneMouseClicked(self.howActiveMouse) or\
					self._event.getOnePressedKeys(self.howActiveKeyboard):

	def howDisactive(self):
		if self._event:
			if Widget.widgetFocus is in self._labelList and \
					self._event.getOneMouseClicked(self.howDisactiveMouse) or\
					self._event.getOnePressedKeys(self.howDisactiveKeyboard):
				return True
		else:
			return False

	def activeIt(self):
		widgetFocus = Widget.widgetFocus

	def disactiveIt(self):
		return
