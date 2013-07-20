from SelectionMenu import SelectionMenu
from Active import Active
from Widget import Widget

class RadioButton(SelectionMenu):
	def __init__(self, parent=None, rect=sf.Rectangle(),\
			alignment = Position.Center, spacing=sf.Vector2(0, 0), \
			autoDefineSize = True, select=False, active=False, \
			alwaysUpdateSelection=True, alwaysUpdateActivation=True, \
			permanentSelection=False, permanentActivation=False, \
			changeRight = sf.Keyboard.RIGHT, changeLeft = sf.Keyboard.LEFT,\
			changeTop = sf.Keyboard.UP, changeBottom = sf.Keyboard.DOWN):
		SelectionMenu.__init__(self,parent, rect, alignment, spacing, \
				autoDefineSize, select, active, alwaysUpdateSelection, \
				alwaysUpdateActivation, permanentSelection, permanentActivation, \
				changeRight, changeLeft, changeTop, changeBottom)
		self._currentActive = None

	def update(self, render):
		if self.isActive and self.isSelect:
			done = False
			for widgetList in self._widget:
				for child in widgetList:
					if isinstance(child, Active) and \
							child is not self._currentActive:
						self._currentActive = child
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

