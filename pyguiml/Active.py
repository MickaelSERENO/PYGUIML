import sfml as sf

class Active:
	def __init__(self, select=False, active=False,\
			alwaysUpdateSelection=True, alwaysUpdateActivation=True,\
			permanentSelection = False, permanentActivation = False):
		self._active = active
		self._select = select
		self.alwaysUpdateSelection = alwaysUpdateSelection
		self.alwaysUpdateActivation = alwaysUpdateActivation
		self.permanentSelection = permanentSelection
		self.permanentActivation = permanentActivation
		self.selectOnce = False
		self.activeOnce = False
		self.deselectOnce = False
		self.disactiveOnce = False

		self.howActiveKeyboard = None
		self.howActiveMouse = sf.Mouse.LEFT

	def update(self):
		if self.alwaysUpdateSelection:
			self.updateSelection()
		if self.alwaysUpdateActivation:
			self.updateActivation()

	def howActive(self):
		return self._select

	def howDisactive(self):
		return not self.howActive()

	def howSelect(self):
		return self._active

	def howDeselect(self):
		return not self.howSelect()

	def updateSelection(self):
		if (self.howSelect() and not self.howDeselect()) or self.permanentSelection or self.selectOnce:
			self.selectIt()
		elif self.howDeselect():
			self.deselectIt()

		return self._select

	def updateActivation(self):
		if (self.howActive() and not self.howDisactive()) or self.permanentActivation or self.activeOnce:
			self.activeIt()
		elif self.howDisactive():
			self.disactiveIt()

		return self._active

	def selectIt(self):
		self._select = True

	def deselectIt(self):
		self._select = False

	def activeIt(self):
		self._active = True

	def disactiveIt(self):
		self._active = False

	isSelect = property(lambda self:self._select)
	isActive = property(lambda self:self._active)