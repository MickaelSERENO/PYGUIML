import sfml as sf
from EventManager import EventManager
from copy import copy
from Updatable import Updatable
from Render import Render

def enum(*seq, **keys):
	enums = dict(zip(seq,range(len(keys))),**keys)
	return type("Enum", (), keys);

Position = enum('TopLeft','TopRight','Center','BottomLeft','BottomRight')

class Widget(Updatable:
	"""Basic class for create Widgets"""

	widgetFocus = None

	def __init__(self, parent=0, rect=sf.IntRect(0,0,0,0)):
		Updatable.__init__(self,parent)
		self.isDrawing = True
		self.isStaticToView = False
		self.canFocus = True
		self.movingiAllChild = False

		self._origin = sf.Vector2f(0,0)
		self._pos = sf.Vector2f(rect.left,rect.top)
		self._posSaved = copy(self._pos)
		self._dimensions = sf.Vector2f(rect.width, rect.height)
		self._virtualPos = copy(self._pos)
		self._virtualDimensions = copy(self._dimensions)
		self._posOnScreen = sf.Vector2f(rect.left -getRenderViewPosition().x,\
				rect.top - getRenderViewPosition().y)
		self._scale = sf.Vector2f(1,1)

	def getCopyWidget(self):
		"""This methode return a copy of this Widget.
		The object's parent and child are reset at 0."""
		copyWidget = copy(self)
		copyWidget._parent = 0
		copyWidget._child = list()
		return copyWidget

	def updateFocus(self):
		if self.canFocus:
			renderParentViewPosition = getRenderViewPosition()
			getPosOnScreen()
			if self.isDrawing and isinstance(self._event,EventManager) and\
				self._event.isMouseInRect(getRectOnScreen()):
				Updatable._focusIsChecked = False
				Widget.widgetFocus = self
			Updatable.updateFocus(self)

	def update(self, render):
		if self._changeWindow:
			self.setRect(self._getRect())
		if self.isStaticToView:
			posInit = copy(self._posSaved)
			setPosition(self._posSaved.x + render.getViewPosition().x,\
					self._posSaved.y + render.getViewPosition().y);
			
	def drawAllWidget(self, drawing):
		"""If you want to show the Widget, put drawing to true, else to false"""
		for child in self._child:
			child._isDrawing = True

	def scale(self, scale):
		"""scale is a sf.Vector2f type. This methode set the dimensions and the positions of the widget"""
		self.dimensions = sf.Vector2f(self._virtualDimensions.x * scale.x, self.dimensions.y * scale.y)

	def move(self, moving):
		"""This methode move the widgets. moving is a sf.Vector2f type"""
		self.pos = sf.Vector2f(self._virtualPos.x + moving.x, self._virtualPos.y + moving.y)

	def addSize(self, addingSize):
		"""This methode add a size at the widget. addingSize is a sf.Vector2f type"""
		self.dimensions = sf.Vector2f(self._virtualDimensions.x + addingSize.x, self._virtualDimensions.y + addingSize.y)

	def getEvent(self):
		if isinstance(parent, Widget):
			return self._parent.getEvent()
		else:
			return False

	def resizeWidget(selfi, defaultWindowSize, newWindowSize):
		"""Thie methode resize correctly the Widgets"""

		self._dimensions.x = self._virtualDimensions.x * newWindowSize.x / defaultWindowSize.x
		self._pos.x = self._virtualPos.x * newWindowSize.x / defaultWindowSize.x

		self._dimensions.y = self._virtualDimensions.y * newWindowSize.y / defaultWindowSize.y
		self._pos.y = self._virtualPos.y * newWindowSize.y / defaultWindowSize.y

		for child in self._child
			child.resizeWidget(defaultWindowSize, newWindowSize);

	def _getRect(self):
		return sf.FloatRect(self._pos.x, self._pos.y, self._dimensions.x, self._dimensions.y)

	def _getVirtualPos(self):
		return sf.FloatRect(self._virtualPos.x, self._virtualPos.y, self._virtualDimensions.x, self._virtualDimensions.y)

	def _setRect(self, rect):
		"""rect is a sf.FloatRect type. This methode set the dimensions and the positions of the widget"""
		self._setDimensions(sf.Vector2f(rect.width, rect.height))
		self._setPos(sf.Vector2f(rect.left, rect.top))

	def _setPos(self, pos):
		if self.movingAllChild:
			for child in self._child:
				child.move(pos.x - self._virtualPos.x, pos.y - self._virtualPos.y)

		event = self.getEvent()
		if event:
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.
				self._pos = sf.Vector2f(pos.x * newWindowSize.x / defaultWindowSize.x, pos.y * newWindowSize.y / defaultWindowSize.y)
			else:
				self._pos = copy(pos)

		else:
			self._pos = copy(pos)
		self._virtualPos = copy(pos)

	def _setDimensions(self, dimensions):
		self._dimensions = dimensions
		event = self.getEvent()
		if event:
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.
				self._dimensions = sf.Vector2f(dimensions.x * newWindowSize.x / defaultWindowSize.x, dimensions.y * newWindowSize.y / defaultWindowSize.y)
			else:
				self._dimensions = copy(dimensions)

		else:
			self._dimensions = copy(dimensions)
		self._virtualDimensions = copy(dimensions)

	def _setParent(self, parent, pos=-1):
		"""Set the object's Widget parent"""

		if isinstance(self._parent, Widget):
			self._parent.removeChild(self)

		self._parent = parent

		if isinstance(self._parent, Widget):
			self._parent.addChild(self, pos)

	def _getPos(self):
		return self._pos

	def _getVirtualPos(self):
		return self._virtualPos

	def _getDimensions(self):
		return self._dimensions

	def _getVirtualDimensions(self):
		return self._virtualDimensions

	def _getParent(self):
		return self._parent

	def _drawWidget(self, drawing):
		self._isDrawing = drawing

	def _resizeWidget(self, pos, size):
		self._dimensions = size
		self._pos = pos

	dimensions = property(_getDimensions, _setDimensions)
	virtualDimensions = property(_getVirtualDimensions)
	pos = property(_getPos, _setPos)
	virtualPos = property(_getVirtualPos)
	parent = property(_getParent, _setParent)
	rect = property(_getRect, _setRect)
	virtualRect = property(_getVirtualRect)
