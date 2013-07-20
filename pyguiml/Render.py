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
		self._backgroundImage=None
		self.backgroundColor = backgroundColor
		self.backgroundImage = backgroundImage
		self._clipRect = None
		self._clipPosParent = None
		self._title = title
		self._currentViewSizeClip = None

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
		else:
			return self.map_coords_to_pixel(position)

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
		if not isinstance(self,sf.Window):
			self.size = size

	def _setBackgroundImage(self, backgroundImage):
		if self._backgroundImage:
			self.removeChild(self._backgroundImage)
		if backgroundImage:
			self.addChild(backgroundImage, 0)
			self._backgroundImage = backgroundImage
			self._backgroundImage.size = self.view.size
			self._backgroundImage.pos = self.getViewPosition()
			self._backgroundImage.canUpdate = True
			self._backgroundImage.isDrawing = True
	
	def _setView(self, view):
		super(Render,self.__class__).view.__set__(self,view)

		if not self._clipRect:
			for child in self._child:
				if isinstance(child,Widget) and child.isStaticToView:
					child.setPosOnView(child.pos)

			self.backgroundImage = self.backgroundImage

	def _setViewport(self, rect):
		newView = self.view
		newView.viewport = rect
		self.view = newView

	def _setTitle(self, title):
		self._title  = title
		
	def clipping(self, funcDraw, rect, posWidget, funcUpdate=None):
		if not 0 in self.size:
			if not self._currentViewSizeClip:
				self._currentViewSizeClip = copy(self.view.size)
			rect = copy(rect)
			oldClip = copy(self._clipRect)
			oldPosParent = self._clipPosParent
			currentView = self.view
			if self._clipRect:
				if rect.left + posWidget.x < self._clipRect.left:
					rect.width = max(0, rect.left + rect.width + posWidget.x\
							-self._clipRect.left)
					rect.left = self._clipRect.left - self._clipPosParent.x
				else:
					rect.width = min(self._clipRect.left + \
							self._clipRect.width - rect.left-posWidget.x, \
							rect.width)

				if rect.top+posWidget.y < self._clipRect.top:
					rect.top = self._clipRect.top
					rect.height = max(\
							0, rect.top + rect.height + posWidget.y\
							-self._clipRect.top)
					rect.top = self._clipRect.top - self._clipPosParent.y
				else:
					rect.height= min(self._clipRect.top + \
							self._clipRect.height - rect.left-posWidget.y, \
							rect.height)

			rect.width = max(0, rect.width)
			rect.height = max(0, rect.height)


			clippingView = sf.View(rect)
			clippingView.move(posWidget.x, posWidget.y)
			clippingView.viewport = sf.Rectangle((posWidget+rect.position) /\
					self._currentViewSizeClip, rect.size /\
					self._currentViewSizeClip)
			self.view = clippingView
			self._isClipping = True
			self._clipRect = sf.Rectangle(posWidget+rect.position, rect.size)
			self._clipPosParent = posWidget
			
			funcDraw(self)
			if funcUpdate:
				funcUpdate(self)
			super(Render, self.__class__).view.__set__(self, currentView)
			self._clipRect = oldClip
			self._clipPosParent = oldPosParent
			self._currentViewSizeClip = None

	def getClipRect(self):
		render = self.getRender()
		if render is not self and render._isClipping:
			return render.getClipRect()
		return self._clipRect

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
