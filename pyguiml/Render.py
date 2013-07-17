import sfml as sf
from Image import Image
from Widget import Widget
from copy import copy
from functools import reduce
import functions

class Render(Widget):
	"""Basic virtual class for all Render's class"""

	def __init__(self, parent=None, rect=sf.Rectangle, backgroundColor=sf.Color.BLACK,\
			title=str(), backgroundImage=Image()):
		Widget.__init__(self,parent, rect)
		self.canFocus = False
		self.backgroundColor = backgroundColor
		self._backgroundImage = backgroundImage
		self._title = title

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
		moveView(pos - self.getViewPosition())

	def setViewport(self, viewport):
		viewCopy = self.view
		viewCopy.viewport = viewport 
		self.view = viewCopy

	def getViewPositionWithViewport(self):
		return  self.view.center + self.viewport.position * self.size - \
				self.view.size / 2

	def getViewPosition(self):
		return self.view.center - self.view.size / 2
	
	def getViewSizeWithViewport(self):
		return self.view.size * self.view.viewport.size

	def getViewSizeWithZoom(self):
		return self.getViewSizeWithViewport() * self.getViewScale()

	def convertScreenCoordToTargetPoint(self, position):
		render = self.getRender()
		if isinstance(render,Render) and render is not self:
			return render.map_pixel_to_coords(position) - \
					render.convertTargetPointToScreenCoord(self.pos)
		else:
			return render.map_pixel_to_coords(position)

	def convertTargetPointToScreenCoord(self, position):
		render=None
		if self.parent:
			render = self.parent.getRender()
		if isinstance(render,Render) and render is not self:
			return render.convertTargetPointToScreenCoord(self.pos) + \
					render.map_coords_to_pixel(position)
		elif render:
			return render.map_coords_to_pixel(position)
		else:
			return position

	def getViewRect(self):
		return sf.Rectangle(self.getViewPosition(),\
				self.view.size)

	def getRender(self):
		return self

	def isInView(self,rect):
		return functions.rectCollision(rect,self.getViewRect())

	def getViewScale(self):
		render = self.getRender()
		if render and\
				(render.getViewSizeWithViewport().x != 0 or render.getViewSizeWithViewport().y != 0):
			return render.sizeOnView / self.view.size
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
		super(Render,self.__class__).view.__set__(self,view)

		for child in self._child:
			if isinstance(child,Widget) and child.isStaticToView:
				child.setPosOnView(child.pos)

	def _setViewport(self, rect):
		newView = self.view
		newView.viewport = rect
		self.view = newView

	def _setTitle(self, title):
		self._title  = title
		
	def clipping(self, funcDraw, rect, funcUpdate=None):
		currentView = self.view
		clippingView = sf.View(rect)
		clippingView.viewport = sf.Rectangle(rect.position / self.size, \
				rect.size / self.size)
		super(Render, self.__class__).view.__set__(self, clippingView)
		
		funcDraw(self)
		if funcUpdate:
			funcUpdate(self)
		super(Render, self.__class__).view.__set__(self, currentView)

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

def addSizeBetweenPosAndCenter(result, difference, n):
	return result + difference/2**n