import sfml as sf
from Render import Render
from Updatable import Updatable
from Widget import Widget
from EventManager import EventManager
from Image import Image

class Window(Render, sf.RenderWindow):
	"""This class create a window
	Cette classe créé une fenêtre"""

	def __init__(self, videoMode=sf.VideoMode(800, 600, 32), \
			title="window", parent=0, framerateLimit=60,\
			backgroundColor = sf.Color.BLACK, backgroundImage = Image()):

		sf.RenderWindow.__init__(self, videoMode, title)
		Render.__init__(self, parent, sf.Rectangle(sf.Vector2(),\
				videoMode.size), backgroundColor, backgroundImage)

		self._isStaticToView = False
		self.position = (0,0)
		self.framerate_limit = framerateLimit
		self._event = EventManager(self)
		self.resetView()
		self.clear(backgroundColor)

#	def updateFocus(self):
#		return Updatable.updateFocus(self)

	def update(self):
		"""Update the Window. It Update all event, and update framerate.
		It Draw and display also all widgets child"""
		if self.isDrawing:
			self._event.update()

			if self._event.isResize:
				Render._setSize(self,self.size)
	
			Widget.widgetFocus =  None

			if self.event.isMouseInRect(self.rectOnScreen):
				Updatable._focusIsChecked= False
				Updatable.updateFocus(self)
			else:
				Widget.widgetFocus = None
			Widget.update(self, self)
			self.display()
			self.clear(self.backgroundColor)

	def getEventFromRootParent(self):
		return self._event

	def _setSize(self, size):
		sf.RenderWindow.size.__set__(self, size)
		Widget.size.__set__(self,size)
		self._event._defaultWindowSize = size

	def getPosOnScreen(self, *args):
		return sf.Vector2(0,0)

	def setPos(self, position, *args):
		Widget.setPos(position, False)
		self.position = position

	def _setView(self,view):
		sf.RenderWindow.view.__set__(self, view)
		Render._setView(self,view)

	size = property(lambda self : sf.RenderWindow.size.__get__(self), _setSize)
	event = property(lambda self:self._event)
	framerate = property(lambda self:1/(self._event.elapsedTime*10**-6))
	setPosOnScreen = setPos
	draw = sf.RenderWindow.draw
	sizeOnScreen = property(lambda self:self.size)
