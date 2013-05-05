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
		if self.canUpdate:
			if not render:
				render = self.getRender()

			if render:
				if self._changeWindow:
					if self._isStaticToView:
						self.setRect(self.virtualPos -\
								render.getViewPosition(), self.virtualSize)
					else:
						self.setRect(self._getVirtualRect())

				if self.isDrawing and render.isInView(self._getVirtualRect()):
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
		for child in self._child:
			if isinstance(child,Widget):
				child._isDrawing = True

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

		newWindowSize = self._event.newWindowSize
		defaultWindowSize = self._event.defaultWindowSize

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

		for child in self._child:
			if isinstance(child,Widget):
				child.resizeWidget(defaultWindowSize, newWindowSize);

	def setPos(self, pos, withOrigin=True):
		if self.movingAllChild:
			for child in self._child:
				child.move(pos.x - self._virtualPos.x, \
						pos.y - self._virtualPos.y)

		render = self.getRender()
		addView = sf.Vector2(0,0)

		if render is not None and self._isStaticToView:
			addView = copy(render.getViewRectWithZoom())
			addView = sf.Vector2(addView.left, addView.top)

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

	def setSize(self, size):
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
			if self._pos.x == 0 and self._pos.y == 0:
				return self._origin 
			elif self._pos.x == 0:
					return sf.Vector2(self._origin.x, \
							self._pos.y/self._virtualPos.y*\
							(self._virtualPos.y+self._origin.y))
			elif self._pos.y==0:
				return sf.Vector2(self._pos.x/self._virtualPos.x*\
						(self._virtualPos.x+self._origin.x), self._origin.y)
			else:
				return sf.Vector2(self._pos.x/se._virtualPos.x*\
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
					return sf.Vector2(self.getPos(withOrigin) -\
						render.getViewPosition() *\
						newWindowSize / defaultWindowSize)\
			
		return self.getVirtualPos(withOrigin)

	def getVirtualPos(self, withOrigin=True):
		if withOrigin:
			return self._virtualPos + self._origin
		return self._virtualPos

	def getVirtualPosOnScreen(self, withOrigin=True):
		render = self.getRender()
		if render is not None:
			return self.getVirtualPos(withOrigin)-render.getViewPosition()
		else:
			return self.getVirtualPos(withOrigin)

	def getSizeOnScreen(self):
		render = self.getRender()
		if render:
			return self._size*render.getViewScale().size
		return self._size

	def getVitualSizeOnScreen(self):
		render = self.Render()
		if render:
			return self.virtualSize*render.getViewScale().size
		return self.virtualSize

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
				self.getSizeOnScreen())

	def _getVirtualRectOnScreen(self):
		return sf.Rectangle(self.getVirtualPosOnScreen(False),\
				self.getVirtualSizeOnScreen())

	def _getVirtualRect(self):
		return sf.Rectangle(self.virtualPos, self.virtualSize)

	def _setRect(self, rect):
		"""rect is a sf.Rectangle type.
		This methode set the size and the positions of the widget"""
		self.setPos(rect.position, False)
		self.setSize(rect.size)

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
