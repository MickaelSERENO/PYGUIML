import sfml as sf
from Widget import Widget

class Render:
	"""Basic virtual class for all Render's class"""

	def __init__(self, parent, rect, backgroundColor=sf.Color.BLACK, title=str(), backgroundImage=Image()):
		Widget.__init__(parent, rect)
		self.backgroundColor = copy(backgroundColor)
		self._backgroundImage = backgroundImage.getCopyWidget
		sefl._backgroundImage.parent = self
		self._backgroundImage.rect = self.rect

		self._view = sf.View()

	def show(self):
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

	def setViewport(self, rect):
		self._view.viewport = rect
		self.view = self._view

	def _setBackgroundImage(self, backgroundImage):
		self.backgroundImage = backgroundImage.getCopyWidget
		self.backgroundImage.rect = self.rect
		self.backgroundImage.parent = (self.parent, 0)
	
	def _setView(self, view): #It is a lot of use for refresh the view
		self._view = view

	def _getViewport(self):
		return self._view.viewport

	def _getBackgroundImage(self):
		return self._backgroundImage

	def _getView(self):
		return self._view

	backgroundImage = property(_getBackgroundImage, _setBackgroundImage)
	view = property(_getView, _setView)
