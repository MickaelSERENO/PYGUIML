import sfml as sf
from EventManager import EventManager
from copy import copy
from Updatable import Updatable
import functions

def enum(*seq, **keys):
	enums = dict(zip(seq,range(len(seq))),**keys)
	return type("Enum", (), enums);

Position = enum('TopLeft','TopRight','Center','BottomLeft','BottomRight')

class Widget(Updatable):
	"""Basic class for create Widgets"""

	widgetFocus = None

	def __init__(self, parent=0, rect=sf.IntRect(0,0,0,0)):
		Updatable.__init__(self,parent)
		self.isDrawing = True
		self._isStaticToView = False
		self.canFocus = True
		self.movingAllChild = False

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
		from Render import Render
		if not isinstance(render,Render):
			render = getRender()

		if self._changeWindow:
			if self._isStaticToView:
				self.setRect(self._virtualPos - render.getViewPosition(),\
						self._virtualDimensions)
			else:
				self.setRect(self._getVirtualRect())

		if self.isDrawing and render.isInView(self._getVirtuallRect()):
			self._draw(render)

	def draw(self, render=None):
		pass
			
	def drawAllWidget(self, drawing):
		"""If you want to show the Widget, put drawing to true"""
		for child in self._child:
			if isinstance(child,Widget):
				child._isDrawing = True

	def move(self, moving):
		"""This methode move the widgets. moving is a sf.Vector2f type"""
		self.setPos = (self._virtualPos + moving, False)

	def setPositionOnScreen(self, position, withOrigin=True):
		render = getRender()
		if self._isStaticToView and render is not None:
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

		newWindowSize = self._event.newWindowSize()
		defaultWindowSize = self._event.defaultWindowSize()

		if defaultWindowSize.x != 0:
			self._dimensions.x = self._virtualDimensions.x * \
					newWindowSize.x / defaultWindowSize.x
			self._pos.x =\
					self._virtualPos.x * newWindowSize.x / defaultWindowSize.x

		if defaultWindowSize.y !=0:
			self._dimensions.y = self._virtualDimensions.y * \
					newWindowSize.y / defaultWindowSize.y
			self._pos.y =\
					self._virtualPos.y * newWindowSize.y / defaultWindowSize.y

		for child in self._child:
			if isinstance(child,Widget):
				child.resizeWidget(defaultWindowSize, newWindowSize);

	def setPos(self, pos, withOrigin=True):
		if self.movingAllChild:
			for child in self._child:
				child.move(pos.x - self._virtualPos.x, \
						pos.y - self._virtualPos.y)

		render = self.getRender()
		addView = sf.Vector2f(0,0)

		if render is not None and self._isStaticToView:
			addView = copy(render.getViewPosition())

		if isinstance(self._event, EventManager):
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.newWindowSize

				if withOrigin:
					self._pos = (pos - self._origin + addView) *\
							newWindowSize / defaultWindowSize
				else:
					self._pos = (self.pos + addView) * \
							newWindowSize / defaultWindowSize
			else:
				if withOrigin:
					self._pos = pos - self._origin + addView
				else:
					self._pos = pos+addView

		else:
			if withOrigin:
				self._pos = pos - self._origin + addView
			else:
				self._pos = pos+addView
		if withOrigin:
			self._virtualPos = pos - self._origin + addView
		else:
			self._virtualPos = pos+addView

	def setDimensions(self, dimensions):
		self._scale = sf.Vector2f(1,1)
		if isinstance(self._event, EventManager):
			defaultWindowSize = event.defaultWindowSize
			if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
				newWindowSize = event.newWindowSize
				self._dimensions = \
						dimensions.x * newWindowSize.x / defaultWindowSize.x,\
						dimensions.y * newWindowSize.y / defaultWindowSize.y
			else:
				self._dimensions = dimensions

		else:
			self._dimensions = dimensions
		self._virtualDimensions = dimensions
		self._setOriginPos(self._posOrigin)

	def setIsStaticToView(self, new, change=True):
		"""Methode for set your widget static on the view or not"""
		self._isStaticToView = copy(new)
		if change:
			self.pos = self._pos

	def getPos(self, withOrigin=True):
		if withOrigin:
			if self._pos.x == 0 and self.__pos.y == 0:
				return self._origin 
			elif self._pos.x == 0:
					return sf.Vector2f(self._origin.x, \
							self._pos.y/self._virtualPos.y*\
							(self._virtualPos.y+self._origin.y))
			elif self._pos.y==0:
				return sf.Vector2f(self._pos.x/self._virtualPos.x*\
						(self._virtualPos.x+self._origin.x), self._origin.y)
			else:
				return sf.Vector2f(self._pos.x/se._virtualPos.x*\
						(self._virtualPos.x+self._origin.x),\
						self._pos.y/self._virtualPos.y*\
						(self._virtualPos.y+self._origin.y))

		else:
			return self._pos

	def getPosOnScreen(self, withOrigin=True):
		render = self.getRender()
		if render is not None:
			if self._event:
				defaultWindowSize = self._event.defaultWindowSize()
				if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
					newWindowSize = self._event.newWindowSize()
					return sf.Vector2f(self.getPosition(withOrigin) -\
						render.getViewPosition() *\
						newWindowSize / defaultWindowSize)\
			
		return self.getVirtualPos(withOrigin)

	def getVirtualPos(self, withOrigin=True):
		if withOrigin:
			return sf.Vector2f(self._virtualPos + self._origin)
		return self._virtualPos

	def getVirtualPosOnScreen(self, withOrigin=True):
		render = self.getRender()
		if render is not None:
			return self.getVirtualPos(withOrigin)-render.getViewPosition()
		else:
			return self.getVirtualPos(withOrigin)

			print("they are Rect")
	def _setOrigin(self, newOrigin):
		"""Change the origin of the widget"""
		self.move = sf.Vector2f(newOrigin-self._origin)
		self._origin = newOrigin
		self._posOrigin = Other

	def _setOriginPos(self, position):
		back = copy(self._origin)

		if position == Position.TopLeft:
			self._origin = sf.Vector2f(0,0)
		elif position == Position.TopRight:
			self._origin = sf.Vector2f(self._virtualSize.x,0)
		elif position == Position.Center:
			self._origin = sf.Vector2f(self._virtualSize/2)
		elif position == Position.BottomLeft:
			self._origin = sf.Vector2f(0,self._virtualSize.y)
		elif position == Position.BottomRight:
			self._origin = copy(self._virtualSize)

		self.move(self._origin-back)
		self._posOrigin = position
	
	def _getRect(self):
		"""Set the Rect of the view"""
		return sf.FloatRect(\
				self.getPosition(False).y, self.getPosition(False).y,\
				self._dimensions.x, self._dimensions.y)

	def _getVirtualRect(self):
		return sf.FloatRect(\
				self.getVirtualPos(False).x, self.getVirtualPos(False).y,\
				self._virtualDimensions.x, self._virtualDimensions.y)

	def _setRect(self, rect):
		"""rect is a sf.FloatRect type.
		This methode set the dimensions and the positions of the widget"""
		if isinstance(rect,sf.FloatRect):
			self.setPos(sf.Vector2f(rect.left, rect.top), False)
			self.setDimensions(sf.Vector2f(rect.width, rect.height))
			print("they are Rect")

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
			lambda self,pos : self.setPos(pos))
	posOnScreen = property(lambda self:self.getPosOnScreen(),\
			lambda self,position:self.setPosOnScreen())
	virtualPos = property(lambda self: self._getVirtualPos())
	virtualPosOnScreen = property(lambda self:self.getVirtualPosOnScreen())

	rect = property(lambda self:self._getRect(),\
			lambda self, rect:self._setRect(rect))
	virtualRect = property(lambda self:self._getVirtualRect())
	rectOnScreen = property(lambda self:self._getRectOnScreen(),\
			lambda self,rect : self._setRectOnScreen(rect))
	virtualRectOnScreen = property(lambda self:self._getVirtualRectOnScreen())

	globalScale = property(lambda self:self._scale,\
			lambda self,newScale : self._setScale(newScale))
