import sfml as sf
from Render import Render
from Updatable import Updatable
from Widget import Widget
from EventManager import EventManager
from Image import Image

class Window(Render, sf.RenderWindow):
	"""This class create a window
	Cette classe créé une fenêtre"""

	def __init__(self, videoMode, title, parent=0, framerateLimit=60,\
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

	def updateFocus(self):
		return;

	def update(self):
		"""Update the Window. It Update all event, and update framerate.
		It Draw and display also all widgets child"""
		if self.isDrawing:
			self._event.update()
			self._framerate = 1/(self.event.elapsedTime*10**-6)

			if self._event.isResize:
				Render._setSize(self,self.size)
				Widget._resizeWidget(self)
				print("ok")
				
	
			Widget.widgetFocus =  None
			Updatable._focusIsChecked = False


			if self.event.isMouseInRect(self.rectOnScreen):
				Updatable.updateFocus(self)
			Widget.update(self, self)
			self.display()
			self.clear(self.backgroundColor)

	def getEventFromRootParent(self):
		return self._event

	def _setSize(self, size):
		print("ok")
		Widget.size.__set__(self,size)

	def getPosOnScreen(self, *args):
		return sf.Vector2(0,0)

	def setPos(self, position, *args):
		Widget.setPos(position, False)
		self.position = position

	def _setView(self,view):
		sf.RenderWindow.view.__set__(self, view)
		Render._setView(self,view)
	
	def _resizeWidget(self, pos, size):
		self._size = size
		self._virtualSize = size
	
	size = sf.RenderWindow.size
	virtualSize = size
	event = property(lambda self:self._event)
	framerate = property(lambda self:1/self._event.elapsedTime*0.001)
	setPosOnScreen = setPos
