from Widget import *

class Layout(Widget):
	def __init__(self, parent=0, rect=None, keepProportion = True,\
			alignment=Position.Center, spacing = 0, autoDefineSize = None):
		Widget.__init__(self, parent, rect)
		self._keepProportion = keepProportion
		self._alignment = alignment
		self._widget = list(list())
		self._casePerWidget = list(list())
		self._spacing = spacing
		self._autoDefineSize = autoDefineSize

	def __getitem__(self, pos)
		return self._widget[pos.x][pos.y]

	def __setitem__(self, pos, widget):
		self.addWidget(widget, pos)

	def __delitem__(self, pos):

		self._widget[pos.x][pos.y] = None
		self._casePerWidget[pos.x][pos.y] = sf.Vector2(1,1)

		stop = False

		while not stop:
			stop = True
			check = [False, False, False, False]

			if len(self._widget) != 0 and len(self._widget[0]) != 0:
				if len(dropwhile(lambda x : x == None, self._widget[0])) == \
						len(self._widget[0]):
						check[0] = True
					del self._widget[0]

				if len(dropwhile(lambda x : x == None, \
						self._widget[len(self._widget)-1])) == \
						len(self._widget[0]):
					check[1] = True
					del self._widget[len(self._widget)-1]

				i = 0

				for listWidget in self._widget:
					if listWidget[len(listWidget)-1] == None:
						i += 1
					else:
						break

				if i == len(self._widget):
					check[2] = True
					for listWidget in self._widget:
						del listWidget[len(listWidget)-1]
						
				i = 0

				for listWidget in self._widget:
					if listWidget[0] == None:
						i += 1
					else:
						break

				if i == len(self._widget):
					check[3] = True
					for listWidget in self._widget:
						del listWidget[0]

				if True in check:
					stop = False

		if self.autoDefineSize :
			self.autoDefineSize = True
		else:
			self.rect = self.virtualRect

	def setSize(self, widget)

	def delWidget(self, widget)
		x = -1
		y = -1

		for i in self._widget:
			for j in i :
				if self._widget[i][j] is widget:
					x = i
					y = j

		if x != -1 :
			self.__delitem__(sf.Vector2(x, y))

	def addWidget(self, widget, pos, numberCases=(1,1), direction=Direction.Vertical, delete = False):
		if pos.x > self._getNumberWidgetOnY(pos.x):
			for x in range(self._getNumberWidgetOnY(pos.y),\
					pos.x + numberCases.x):
				self._widget.append(list())
				self._casePerWidget.append(list())

		for widgetList, caseWidget, posX in \
				zip(self._widget, self._casePerWidget, range(len(self._widget))):

			for x in range(self._getNumberCasesOnX(posX), pos.y + numberCases.y):
				if posX = pos.x:
					if len(widgetList) == pos.y:
						caseWidget.append(numberCases)
					elif len(widgetList) > pos.y and len(widgetList) < pos.y + numberCases.y :
						caseWidget.append(sf.Vector2(0,0))
					else:
						caseWidget.append(sf.Vector2(1,1))
				else:
					caseWidget.append(sf.Vector2(0,0))
				widgetList.append(None)

		check = False
		x = -1
		y = -1
		for i in range(pos.x + numberCases.x, pos.x, -1):
			for j in range(pos.y + numberCases.y, pos.y, -1):
				if pos != sf.Vector2(i, j) and not delete and self[pos] != None:
					if direction = Direction.Vertical:
						

		self._widget[pos.x][pos.y] = widget
		if self.autoDefineSize :
			self.autoDefineSize = True
		else:
			self.rect = self.virtualRect

	def _maxWidgetInRectangle(self, rect):
		return max([max[]]

	def _getNumberWidgetOnX(self, x):
		return len([number for number in self._casePerWidget[x] if nomber> 0])

	def _getNumberWidgetOnY(self, y):
		return len([number for number in\
				[liste[y] for liste in self._casePerWidget] if number > 0])

	def _getNumberCasesOnY(self, y):
		return sum([number for number in \
				[liste[y] for liste in self._casePerWidget]])

	def _getNumberCasesOnX(self, x):
		return sum(self._casePerWidget[x])

	def _getNumberCases(self):
		return sf.Vector2(sum([self._casePerWidget[x][0]\
				for x in range(len(self._widget))]),\
				sum(self._casePerWidget[0))

	def _setAlignment(self, alignment):
		self._alignment = alignment
		autoDefineSize = self._autoDefineSize
		self.rect = self.virtualRect
		self._autoDefineSize = autoDefineSize
	
	def _setKeepProportion(self, keepProportion):
		self._keepProportion = keepProportion
		autoDefineSize = self._autoDefineSize
		self.rect = self.virtualRect
		self._autoDefineSize = autoDefineSize

	def _setAutoDefineSize(self, auto):
		self._autoDefineSize = auto
		self._keepProportion = True
		if auto = True and len(self._widget) != 0:
			sizeDefine = sf.Vector2(0,0)
			sizeDefine.x = \
					max([max([y.pos.x for y in x]) for x in self._widget])
			sizeDefine.y = \
					max([max([y.pos.x for y in x]) for x in self._widget])

	alignment = property(lambda self:self._alignment, _setAlignment)
	keepProportion = property(lambda self:self._keepProportion,\
			_setKeepProportion)
	spacing = property(lambda self:self._spacing, _setSpacing)
	autoDefineSize = property(lambda self:self._autoDefineSize, _setAutoDefineSize)
