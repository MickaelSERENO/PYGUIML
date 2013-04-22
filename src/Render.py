import sfml as sf
from Widget import Widget
from Image import image

class Render(Widget):
	"""Basic virtual class for all Render's class"""

	def __init__(self, parent, rect, backgroundColor=sf.Color.BLACK,\
			title=str(), backgroundImage=Image()):
		Widget.__init__(parent, rect)
		self.canFocus = False
		self.backgroundColor = copy(backgroundColor)
		self._backgroundImage = backgroundImage.getCopyWidget
		sefl._backgroundImage.setParent = (self, 0)
		self._backgroundImage.rect = self.rect

		self._view = sf.View()

	def show(self, render):
		raise NotImplementedError

	def moveView(self, pos):
		self._view.move(pos)
		self.view = self._view

	def resizeView(self, size):
		self._view.size(size)
		self.view = self._view

	def resetView(self):
		raise NotImplementedError

	def setViewPosition(self, pos):
		self._view.viewport(sf.FloatRect(pos.x, pos.y, self._view.size.x, self._view.size.y))
		self.view = self._view

	def _setBackgroundImage(self, backgroundImage):
		self._backgroundImage = backgroundImage.getCopyWidget
		self._backgroundImage.rect = self.rect
		self._backgroundImage.setParent(self.parent, 0)
	
	def _setView(self, view): #It is a lot of use for refresh the view
		self._view = view

	def _setViewport(self, rect):
		self._view.viewport = rect
		self.view = self._view

	backgroundImage = property(lambda self:self._backgroundImage,\
			_setBackgroundImage)
	view = property(lambda self:self._view,\
			lambda self,view:self._setView(view))
	viewport = property(lambda self:self._view.viewport,\
			lambda self,rect : self._setViewport(rect))
