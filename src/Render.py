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

	def moveView(self, move):
		newView = self.view
		newView.move(move.x, move.y)
		self.view = newView

	def zoomView(self,zoom):
		newView = self.view
		newView.zoom(zoom)
		self.view = newView

	def resizeView(self, size):
		self.view.size = size
		self.view = self.view

	def resetView(self):
		self.view = self.default_view

	def setViewSize(self, size):
		newView = self.view
		newView.size = size
		self.view = newView

	def setViewCenter(self, center):
		viewCopy = self.view
		viewCopy.center = center
		self.view = viewCopy

	def setViewPosition(self, pos):
		viewCopy = self.view
		viewCopy.center = sf.Vector2(pos - self.view.size / 2)
		viewCopy.viewport.width -= viewCopy.viewport.left
		viewCopy.viewport.heigth -= viewCopy.viewport.top
		viewCopy.viewport.left = 0
		viewCopy.viewport.top = 0
		self.view = viewCopy

	def setViewport(self, viewport):
		viewCopy = self.view
		viewCopy.viewport = viewport 
		self.view = viewCopy

	def getViewPositionWithViewport(self):
		return sf.Vector2(self.view.center.x,self.view.center.y) - \
				sf.Vector2(self.view.size.x,self.view.size.y) / 2 + \
				self.viewport.position * self.view.size

	def getViewPosition(self):
		return sf.Vector2(self.view.center.x,self.view.center.y) - \
				sf.Vector2(self.view.size.x,self.view.size.y) / 2 
	
	def getViewPositionWithZoom(self):
		render = self.getRender()
		if render:
			return self.getViewPosition(self) * \
					(render.sizeOnScreen / \
					render.getViewSizeWithViewport())

	def getViewSizeWithViewport(self):
		return self.view.size * (self.viewport.size-self.viewport.position)

	def getViewSizeWithZoom(self):
		return self.getViewSizeWithViewport() * self.getViewScale()

	def getSommeViewPosition(self):
		render = self.getRender()
		if isinstance(render,Render) and render is not self:
			return render.getSommeViewPosition() + self.getViewPositionWithViewport()
		else:
			return self.getViewPosition()

	def getSommeViewPositionWithZoom(self):
		return self.getSommeViewPosition() * self.getViewScale()

	def getViewRect(self):
		return sf.Rectangle(self.getViewPosition(),\
				self.getViewSizeWithViewport())

	def getViewRectWithZoom(self):
		viewRect = self.getViewRect()
		return sf.Rectangle(self.getSommeViewPositionWithZoom(),\
				self.getViewSizeWithZoom())

	def getRender(self):
		return self

	def isInView(self,rect):
		return functions.rectCollision(rect,self.getViewRectWithZoom())

	def getViewScale(self):
		render = self.getRender()
		if render and\
				(render.getViewSizeWithViewport().x != 0 or render.getViewSizeWithViewport().y != 0):
			return render.sizeOnScreen / render.getViewSizeWithViewport()
		return sf.Vector2(1,1)

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
				child.relativePositionOnView = child.relativePositionOnView
				self.relativePositionOnView = self.relativePositionOnView

		Widget._resizeWidget(self)

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
