import sfml as sf
from copy import copy


class Widget:
	"""Basic class for create Widgets"""

	def __init__(self, parent=0, rect=sf.IntRect(0,0,0,0)):
		self._parent = 0
		self._child = list()
		self._isDrawing = True
		self._pos = sf.Vector2f(rect.left,rect.top)
		self._dimensions = sf.Vector2f(rect.width, rect.height)
		self.movingSize = False
		if isinstance(parent, Widget):
			self.parent = parent

	def __del__(self):
		self.parent = 0

		for it in self._child:
			self.removeChild(it)

	def getCopyWidget(self):
		"""This methode return a copy of this Widget. The object's parent and child are reset at 0."""
		copyWidget = copy(self)
		copyWidget._parent = 0
		copyWidget._child = list()
		return copyWidget

	def addChild(self, child, pos=-1):
		"""child become a widget's child"""
		if child._parent is not self:
			child._parent = self,pos
	
		if not self.isChild(child):
			if pos < 0:
				self._child.append(child)
			else:
				self._child.insert(pos, child)

	def removeChild(self, child):
		"""Remove child in the object"""
		self._child.remove(child)
		child._parent = 0

	def isChild(self, child):
		""" This methode say if child is a widget's child"""
		for widget in self._child:
			if child == widget:
				return True
		return False

	def drawAllWidget(self, drawing):
		"""If you want to show the Widget, put drawing to true, else to false"""
		for child in self._child:
			child._isDrawing = True

	def update(self, drawables):
		"""this methode Update all child of this Widget. It launch them Update() for drawing there"""

		for child in self._child:
			child.update(drawables)

	def scale(self, scale):
		"""scale is a sf.Vector2f type. This methode set the dimensions and the positions of the widget"""
		self.dimensions = sf.Vector2f(self.dimensions.x * scale.x, self.dimensions.y * scale.y)

	def move(self, moving):
		"""This methode move the widgets. moving is a sf.Vector2f type"""
		self.pos = sf.Vector2f(self.pos.x + moving.x, self.pos.y + moving.y)

	def addSize(self, addingSize):
		"""This methode add a size at the widget. addingSize is a sf.Vector2f type"""
		self.dimensions = sf.Vector2f(self.dimensions.x + addingSize.x, self.dimensions.y + addingSize.y)

	def getEvent(self):
		return self._parent.getEvent()

	def _getRect(self):
		return sf.FloatRect(self.pos.x, self.pos.y, self.dimensions.x, self.dimensions.y)

	def _setRect(self, rect):
		"""rect is a sf.FloatRect type. This methode set the dimensions and the positions of the widget"""
		self._setDimensions(sf.Vector2f(rect.width, rect.height))
		self._setPos(sf.Vector2f(rect.left, rect.top))

	def _setPos(self, pos):
		self._pos = pos

	def _setDimensions(self, dimensions):
		self._dimensions = dimensions

	def _setParent(self, parent, pos=-1):
		"""Set the object's Widget parent"""

		if isinstance(self._parent, Widget):
			self._parent.removeChild(self)

		self._parent = parent

		if isinstance(self._parent, Widget):
			self._parent.addChild(self, pos)

	def _getPos(self):
		return self._pos

	def _getDimensions(self):
		return self._dimensions

	def _getParent(self):
		return self._parent

	def _getIsDrawing(self):
		return self._isDrawing

	def _drawWidget(self, drawing):
		self._isDrawing = drawing

	def _resizeWidget(self, pos, size):
		self._dimensions = size
		self._pos = pos

	dimensions = property(_getDimensions, _setDimensions)
	pos = property(_getPos, _setPos)
	parent = property(_getParent, _setParent)
	rect = property(_getRect, _setRect)
	isDrawing = property(_getIsDrawing ,_drawWidget)
