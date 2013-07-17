from Button import Button
from Widget import *
from Layout import Layout
from EventManager import EventManager
from Active import Active
import sfml as sf


class ButtonMenu(Layout, Active):
	def __init__(self, parent=None, rect=sf.Rectangle,\
			alignment = Position.Center, spacing=sf.Vector2(0, 0), \
			autoDefineSize = True, select=False, active=False, \
			alwaysUpdateSelection=True, alwaysUpdateActivation=True, \
			permanentSelection=False, permanentActivation=False, \
			changeRight = sf.Keyboard.RIGHT, changeLeft = sf.Keyboard.LEFT,\
			changeTop = sf.Keyboard.UP, changeBottom = sf.Keyboard.DOWN):
		Layout.__init__(parent, rect, alignment, spacing, autoDefineSize)
		Active.__init__(self, select, active, alwaysUpdateSelection,\
				alwaysUpdateActivation, permanentSelection, permanentActivation)
		self.canFocus=False
		self.changeLeft = changeLeft
		self.changeRight = changeRight
		self.changeTop = changeTop
		self.changeBottom = changeBottom
		self._currentSelect = None

	def update(self, render=None):
		Active.__init__(self)
		if self.isActive:
			for child in self._child:
				if child.isSelect and child is not self._currentSelect:
					self._currentSelect = child
					break

			self._deselectOtherWidget()


			if not self._currentSelect and self.child:
				self._currentSelect = self.child[0]

			if self.event and self._child:
				posCurrentSelect = self.getWidgetPosition(self._currentSelect)
				caseCurrentSelect = self.getWidgetCase(self._currentSelect)

				if self.event.getOnePressedKeys(changeLeft):
					done = False
					y = posCurrentSelect.y
					for x in range(posCurrentSelect.x, -1, -1):
						child = self.__getitem__(sf.Vector2(x, y))
						if child:
							done = True
							self._currentSelect = child

					if not done:
						for x in range(len(self._widget), posCurrentSelect.x, -1):
							child = self.__getitem__(sf.Vector2(x, y))
							if child:
								done = True
								self._currentSelect = child

				elif self.event.getOnePressedKeys(changeRight):
					done = False
					y = posCurrentSelect.y
					for x in range(posCurrentSelect.x + caseCurrentSelect.x, \
							len(self._widget)):
						child = self.__getitem__(sf.Vector2(x, y))
						if child:
							done = True
							self._currentSelect = child

					if not done:
						for x in range(0, posCurrentSelect.x):
							child = self.__getitem__(sf.Vector2(x, y))
							if child:
								done = True
								self._currentSelect = child

				elif self.event.getOnePressedKeys(changeTop):
					done = False
					x = posCurrentSelect.x
					for y in range(posCurrentSelect.y, -1, -1):
						child = self.__getitem__(sf.Vector2(x, y))
						if child:
							done = True
							self._currentSelect = child

					if not done:
						for y in range(len(self._widget), posCurrentSelect.y, -1):
							child = self.__getitem__(sf.Vector2(x, y))
							if child:
								done = True
								self._currentSelect = child
				elif self.event.getOnePressedKeys(changeBottom):
					done = False
					x = posCurrentSelect.x
					for y in range(posCurrentSelect.y + caseCurrentSelect.y, \
							len(self._widget)):
						child = self.__getitem__(sf.Vector2(x, y))
						if child:
							done = True
							self._currentSelect = child

					if not done:
						for y in range(0, posCurrentSelect.y):
							child = self.__getitem__(sf.Vector2(x, y))
							if child:
								done = True
								self._currentSelect = child

		Layout.update(self, render)

	def setAllActiveMouseKeyboard(self, keyboard=None, mouse=None):
		for child in self.child:
			child.howActiveKeyboard = keyboard
			child.howActiveMouse = mouse

	def _deselectOtherWidget(self):
		for child in self._child:
			if child is not self._currentSelect:
				child.permanentSelection = False
			self._currentSelect.permanentSelection = True

	def _setCurrentSelection(self, value):
		widget = value
		if type(value) is sf.Vector2:
			widget = self.__getitem__(value)
		if widget:
			self._currentSelect = widget
			self._deselectOtherWidget()


	currentSelect = property(lambda self:self._currentSelect, \
			_setCurrentSelection)
