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

	filesLoading = dict()
	widgetFocus = None

	def __init__(self, parent=0, rect=sf.Rectangle()):
		Updatable.__init__(self,parent)
		self._isDrawing = True
		self._isStaticToView = False
		self.canFocus = True
		self.movingAllChild = False

		self._origin = sf.Vector2(0,0)
		self._posOrigin = Position.TopLeft

		self._pos = sf.Vector2(rect.left,rect.top)
		self._size = sf.Vector2(rect.width, rect.height)
		self._virtualPos = copy(self._pos)
		self._virtualSize = copy(self._size)
		self._scale = sf.Vector2(1,1)
		self._relativeSizeOnView = None
		self._relativePositionOnView = None

	def getCopyWidget(self):
		"""This methode return a copy of this Widget.
		The object's parent and self are reset at 0."""
		copyWidget = copy(self)
		copyWidget._parent = 0
		copyWidget._self = list()
		return copyWidget

	def updateFocus(self):
		if self.canFocus:
			if self.canUpdate and isinstance(self._event,EventManager) and\
				self._event.isMouseInRect(self.rectOnScreen):
				Widget.widgetFocus = self
			Updatable.updateFocus(self)

	def update(self, render=None):
		if self.canUpdate:
			if not render:
				render = self.getRender()

			if render:
				if self._changeWindow:
					self.relativeSizeOnView = self.relativeSizeOnView
					self.relativeSizeOnView = self.relativeSizeOnView
					if self._isStaticToView:
						self._setRect(self.virtualPos -\
								render.getViewPosition(), self.virtualSize)
					else:
						self._setRect(self._getVirtualRect())

			if self.isDrawing and render.isInView(self.rectOnScreen):
				if render is not self:
					self.draw(render)
		super().update()

	def draw(self, render=None):
		"""Draw the Widget on the render"""
		pass
			
	def drawWidget(self, draw=True):
		"""If you want thatt at the next update your
		widget will be drawing or not"""
		self._isDrawing = draw

	def drawAllWidget(self, drawing):
		"""If you want to show the Widget, put drawing to true"""
		for self in self._self:
			if isinstance(self,Widget):
				self._isDrawing = True

	def move(self, moving):
		"""This methode move the widgets. moving is a sf.Vector2 type"""
		self.setPos(self._virtualPos + moving, False)

	def setPosOnScreen(self, position, withOrigin=True):
		render = self.getRender()
		if self._isStaticToView and render is not None:
			self._setPosition(position-render.getViewPosition(), withOrigin)
		else:
			self._setPosition(position, withOrigin)

	def scale(self, scale):
		"""scale is a sf.Vector2 type.
		This methode set the size of the widget"""
		self._scale = sf.Vector2(x * self._scale.x, y*self._scale.y)
		self.size = sf.Vector2(self.virtualSize.x * scale.x,\
				self.size.y * scale.y)

	def addSize(self, addingSize):
		"""This methode add a size at the widget.
		addingSize is a sf.Vector2 type"""
		self.size = sf.Vector2(self.virtualSize.x+addingSize.x,\
				self.virtualSize.y + addingSize.y)
	
	def _resizeWidget(self):
		"""This methode resize correctly the Widgets"""

		newWindowSize = sf.Vector2(self._event.newWindowSize)
		defaultWindowSize = sf.Vector2(self._event.defaultWindowSize)


		if defaultWindowSize.x != 0:
			self._size.x = self.virtualSize.x * \
					newWindowSize.x / defaultWindowSize.x
			self._pos.x =\
					self.virtualPos.x * newWindowSize.x / defaultWindowSize.x

		if defaultWindowSize.y !=0:
			self._size.y = self.virtualSize.y * \
					newWindowSize.y / defaultWindowSize.y
			self._pos.y =\
					self.virtualPos.y * newWindowSize.y / defaultWindowSize.y

		for self in self._child:
			if isinstance(self,Widget):
				self._resizeWidget()

	def setPos(self, pos, withOrigin=True):
		if self.movingAllChild:
			for self in self._self:
				self.move(pos.x - self._virtualPos.x, \
						pos.y - self._virtualPos.y)

		if self._relativePositionOnView == None:
			render = self.getRender()
			scale = sf.Vector2(1,1)

			if isinstance(self._event, EventManager):
				defaultWindowSize = self._event.defaultWindowSize
				if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
					scale = self._event.newWindowSize / defaultWindowSize

				if withOrigin:
					self._pos = (pos - self._origin) * scale
				else:
					self._pos = self.pos * scale

			if withOrigin:
				self._virtualPos = pos - self._origin
			else:
				self._virtualPos = pos

	def setSize(self, size):
		if self._relativeSizeOnView == None:
			self._scale = sf.Vector2(1,1)
			if isinstance(self._event, EventManager):
				defaultWindowSize = self._event.defaultWindowSize
				if defaultWindowSize.x != 0 and defaultWindowSize.y != 0:
					newWindowSize = self._event.newWindowSize
					self._size = \
							size.x * newWindowSize.x / defaultWindowSize.x,\
							size.y * newWindowSize.y / defaultWindowSize.y
				else:
					self._size = size

			else:
				self._size = size
			self._virtualSize = size
			self._setOriginPos(self._posOrigin)

	def setIsStaticToView(self, new, change=True):
		"""Methode for set your widget static on the view or not"""
		self._isStaticToView = copy(new)
		if change:
			if self._isStaticToView:
				self.pos = self._pos
			else:
				render = self.getRender()
				if render:
					viewPosition = render.getViewRectWithZoom()
					viewPosition = sf.Vector2(viewPosition.left,\
							viewPosition.top)
					self.pos = self._pos - viewPosition

	def getPos(self, withOrigin=True):
		if withOrigin:
			if self._virtualPos.x == 0 and self._virtualPos.y == 0:
				return self._origin 
			elif self._virtualPos.x == 0:
					return sf.Vector2(self._origin.x, \
							self._pos.y/self._virtualPos.y*\
							(self._virtualPos.y+self._origin.y))
			elif self._virtualPos.y==0:
				return sf.Vector2(self._pos.x/self._virtualPos.x*\
						(self._virtualPos.x+self._origin.x), self._origin.y)
			else:
				return sf.Vector2(self._pos.x/self._virtualPos.x*\
						(self._virtualPos.x+self._origin.x),\
						self._pos.y/self._virtualPos.y*\
						(self._virtualPos.y+self._origin.y))
		else:
			return self._pos

	def getPosOnScreen(self, withOrigin=True):
		render = self.getRender()
		if render is not None:
			return self.getPos(withOrigin) - render.getSommeViewPositionWithZoom()
		else:
			return self.getPos(withOrigin)

	def getVirtualPos(self, withOrigin=True):
		if withOrigin:
			return self._virtualPos + self._origin
		return self._virtualPos

	def getVirtualPosOnScreen(self, withOrigin=True):
		render = self.getRender()
		if render is not None:
			return self.getVirtualPos(withOrigin) - render.getSommeViewPosition()
		else:
			return self.getVirtualPos(withOrigin)

	def _setOrigin(self, newOrigin):
		"""Change the origin of the widget"""
		self.move = sf.Vector2(newOrigin-self._origin)
		self._origin = newOrigin
		self._posOrigin = Other

	def _setOriginPos(self, position):
		back = copy(self._origin)

		if position == Position.TopLeft:
			self._origin = sf.Vector2(0,0)
		elif position == Position.TopRight:
			self._origin = sf.Vector2(self.virtualSize.x,0)
		elif position == Position.Center:
			self._origin = sf.Vector2(self.virtualSize/2)
		elif position == Position.BottomLeft:
			self._origin = sf.Vector2(0,self.virtualSize.y)
		elif position == Position.BottomRight:
			self._origin = copy(self.virtualSIze)

		self.move(self._origin-back)
		self._posOrigin = position
	
	def _getRect(self):
		"""Set the Rect of the view"""
		return sf.Rectangle(self._pos, self._size)

	def _getRectOnScreen(self):
		return sf.Rectangle(self.getPosOnScreen(False),\
				self.size)

	def _getVirtualRectOnScreen(self):
		return sf.Rectangle(self.getVirtualPosOnScreen(False),\
				self.virtualSize)

	def _getVirtualRect(self):
		return sf.Rectangle(self.virtualPos, self.virtualSize)

	def _setRect(self, rect):
		"""rect is a sf.Rectangle type.
		This methode set the size and the positions of the widget"""
		self.setPos(rect.position, False)
		self.setSize(rect.size)

	def _setRelativePositionOnView(self, scale):
		render = self.getRender()
		if render and scale:
			self.pos = render.getViewSizeWithZoom() * scale

	def _setRelativeSizeOnView(self, scale):
		render = self.getRender()
		if render and scale:
			self.size = render.getViewSizeWithZoom() * scale

	isStaticToView = property(lambda self : self._isStaticToView, \
			lambda self,static: self.setIsStaticToView(static))

	origin = property(lambda self: self._origin,\
			lambda self,origin : self._setOrigin(origin))
	posOrigin = property(lambda  self: self._posOrigin,\
			lambda self,position : self._setOriginPos(position))

	size = property(lambda self : self._size,\
			lambda self, dimension, : self.setSize(dimension))
	virtualSize = property(lambda self : self._virtualSize)

	pos = property(lambda self: self.getPos(), \
			lambda self,pos : self.setPos(pos))
	posOnScreen = property(lambda self:self.getPosOnScreen(),\
			lambda self,position:self.setPosOnScreen())
	virtualPos = property(lambda self: self.getVirtualPos())
	virtualPosOnScreen = property(lambda self:self.getVirtualPosOnScreen())

	rect = property(lambda self:self._getRect(),\
			lambda self, rect:self._setRect(rect))
	virtualRect = property(lambda self:self._getVirtualRect())
	rectOnScreen = property(lambda self:self._getRectOnScreen(),\
			lambda self,rect : self._setRectOnScreen(rect))
	virtualRectOnScreen = property(lambda self:self._getVirtualRectOnScreen())

	globalScale = property(lambda self:self._scale,\
			lambda self,newScale : self._setScale(newScale))
	event = property(lambda self:self._event)
	isDrawing = property(lambda self:self._isDrawing,\
			lambda self,draw:self.drawWidget(draw))
	relativePositionOnView=property(lambda self:self._relativePositionOnView,\
			lambda self,scale:self._setRelativePositionOnView(scale))
	relativeSizeOnView=property(lambda self:self._relativeSizeOnView,\
			lambda self,scale:self._setRelativeSizeOnView(scale))
