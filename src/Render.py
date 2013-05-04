import sfml as sf
from Image import Image
from Widget import Widget
from copy import copy
import functions

class Render(Widget):
	"""Basic virtual class for all Render's class"""

	def __init__(self, parent, rect, backgroundColor=sf.Color.BLACK,\
			title=str(), backgroundImage=Image()):
		Widget.__init__(self,parent, rect)
		self.canFocus = False
		self.backgroundColor = backgroundColor
		self._backgroundImage = backgroundImage

	def show(self, render):
		raise NotImplementedError

	def moveView(self, move):
		newView = self.view
		newView.move(move.x, move.y)
		self.view = newView

	def zoomView(self,zoom):
		newView = self.view
		newView.zoom(zoom)
		self.view = newView

	def resizeView(self, size):
		self.view.size(size)
		self.view = self.view

	def resetView(self):
		self.view = self.default_view

	def setViewSize(self, size):
		newView = self.view
		newView.size = size
		self.view = newView

	def setViewPosition(self, pos):
		viewCopy = self.view
		viewCopy.center = sf.Vector2(pos - self.view.size / 2)
		self.view = viewCopy

	def setViewport(self, viewport):
		viewCopy = self.view
		viewCopy.viewport = viewport 
		self.view = viewCopy

	def getViewPosition(self):
		return sf.Vector2(self.view.center[0],self.view.center[1]) + \
				sf.Vector2(self.view.size[0],self.view.size[1]) / 2

	def getSommeViewPosition(self):
		render = Widget.getRender()
		rect = self.getViewRectWithZoom()
		if isinstance(render,Render):
			return sf.Vector2(render.getSommeViewPosition() +\
					sf.Vector2(rect.left, rect.top))
		else:
			return sf.Vector2(rect.left, rect.top)

	def getViewRect(self):
		return sf.Rectangle(self.getViewPosition(), self.view.size)

	def getViewRectWithZoom(self):
		viewRect = self.getViewRect()
		scale = self.getViewScale()
		return sf.Rectangle(\
				sf.Vector2(viewRect.left*scale.left, viewRect.top*scale.top),\
				sf.Vector2(viewRect.width * scale.width,\
					viewRect.height * scale.height))

	def getRender(self):
		return self

	def isInView(self,rect):
		return functions.rectCollision(rect,self.view.viewport)

	def getViewScale(self):
		if self.size.x != 0 or self.size.x != 0:
			return sf.Rectangle(sf.Vector2(\
					self.viewport.left*self.view.size.x+1,\
					self.viewport.top * self.view.size.y + 1),\
					\
					sf.Vector2(self.viewport.width / \
					(self.view.size.x / self.size.x),\
					self.viewport.height / (self.view.size.y / self.size.y)))
		return sf.Rectangle(sf.Vector2(1,1),sf.Vector2(1,1))

	def _setSize(self,size):
		self._backgroundImage.size = size
		if not isinstance(self,sf.Window):
			self.size = size

	def _setBackgroundImage(self, backgroundImage):
		self._backgroundImage = backgroundImage
		self._backgroundImage.setPos(sf.Vector2(0,0),False)
		self._backgroundImage.size = self.size
		self._backgroundImage.setParent(self.parent, 0)
	
	def _setView(self, view):
		back = self.getViewRectWithZoom()
		back = sf.Vector2(back.left, back.top)
		super(Render,self.__class__).view.__set__(self,view)

		for child in self._child:
			if isinstance(child,Widget) and child.isStaticToView:
				child.setPos(child.pos - back)

	def _setViewport(self, rect):
		newView = self.view
		newView.viewport = rect
		self.view = newView

	def _setTitle(self, title):
		self._title  = title

	size = property(lambda self:sf.RenderWindow.size.__get__(self),\
			lambda self,size:self._setSize(size))
	backgroundImage = property(lambda self:self._backgroundImage,\
			lambda self,image: self._setBackgroundImage(image))
	viewport = property(\
			lambda self:self.view.viewport,\
			lambda self,rect : self._setViewport(rect))
	title = property(lambda self:self._title,\
			lambda self,title : self._setTitle(title))
	
	view = property(lambda self:super().view,\
			lambda self,view : self._setView(view))
