from Widget import *

class Layout(Widget):
	def __init__(self, parent=0, rect=sf.Rectangle(), alignment=Position.Center,\
			spacing = 0, autoDefineSize = None):
		Widget.__init__(self, parent, rect)
		self._alignment = alignment
		self._widget = list(list())
		self._casePerWidget = list(list())
		self._spacing = spacing
		self._autoDefineSize = autoDefineSize

	def __getitem__(self, pos):
		return self._widget[pos.x][pos.y]

	def __setitem__(self, pos, widget):
		self.addWidget(widget, pos)

	def __delitem__(self, pos):

		self._widget[pos.x][pos.y] = None
		self._casePerWidget[pos.x][pos.y] = sf.Vector2(1,1)

		self._delUselessWidget()

		self.alignment = self.alignment
		if self.autoDefineSize :
			self.autoDefineSize = True
		else:
			self.rect = self.virtualRect

	def _delUselessWidget(self):
		stop = False

		while not stop:
			stop = True
			check = [False, False, False, False]

			if len(self._widget) != 0 and len(self._widget[0]) != 0:
				if len(takewhile(lambda x : x == None, self._widget[0])) == \
						len(self._widget[0]):
					check[0] = True
					self._widget.pop[0]
					self._casePerWidget.pop[0]

				if len(takewhile(lambda x : x == None, \
						self._widget[-1])) == \
						len(self._widget[-1]):
					check[1] = True
					self._widget.pop[-1]
					self._casePerWidget.pop[-1]

				i = 0

				for listWidget in self._widget:
					if listWidget[-1] == None:
						i += 1
					else:
						break

				if i == len(self._widget):
					check[2] = True
					for listWidget, casePerWidget in\
							zip(self._widget, self._casePerWidget):
						listWidget.pop[-1]
						casePerWidget.pop[-1]
						
				i = 0

				for listWidget in self._widget:
					if listWidget[0] == None:
						i += 1
					else:
						break

				if i == len(self._widget):
					check[3] = True
					for listWidget, casePerWidget in\
							zip(self._widget, self._casePerWidget):
						listWidgeti.pop[0]
						casePerWidget.pop[0]

				if True in check:
					stop = False

	def delWidget(self, widget):
		position = self.getWidgetPosition(widget)
		if position != sf.Vector2(-1, -1):
			self.__delitem__(sf.Vector2(x, y))

	def getWidgetPosition(self, widget):
		x = -1
		y = -1

		for i in self._widget:
			for j in i :
				if self._widget[i][j] is widget:
					x = i
					y = j

		return sf.Vector2(x, y)

	def addWidget(self, widget, pos, numberCases=(1,1), direction=Direction.Vertical, delete = False):
		add = 0
		if direction == Direction.Horizontal:
			add = numberCases.x

			for x in range(self._getNumberCases().x,\
					pos.x + numberCases.x + add):
				self._widget.append(list())
				self._casePerWidget.append(list())

		add = 0
		if direction == Direction.Vertical:
			add = numberCases.y

		for widgetList, caseWidget in zip(self._widget, self._casePerWidget):
			for x in range(self._getNumberCases.Y, pos.y + numberCases.y + add):
				caseWidget.append(sf.Vector2(1,1))
				widgetList.append(None)

		for widgetList, casePerWidget, x in \
				zip(self._widget, enumerate(self._casePerWidget)):
			for theWidget, case, y in \
					zip(widgetList, enumerate(casePerWidget)):
				if sf.Vector2(x, y) == pos:
					self._widget[x][y] = widget
					self._casePerWidget[x][y] = numberCases
				elif x > pos.x and x < pos.x + numberCases.x and \
						y > pos.y and y < pos.y + numberCases.y :
					self._casePerWidget[x][y] = sf.Vector2(0,0)

		addX = 0
		addY = 0
		if direction == Direction.Vertical:
			addY = numberCases.y
		else:
			addX = numberCases.x

			for x in range(self._getNumberCases().x-numberCases.x-1, pos.x, -1):
				for y in range(self._getNumberCases().y-1, pos.y, -1):
					numberCases = self
					self._widget[addX][y+addY] = self._widget[x][y]

		self._delUselessWidget()

		self.alignment = self.alignment
		if self.autoDefineSize :
			self.autoDefineSize = True
		else:
			self.rect = self.virtualRect

	def _maxWidgetInRectangle(self, rect):
		lenX = list()
		lenY = list()
		for x in range(rect.left, rect.left + rect.width):
			nbY = 0
			for y in range(rect.top, rect.top + rect.height):
				nbY += bool(self._widget[x][y])
			lenY.append(nbY)

		for y in range(rect.top, rect.top + rect.height):
			nbX = 0
			for x in range(rect.left, rect.left + rect.width):
				nbX += bool(self._widget[x][y])
			lenX.append(nbY)

		return sf.Vector2(max(lenX), max(lenY))


	def setPos(self, pos, withOrigin = True):
		Widget.setPos(self, pos)
		if self.autoDefineSize :
			maxSize = self._getMinimumWidgetSize()
			for x in range(len(self._widget)):
				for y in range(len(self._widget[0])):
					if self._widget[x][y]:
						self._widget[x][y].setPos(self.virtualPos +\
								self._getNumberWidget(sf.Vector2(x, y),\
								sf.Vector2(x, y)) * self._spacing +\
								maxSize * sf.Vector2(x, y))
						lastPosition = self._widget[x][y].getPos(False) + maxSize * self._casePerWidget[x][y]
			Widget.setSize(lastPosition - self.getPos(False))

		else:
			if len(self._widget) > 0:
				for x in range(len(self._widget[0])):
					for y in range(len(self._widget[0])):
						if self._widget[x][y]:
							self._widget[x][y].setPos(self.virtualPos +\
									self.size - (self.size / self._getNumberCases() * sf.Vector2(x, y)) + \
									self._spacing * self._getNumberWidget(sf.Vector2(x, y), sf.Vector2(x, y)), False)
	def setSize(self, size, autoDefineSize=False):
		if autoDefineSize:
			return self.autoDefineSize == True
		Widget.setSize(self, size)

		for x in range(len(self._widget)):
			for y in range(len(self._widget[0])):
				if self._widget:
					self._widget[x][y].size = self._casePerWidget[x][y] * \
							self.size / self._getNumberCases() -\
							self.spacing / \
							sf.Vector2(self._getNumberWidgetOnX(y), self._getNumberWidgetOnY(x)) 

		self.autoDefineSize = False

	def _getNumberWidgetOnY(self, x, stop=None):
		number = 0
		if len(self._widget) > x:
			y = 0
			while y < len(self._widget[0]):
				if stop != None and y >= stop:
					break

				elif self._casePerWidget[x][y] == 0:
					for xBis in range(x, 0, -1):
						if self._casePerWidget[xBis][y] > 0:
							y += self._casePerWidget[xBis][y].y
							break
				else:
					y += self._casePerWidget[x][y].y
				number += 1
		return number

	def _getNumberWidgetOnX(self, y, stop=None):
		number = 0
		if len(self._widget) > 0:
			x = 0
			while x < self._getNumberCasesOnX(y):
				if stop != None and y >= stop:
					break

				elif self._casePerWidget[x][y] == 0:
					for yBis in range(y, 0, -1):
						if self._casePerWidget[x][yBis] > 0:
							x += self._casePerWidget[yBis][x].y
							break
				else:
					x += self._casePerWidget[x][y].x
				number += 1

		return number

	def _getNumberCasesOnX(self, y):
		if len(self._widget) > 0 and len(self._widget[0]) > y:
			return sum([liste[y] for liste in self._casePerWidget])
		else:
			return 0

	def _getNumberCasesOnY(self, x):
		if len(self._widget) > x:
			return sum(self._casePerWidget[x])
		else:
			return 0

	def _getNumberCases(self):
		return sf.Vector2(self._getNumberCasesOnX(0), self._getNumberCasesOnY(0))

	def _getNumberWidget(self, pos=sf.Vector2(0,0), stop=sf.Vector2(None, None)):
		return sf.Vector2(self._getNumberWidgetOnX(pos.y, stop.x),\
				self._getNumberWidgetOnY(pos.x, stop.y))

	def _getMinimumCasePerWidget(self):
		return sf.Vector2(min([min([y.x for y in x if y.x > 0]) for x in self._casePerWidget]),\
				min([min([y.y for y in x if y.y > 0]) for x in self._casePerWidget]))

	def _getMaxWidgetXY(self):
		return sf.Vector2(max([self._getNumberWidgetOnX(y) for y in\
				range(len(self._getNumberCasesOnX(0)))]), \
				max([self._getNumberWidgetOnY(x) for x in\
				range(len(self._getNumberCasesOnY(0)))]))

	def _getMinimumWidgetSize(self):
			vector = sf.Vector2(0,0)
			minimumCasePerWidget = self._getMinimumCasePerWidget()
			for x in range(len(self._widget)):
				for y in range(len(self._widget[x])):
					if self._widget[x][y]:
						vector = sf.Vector2(max(vector.x,\
								self._widget[x][y].size.x / \
								(self._casePerWidget[x][y].x / minimumCasePerWidget.x)),
								max(vector.y, self._widget[x][y].size.y / \
								(self._casePerWidget[x][y].y / minimumCasePerWidget.y)))
			return vector * self.globalScale

	def _setAlignment(self, alignment):
		self._alignment = alignment
		if self._autoDefineSize:
			minimumSize = self._getMinimumWidgetSize()
			for widgetList in self._widget:
				for widget in widgetList:
					if widget:
						if alignement == Position.TopLeft:
							widget.posOrigin = alignement
						elif alignement == Position.TopRight:
							widget.origin = sf.Vector2(minimumSize.x, 0)*self._casePerWidget[x][y]
						elif alignement == Position.BottomLeft:
							widget.origin = sf.Vector2(0, minimumSize.y)*self._casePerWidget[x][y]
						elif alignement == Position.BottomRight:
							widget.origin = minimumSize*self._casePerWidget[x][y]
						else:
							widget.origin = minimumSize*self._casePerWidget[x][y] / 2
		else:
			for widgetList in self._widget:
				for widget in widgetList:
					if widget:
						widget.posOrigin = Position.TopLeft

	def _setSpacing(self, space):
		self._spacing = space
		if self._autoDefineSize:
			self.autoDefineSize = True
		else:
			self.rect = self.virtualRect
	
	def _setAutoDefineSize(self, auto):
		self._autoDefineSize = auto
		self.alignment = self.alignment
		if auto:
			for widgetList in self._widget:
				for widget in widgetList:
					if widget:
						widget.globalScale = self.globalScale

			self.pos = self.virtualPos

	alignment = property(lambda self:self._alignment, _setAlignment)
	spacing = property(lambda self:self._spacing, _setSpacing)
	autoDefineSize = property(lambda self:self._autoDefineSize, _setAutoDefineSize)
