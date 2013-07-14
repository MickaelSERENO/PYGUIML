from Widget import *
from itertools import *

class Layout(Widget):
	def __init__(self, parent=0, rect=sf.Rectangle(), alignment=Position.Center,\
			spacing = sf.Vector2(0,0), autoDefineSize = None):
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

		self._widget[pos.x][pos.y].parent = None
		self._widget[pos.x][pos.y] = None
		self._casePerWidget[pos.x][pos.y] = sf.Vector2(1,1)

		self._delUselessWidget()

		self.alignment = self.alignment
		if self.autoDefineSize :
			self.autoDefineSize = True
		else:
			self.rect = self.rect

	def _delUselessWidget(self):
		stop = False

		while not stop:
			stop = True
			check = [False, False, False, False]

			if len(self._widget) > 0 and len(self._widget[0]) > 0:
				if len(list(takewhile(lambda x : x == None, self._widget[0]))) == \
						len(self._widget[0]) and len(list(takewhile(lambda x : x != sf.Vector2(0,0), \
						self._casePerWidget[0]))) == 0:
					check[0] = True
					self._widget.pop(0)
					self._casePerWidget.pop(0)

				if len(self._widget) > 0 and len(list(takewhile(lambda x : x == None, \
						self._widget[-1]))) == \
						len(self._widget[-1]) and len(list(takewhile(lambda x : x != sf.Vector2(0,0), \
						self._casePerWidget[-1]))) == 0:
					check[1] = True
					self._widget.pop(-1)
					self._casePerWidget.pop(-1)

				i = 0

				for listWidget, casePerWidget in zip(self._widget, self._casePerWidget):
					if listWidget[-1] == None and casePerWidget[-1] != sf.Vector2(0,0):
						i += 1
					else:
						break

				if i == len(self._widget) and i != 0:
					check[2] = True
					for listWidget, casePerWidget in\
							zip(self._widget, self._casePerWidget):
						listWidget.pop(-1)
						casePerWidget.pop(-1)
						
				i = 0

				for listWidget, casePerWidget in zip(self._widget, self._casePerWidget):
					if listWidget[0] == None and casePerWidget[0] != sf.Vector2(0,0):
						i += 1
					else:
						break

				if i == len(self._widget) and i != 0:
					check[3] = True
					for listWidget, casePerWidget in\
							zip(self._widget, self._casePerWidget):
						listWidgeti.pop(0)
						casePerWidget.pop(0)

				if True in check:
					stop = False

	def delWidget(self, widget):
		position = self.getWidgetPosition(widget)
		if position != sf.Vector2(-1, -1):
			self.__delitem__(sf.Vector2(x, y))

	def getWidgetPosition(self, widget):
		x = -1
		y = -1

		for i in range(len(self._widget)):
			for j in range(len(self._widget[i])) :
				if self._widget[i][j] is widget:
					x = i
					y = j

		return sf.Vector2(x, y)

	def addWidget(self, widget, pos, numberCases=sf.Vector2(1,1), direction=Direction.Vertical, delete = False):
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

		for widgetList, caseWidget, in zip(self._widget, self._casePerWidget):
			for i in range(len(widgetList), pos.y + numberCases.y + add):
				caseWidget.append(sf.Vector2(1,1))
				widgetList.append(None)

		for x in range(pos.x, pos.x+numberCases.x):
			for y in range(pos.y, pos.y + numberCases.y):
					self._casePerWidget[x][y] = sf.Vector2(0,0)

		self._widget[pos.x][pos.y] = widget
		self._casePerWidget[pos.x][pos.y] = numberCases
		widget.parent = self

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
			self.rect = self.rect

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
		lastPosition = self.getPos(False)
		if self.autoDefineSize :
			maxSize = self._getMaximumWidgetSize()
			for x in range(len(self._widget)):
				for y in range(len(self._widget[0])):
					if self._widget[x][y]:
						self._widget[x][y].setPos(self.pos +\
								self._getNumberWidget(sf.Vector2(x, y),\
								sf.Vector2(x, y)) * self._spacing +\
								maxSize * sf.Vector2(x, y))
						lastPosition = self._widget[x][y].getPos(False) + maxSize * self._casePerWidget[x][y]
			Widget.setSize(self, lastPosition - self.getPos(False), False)

		else:
			if len(self._widget) > 0:
				caseWidget = self._getNumberCases()
				for x in range(len(self._widget)):
					for y in range(len(self._widget[x])):
						if self._widget[x][y]:
							self._widget[x][y].setPos(self.pos +\
									(self.size / self._getNumberCases() * sf.Vector2(x, y)) +\
									self._spacing * sf.Vector2(x, y) / caseWidget)

	def setSize(self, size, autoDefineSize=None):
		if autoDefineSize != None and self.autoDefineSize == True or autoDefineSize==True:
			return self.autoDefineSize == True
		else:
			Widget.setSize(self, size)

			self.alignment = None
			numberCase = self._getNumberCases()
			for x in range(len(self._widget)):
				for y in range(len(self._widget[0])):
					if self._widget[x][y]:
						suppr = self.spacing * (numberCase - self._casePerWidget[x][y]) / \
								numberCase
						self._widget[x][y].size = self._casePerWidget[x][y] * \
								self.size / numberCase - suppr

			self.autoDefineSize = False

	def _getNumberWidgetOnY(self, x, stop=None):
		number = 0
		if len(self._widget) > x:
			y = 0
			while y < len(self._widget[x]):
				if stop != None and y >= stop:
					break

				elif self._casePerWidget[x][y] == sf.Vector2(0, 0):
					for xBis in range(x, -1, -1):
						if self._casePerWidget[xBis][y] != sf.Vector2(0, 0):
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

				elif self._casePerWidget[x][y] == sf.Vector2(0, 0):
					for yBis in range(y, -1, -1):
						if self._casePerWidget[x][yBis] != sf.Vector2(0, 0):
							x += self._casePerWidget[x][yBis].x
							break
				else:
					x += self._casePerWidget[x][y].x
				number += 1

		return number

	def _getNumberCasesOnX(self, y):
		if len(self._widget) > 0 and len(self._widget[0]) > y:
			return sum([liste[y].x for liste in self._casePerWidget if y < len(liste)])
		else:
			return 0

	def _getNumberCasesOnY(self, x):
		if len(self._widget) > x and len(self._widget[0]) > 0:
			return sum([y.x for y in self._casePerWidget[x]])
		else:
			return 0

	def _getNumberCases(self):
		return sf.Vector2(self._getNumberCasesOnX(0), self._getNumberCasesOnY(0))

	def _getNumberWidget(self, pos=sf.Vector2(0,0), stop=sf.Vector2(None, None)):
		return sf.Vector2(self._getNumberWidgetOnX(pos.y, stop.x),\
				self._getNumberWidgetOnY(pos.x, stop.y))

	def _getMinimumCasePerWidget(self):
		if len(self._widget) > 0:
			return sf.Vector2(min([min([y.x for y in x if y.x > 0]) for x in self._casePerWidget]),\
					min([min([y.y for y in x if y.y > 0]) for x in self._casePerWidget]))
		else:
			return sf.Vector2(0,0)

	def _getMaxWidgetXY(self):
		if len(self._widget) > 0:
			return sf.Vector2(max([self._getNumberWidgetOnX(y) for y in\
					range(len(self._casePerWidget[0]))]), \
					max([self._getNumberWidgetOnY(x) for x in\
					range(len(self._casePerWidget))]))
		else:
			return sf.Vector2(0,0)

	def _getMaximumWidgetSize(self):
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
			minimumSize = self._getMaximumWidgetSize()
			for widgetList in self._widget:
				for widget in widgetList:
					if widget:
						x, y = self.getWidgetPosition(widget)
						if alignment == Position.TopLeft:
							widget.posOrigin = alignment
						elif alignment == Position.TopRight:
							widget.origin = sf.Vector2(minimumSize.x, 0)*self._casePerWidget[x][y] / 1
						elif alignment == Position.BottomLeft:
							widget.origin = sf.Vector2(0, minimumSize.y)*self._casePerWidget[x][y] / 1
						elif alignment == Position.BottomRight:
							widget.origin = minimumSize*self._casePerWidget[x][y] / 1
						else:
							widget.origin = minimumSize*self._casePerWidget[x][y] / 2

			self._autoDefineSize = self.autoDefineSize
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
			self.rect = self.rect
	
	def _setAutoDefineSize(self, auto):
		self._autoDefineSize = auto
		self.alignment = self.alignment
		if auto:
			for widgetList in self._widget:
				for widget in widgetList:
					if widget:
						widget.globalScale = self.globalScale

			self.pos = self.pos

	alignment = property(lambda self:self._alignment, _setAlignment)
	spacing = property(lambda self:self._spacing, _setSpacing)
	autoDefineSize = property(lambda self:self._autoDefineSize, _setAutoDefineSize)
