import sfml as sf
from Widget import Widget
from EventManager import EventManager
from Image import Image

class Window(Widget, sf.RenderWindow):
	"""This class create a window
	Cette classe créé une fenêtre"""

	def __init__(self, videoMode, title, parent=0, framerateLimit=60, colorBackground = sf.Color.BLACK, imageBackground = Image()):
		sf.RenderWindow.__init__(self, videoMode, title)
		Widget.__init__(self, parent, sf.FloatRect(0, 0, videoMode.width, videoMode.height))

		self.framerate_limit = framerateLimit
		self.colorBackground = colorBackground
		self._imageBackground = imageBackground.getCopyWidget()
		self._imageBackground.parent = self
		self._imageBackground.rect = self.rect

		self._framerateCopy = 0
		self._framerate = framerateLimit
		self._framerateTime = 0
		self._event = EventManager(self)

	def update(self):
		"""Update the Window. It Update all event, and update framerate. It Draw and display also all drawables' widgets child"""
		if self._isDrawing:
			self._event.update()
		
			self._framerateCopy += 1
			self._framerateTime += self._event.elapsedTime
			if self._framerateTime >= 1000:
				self._framerate = self._framerateCopy
				self._framerateCopy = 0
				self._framerateTime = 0

			if self.getEvent().isResize:
				oldSize = self.getEvent().oldWindowSize
				newSize = self.getEvent().newWindowSize
				size = sf.Vector2f(self._dimensions.x * newSize.x / oldSize.x, self._dimensions.y * newSize.y / oldSize.y)
				pos = sf.Vector2f(self._pos.x * newSize.x / oldSize.x, self._pos.y * newSize.y / oldSize.y)
				for it in self._child:
					it._resizeWidget(pos, size)
	
			self.clear(self.colorBackground)
			drawable = list()
			Widget.update(self, drawable)
			self.show(drawable)

	def show(self, drawable):
		"""Show all drawables. Often, you needn't call this methode but call the Update methode"""
		for it in drawable:
			self.draw(it)
		self.display()

	def _setDimensions(self, size):
		Widget.dimensions = size
		sf.RenderWindow.size = size
		self._imageBackground.scale = sf.Vector2f(size.x/self._imageBackground.local_bounds, size.y/self._imageBackground.local_bounds)
		
	def _setPos(self, position):
		Widget._setPos(self, position)
		self.position = position
	
	def _getImageBackground(self):
		return self._imageBackground

	def _setImageBackground(self, background):
		self._imageBackground = background.getCopyWidget()
		self.addChild(self._imageBackground, 1)
		self._imageBackground.rect = sf.FloatRect(0, 0, self._dimensions.x, self._dimensions.y)

		
	def _getFramerate(self):
		return self._framerate

	def _resizeWidget(self, pos, size):
		self._dimensions = size

	def getEvent(self):
		return self._event
	
	imageBackground = property(_getImageBackground, _setImageBackground)
	framerate = property(_getFramerate)
	event = property(getEvent)
