
from Button import Button
from Widget import *
from Layout import Layout
from EventManager import EventManager
from Active import Active
import sfml as sf


class SelectionMenu(Layout, Active):
	def __init__(self, parent=None, rect=sf.Rectangle(),\
			alignment = Position.Center, spacing=sf.Vector2(0, 0), \
			autoDefineSize = True, select=False, active=False, \
			alwaysUpdateSelection=True, alwaysUpdateActivation=True, \
			permanentSelection=False, permanentActivation=False, \
			changeRight = sf.Keyboard.RIGHT, changeLeft = sf.Keyboard.LEFT,\
			changeTop = sf.Keyboard.UP, changeBottom = sf.Keyboard.DOWN):
		Layout.__init__(self, parent, rect, alignment, spacing, autoDefineSize)
		Active.__init__(self, select, active, alwaysUpdateSelection,\
				alwaysUpdateActivation, permanentSelection, permanentActivation)
		self.canFocus=False
		self.changeLeft = changeLeft
		self.changeRight = changeRight
		self.changeTop = changeTop
		self.changeBottom = changeBottom
		self._currentSelect = None

	def update(self, render=None):
		Active.update(self)
		currentHowActiveMouse = None
		if self.isActive and self.isSelect:

			done = False
			for widgetList in self._widget:
				for child in widgetList:
					if isinstance(child, Active) and child.isSelect and child is not self._currentSelect:
						self._currentSelect = child
						done = True
						break
				if done:
					break

			if not self._currentSelect:
				done = False
				for widgetList in self._widget:
					for child in widgetList:
						if isinstance(child, Active):
							self._currentSelect = child
							done = True
							break
					if done:
						break
			self._deselectOtherWidget()

			if self.event and self._currentSelect:
				currentHowActiveMouse = self._currentSelect.howActiveMouse
				if not self._currentSelect.howSelect():
					self._currentSelect.howActiveMouse=[None]
				posCurrentSelect = self.getWidgetPosition(self._currentSelect)
				caseCurrentSelect = self.getWidgetCase(self._currentSelect)

				if not self.changeLeft in self._currentSelect.howActiveKeyboard and\
						self.event.getOnePressedKeys(self.changeLeft):
					if self._currentSelect.__class__.__name__ == 'Slide':
						print('change', self.changeLeft, self._currentSelect.howActiveKeyboard)
					done = False
					for x in range(posCurrentSelect.x-1, -1, -1):
						for y in range(posCurrentSelect.y, len(self._widget[x])):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break

						if done:
							break

						for y in range(0, posCurrentSelect.y):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break
						if done:
							break

					if not done:
						for x in range(len(self._widget)-1, posCurrentSelect.x, -1):
							for y in range(posCurrentSelect.y, len(self._widget[x])):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break

							if done:
								break

							for y in range(0, posCurrentSelect.y):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break

				elif not self.changeRight in self._currentSelect.howActiveKeyboard and\
						self.event.getOnePressedKeys(self.changeRight):
					done = False
					y = posCurrentSelect.y
					for x in range(posCurrentSelect.x + caseCurrentSelect.x, \
							len(self._widget)):
						for y in range(posCurrentSelect.y, len(self._widget[x])):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break

						if done:
							break

						for y in range(0, posCurrentSelect.y):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break

						if done:
							break

					if not done:
						for x in range(0, posCurrentSelect.x):
							for y in range(posCurrentSelect.y, len(self._widget[x])):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break

							for y in range(0, posCurrentSelect.y):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break

				elif not self.changeTop in self._currentSelect.howActiveKeyboard and \
						self.event.getOnePressedKeys(self.changeTop):
					done = False
					for y in range(posCurrentSelect.y-1, -1, -1):
						for x in range(posCurrentSelect.x, len(self._widget)):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break
						if done:
							break

						for x in range(0, posCurrentSelect.x):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break
						if done:
							break


					if not done:
						for y in range(len(self._widget[0])-1, posCurrentSelect.y, -1):
							for x in range(posCurrentSelect.x, len(self._widget)):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break
							for x in range(0, posCurrentSelect.x):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break
				elif not self.changeBottom in self._currentSelect.howActiveKeyboard and\
						self.event.getOnePressedKeys(self.changeBottom):
					done = False
					x = posCurrentSelect.x
					for y in range(posCurrentSelect.y + caseCurrentSelect.y, \
							len(self._widget[0])):
						for x in range(posCurrentSelect.x, len(self._widget)):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break
						if done:
							break

						for x in range(0, posCurrentSelect.x):
							child = self.__getitem__(sf.Vector2(x, y))
							if isinstance(child, Active) and child is not self._currentSelect:
								done = True
								self._currentSelect = child
								break
						if done:
							break

					if not done:
						for y in range(0, posCurrentSelect.y):
							for x in range(posCurrentSelect.x, len(self._widget)):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break
							for x in range(0, posCurrentSelect.x):
								child = self.__getitem__(sf.Vector2(x, y))
								if isinstance(child, Active) and child is not self._currentSelect:
									done = True
									self._currentSelect = child
									break
							if done:
								break
			self._deselectOtherWidget()
		else:
			if self._currentSelect:
				self._currentSelect.permanentSelection=False
				self._currentSelect.deselectIt()

		Layout.update(self, render)
		if self._currentSelect:
			self._currentSelect.howActiveMouse = currentHowActiveMouse

	def setAllActiveMouseKeyboard(self, keyboard=None, mouse=None):
		for widgetList in self._widget:
			for child in widgetList:
				if isinstance(child, Active):
					child.howActiveKeyboard = keyboard
					child.howActiveMouse = mouse

	def _deselectOtherWidget(self):
		for widgetList in self._widget:
			for child in widgetList:
				if child is not self._currentSelect:
					if isinstance(child, Active):
						child.permanentSelection = False
						child.deselectIt()
		if self._currentSelect:
			self._currentSelect.permanentSelection = True
			self._currentSelect.selectIt()

	def _setCurrentSelection(self, value):
		widget = value
		if type(value) is sf.Vector2:
			widget = self.__getitem__(value)
		if widget:
			self._currentSelect = widget
			self._deselectOtherWidget()

	currentSelect = property(lambda self:self._currentSelect, \
			_setCurrentSelection)
