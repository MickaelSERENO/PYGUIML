import sfml as sf
from EventManager import EventManager
from copy import copy
from Updatable import Updatable
from Render import Render

def enum(*seq, **keys):
	enums = dict(zip(seq,range(len(keys))),**keys)
	return type("Enum", (), keys);

Position = enum('TopLeft','TopRight','Center','BottomLeft','BottomRight')

class Widget(Updatable):
	"""Basic class for create Widgets"""

	widgetFocus = None

	def __init__(self, parent=0, rect=sf.IntRect(0,0,0,0)):
		Updatable.__init__(self,parent)
		self.isDrawing = True
		self._isStaticToView = False
		self.canFocus = True
		self.movingiAllChild = False

		self._origin = sf.Vector2f(0,0)
		self._posOrigin = Position.TopLeft

		self._pos = sf.Vector2f(rect.left,rect.top)
		self._dimensions = sf.Vector2f(rect.width, rect.height)
		self._virtualPos = copy(self._pos)
		self._virtualDimensions = copy(self._dimensions)
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
			if self.isDrawing and isinstance(self._event,EventManager) and\
				self._event.isMouseInRect(getRectOnScreen()):
				Widget.widgetFocus = self
			Updatable.updateFocus(self)

	def update(self, render=None):
		if not isinstance(render,Render):
			render = getRender()

		if self._changeWindow:
			if self._isStaticToView:
				self.setRect(self._virtualPos - render.getViewPosition(),\
						self._virtualDimensions)
			else:
				self.setRect(self._getVirtualRect())

		if self.isDrawing and render.isInView(self._getVirtuallRect()):
			self._draw(render):

	def draw(self, render=None):
		pass
			
	def drawAllWidget(self, drawing):
		"""If you want to show the Widget, put drawing to true"""
		for child in self._child:
			if isinstance(child,Widget):
				child._isDrawing = True

	def move(self, moving):
		"""This methode move the widgets. moving is a sf.Vector2f type"""
		self.pos = (self._virtualPos + moving, false)

	def setPositionOnScreen(self, position, withOrigin):
		render = getRender()
		if self._isStaticToView and isinstance(render, Render):
			self._setPosition(position-render.getViewPosition(), withOrigin)
		else:
			self._setPosition(position, withOrigin)

	def scale(self, scale):
		"""scale is a sf.Vector2f type.
		This methode set the dimensions of the widget"""
		self._scale = sf.Vector2f(x * self._scale.x, y*self._scale.y)
		self.dimensions = sf.Vector2f(self._virtualDimensions.x * scale.x,\
				self.dimensions.y * scale.y)

	def addSize(self, addingSize):
		"""This methode add a size at the widget.
		addingSize is a sf.Vector2f type"""
		self.dimensions = sf.Vector2f(self._virtualDimensions.x+addingSize.x,\
				self._virtualDimensions.y + addingSize.y)
	
	def resizeWidget(selfi, defaultWindowSize, newWindowSize):
		"""This methode resize correctly the Widgets"""

		self._dimensions.x = self._virtualDimensions.x * \
				newWindowSize.x / defaultWindowSize.x
		self._pos.x =\
				self._virtualPos.x * newWindowSize.x / defaultWindowSize.x

		self._dimensions.y = self._virtualDimensions.y * \
				newWindowSize.y / defaultWindowSize.y
		self._pos.y =\
				self._virtualPos.y * newWindowSize.y / defaultWindowSize.y

		for child in self._child
			child.resizeWidget(defaultWindowSize, newWindowSize);

	def setPos(self, pos, withOrigin):
		if self.movingAllChild:
			for child in self._child:
				child.move(pos.x - self._virtualPos.x, \
						pos.y - self._virtualPos.y)

		render = self.getRender()
		addView = sf.Vector2f(0,0)

		if isinstance(render,Render) and self._isStaticToView:
			addView = copy(render.getViewPosition())

		if isinstance(self._event, EventManager):
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.newWindowSize

				if withOrigin:
					self._pos = sf.Vector2f((pos + self._origin + addView) *\
							newWindowSize / defaultWindowSize)
				else:
					self._pos = sf.Vector2f((self.pos + addView) *\
							newWindowSize / defaultWindowSize)
			else:
				if withOrigin:
					self._pos = sf.Vector2f(pos+  self._origin + addView)
				else:
					self._pos = sf.Vector2f(pos+addView)

		else:
			if withOrigin:
				self._pos = sf.Vector2f(pos + self._origin + addView)
			else:
				self._pos = sf.Vector2f(pos+addView)

		if withOrigin:
			self._virtualPos = sf.Vector2f(pos + self._origin + addView)
		else:
			self._virtualPos = sf.Vector2f(pos+addView)

	def setDimensions(self, dimensions):
		self._scale = sf.Vector2f(1,1)
		if isinstance(self._event, EventManager):
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.newWindowSize
				self._dimensions = sf.Vector2f(\
						dimensions.x * newWindowSize.x / defaultWindowSize.x,\
						dimensions.y * newWindowSize.y / defaultWindowSize.y)
			else:
				self._dimensions = copy(dimensions)

		else:
			self._dimensions = copy(dimensions)
		self._virtualDimensions = copy(dimensions)
		self._setOriginPos(self._posOrigin)

	def setIsStaticToView(self, new, change=True):
		"""Methode for set your widget static on the view or not"""
		self._isStaticToView = copy(new)
		if change:
			self.pos = self._pos

	def getVirtualPos(self):
		return sf.FloatRect(self._virtualPos.x, self._virtualPos.y,\
				self._virtualDimensions.x, self._virtualDimensions.y)

	def _setOrigin(self, newOrigin):
		"""Change the origin of the widget"""
		self.move = sf.Vector2f(newOrigin-self._origin)
		self._origin = newOrigin
		self._posOrigin = Other

	def _setOriginPos(self, position):
		back = copy(m_origin)

		if position = Position.TopLeft:
			self._origin = sf.Vector2f(0,0)
		elif position = Position.TopRight:
			self._origin = sf.Vector2f(self._virtualSize.x,0)
		elif position = Position.Center:
			self._origin = sf.Vector2f(self._virtualSize/2)
		elif position = Position.BottomLeft:
			self._origin = sf.Vector2f(0,self._virtualSize.y)
		elif position = Position.BottomRight:
			self._origin = copy(self._virtualSize)

		self.move(self._origin-back)
		self._posOrigin = position
	
	def _getRect(self):
		"""Set the Rect of the view"""
		return sf.FloatRect(self.pos(False),\
				self._dimensions.x, self._dimensions.y)


	def _setRect(self, rect):
		"""rect is a sf.FloatRect type.
		This methode set the dimensions and the positions of the widget"""
		self._setDimensions(sf.Vector2f(rect.width, rect.height))
		self._setPos(sf.Vector2f(rect.left, rect.top), False)

	isStaticToView = property(lambda self : self._isStaticToView, \
			lambda self,static: self._setIsStaticToView(static))

	origin = property(lambda self: self._origin,\
			lambda self,origin : self._setOrigin(origin))
	posOrigin = property(lambda  self: self._posOrigin,\
			lambda self,position : self._setOriginPos(position))

	dimensions = property(lambda self :	self._dimensions,\
			lambda self, dimension, : self._setDimensions(dimension))
	virtualDimensions = property(lambda self : self._virtualDimensions)

	pos = property(lambda self: self.getPos(), \
			lambda self,pos : self._setPos(pos))
	virtualPos = property(lambda self: self._getVirtualPos())

	rect = property(lambda self:self._getRect(),\
			lambda self, rect:self._setRect(rect))
	virtualRect = property(lambda self:self._getVirtualRect())

	globalScale = property(lambda self:self._scale,\
			lambda self,newScale : self._setScale(newScale)
