import sfml as sf
from Image import Image
from Widget import Widget

class Render(Widget, sf.RenderTarget):
	"""Basic virtual class for all Render's class"""

	def __init__(self, parent, rect, backgroundColor=sf.Color.BLACK,\
			title=str(), backgroundImage=Image()):
		sf.RenderTarget.__init__(self)
		Widget.__init__(self,parent, rect)
		self.canFocus = False
		self.backgroundColor = copy(backgroundColor)
		self._backgroundImage = backgroundImage
		sefl._backgroundImage.setParent = (self, 0)
		self._backgroundImage.rect = self.rect
		sf.RenderTarget.view.fset(self,sf.View())

	def show(self, render):
		raise NotImplementedError

	def moveView(self, movee):
		newView = copy(self.view)
		newView.move(move)
		self.view = newView

	def resizeView(self, size):
		self._view.size(size)
		self.view = self._view

	def resetView(self):
		raise NotImplementedError

	def setViewPosition(self, pos):
		viewCopy = copy(self._view)
		viewCopy.center = sf.Vector2f(pos - self._view.size / 2)
		self.view = viewCopy

	def getViewPosition(self):
		return sf.Vector2f(self._view.center + self._view.size / 2)

	def getSommeViewPosition(self):
		render = Widget.getRender()
		if isinstance(render,Render):
			return sf.Vector2f(render.getSommeViewPosition() +\
					self.getViewPosition())
		else:
			return self.getViewPosition()

	def getViewport(self):
		return self._view.viewport

	def getViewRect(self):
		return sf.FloatRect(self._view.getViewPosition().x,\
				self._view.getViewPosition().y, \
				self._view.size.x, self._view.size.y)

	def getRender(self):
		return self

	def isInView(self,rect):
		return functions.rectCollision(rect,self.getViewRect())

	def _setBackgroundImage(self, backgroundImage):
		self._backgroundImage = backgroundImage.getCopyWidget
		self._backgroundImage.rect = self.rect
		self._backgroundImage.setParent(self.parent, 0)
	
	def _setView(self, view):
		back = getViewPosition()
		sf.RenderTarget.view.fset(self,view)

		for child in self._child:
			if isinstance(child,Widget) and child.isStaticToView:
				child.setPos(child.pos - back)

	def _setViewport(self, rect):
		newView = copy(self.view)
		newView.viewport = rect
		self.view = newView

	def _setTitle(self, title):
		self._title  = title
	backgroundImage = property(lambda self:self._backgroundImage,\
			_setBackgroundImage)
	viewport = property(lambda self:sf.RenderTarget.view.fget(self).viewport,\
			lambda self,rect : self._setViewport(rect))
	title = property(lambda self:self._title,\
			lambda self,title : self._setTitle(title))
	
	view = property(lambda self:sf.RenderTarget.view.fget(self),\
			lambda self,view : self._setView(view))
