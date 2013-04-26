import sfml as sf
from Render import Render
from EventManager import EventManager

class Window(Render, sf.RenderWindow):
	"""This class create a window
	Cette classe créé une fenêtre"""

	def __init__(self, videoMode, title, parent=0, framerateLimit=60,\
			colorBackground = sf.Color.BLACK, imageBackground = Image()):
		sf.RenderWindow.__init__(self, videoMode, title)
		Render.__init__(self, parent, sf.FloatRect(0, 0, videoMode.width,\
				videoMode.height), backgroundColor, backgroundImage)

		self._isStaticToView = False
		self.position = sf.Vector2f(0,0)
		self.framerate_limit = framerateLimit
		self._event = EventManager(self)
		self.resetView()

	def update(self, drawable=None):
		"""Update the Window. It Update all event, and update framerate. It Draw and display also all drawable' widgets child"""
		if self._isDrawing:
			self._event.update()
			self._framerate = 1/(self.event.elapsedTime * 0.001)

			if self.getEvent().isResize:
				Widget.resizeWidget(self.event.defaultWindowSize, self.event.newWindowSize)
	
			self.clear(self.colorBackground)
			if drawable is None:
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

	def _resizeWidget(self, pos, size):
		self._dimensions = size

	def getEvent(self):
		return self._event
	
	event = property(getEvent)
