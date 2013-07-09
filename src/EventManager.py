import sfml as sf
from copy import copy

class EventManager:
	nbrKey = 321
	nbrClick = 3

	def __init__(self, window):
		if isinstance(window, sf.Window):
			self._w = window
			self._keys = list()
			self._click = list()
			self._mousePos = sf.Vector2()
			self._oldMousePos = sf.Vector2()
			self._elapsedTime = 0
			self._clock = sf.Clock()
			self._isInputKeys = list()
			self._isInputClick = list()
			self._hasPressedKeyKey = False
			self._isResize = False
			self._oldWindowSize = sf.Vector2(window.width, window.height)
			self._newWindowSize = sf.Vector2(window.width, window.height)
			self._enteredText = False
			self._text = 0
			self._hasPressedKeyMouse = False
			self._defaultWindowSize = sf.Vector2(window.size)
			self._multiplicateMouse = sf.Vector2(1,1)

			i = 0
			for i in range(EventManager.nbrKey):
				self._keys.append(False)
				self._isInputKeys.append(False)

			i = 0
			for i in range(EventManager.nbrClick):
				self._click.append(False)
				self._isInputClick.append(False)
		else:
			raise TypeError("window is not sf.RenderWindow type")

	def update(self):
		"""Update the class : it see if there are news events"""
		self._elapsedTime = self._clock.elapsed_time.microseconds
		self._clock.restart()

		if self._hasPressedKeyMouse:
			for i in range(EventManager.nbrClick):
				self._isInputClick[i] = False

		if self._hasPressedKeyKey:
			for i in range(EventManager.nbrKey):
				self._isInputKeys[i] = False
				
		self._enteredText = False
		self._isResize = False

		self._hasPressedKeyKey = False
		self._hasPressedKeyMouse= False

		for event in self._w.events:
			if type(event) is sf.KeyEvent and event.pressed:
				if event.code <= EventManager.nbrKey:
					self._keys[event.code] = True
					self._isInputKeys[event.code] = True
					self._hasPressedKeyKey = True

			if type(event) is sf.KeyEvent and event.released:
				self._keys[event.code] = False
				self._isInputKeys[event.code] = False

			if type(event) is sf.TextEvent:
				self._text = event.unicode
				self._enteredText = True

			if type(event) is sf.MouseButtonEvent and event.pressed:
				if event.button <= EventManager.nbrClick:
					self._click[event.button] = True
					self._isInputClick[event.button] = True
					self._hasPressedKeyMouse = True

			if type(event) is sf.MouseButtonEvent and event.released:
				self._click[event.button] = False
				self._isInputClick[event.button] = False

			if type(event) is sf.MouseMoveEvent:
				self._oldMousePos = copy(self._mousePos)
				self._mousePos = event.position

			if type(event) is sf.CloseEvent:
				self._w.close()

			if type(event) is sf.ResizeEvent:
				self._isResize = True
				self._oldWindowSize = sf.Vector2(self._newWindowSize.x,\
						self._newWindowSize.y)
				self._newWindowSize = event.size

		if self._keys[sf.Keyboard.BACK_SPACE]:
			self._enteredText = False

		if self._isResize and self._defaultWindowSize.x != 0 and\
				self._defaultWindowSize.y != 0:
			self._multiplicateMouse.x = self._newWindowSize.x / \
					self._defaultWindowSize.x
			self._multiplicateMouse.y = self._newWindowSize.y / \
					self._defaultWindowSize.y

	def isMouseInRect(self, rect):
		if self._mousePos.x > rect.left and\
				self._mousePos.y > rect.top and\
				self._mousePos.x < rect.left + rect.width and\
				self._mousePos.y < rect.top + rect.height :
			return True

		return False

	def getPressedKeys(self, key):
		if key <= EventManager.nbrKey:
			return self._keys[key]
		else:
			return False

	def getOnePressedKeys(self, key):
		if key <= EventManager.nbrKey:
			return self._isInputKeys[key]
		else:
			return False

	def getMouseClicked(self, key):
		if key <= EventManager.nbrClick:
			return self._click[key]
		else:
			return False

	def getOneMouseClicked(self, key):
		if key <= EventManager.nbrClick:
			return self._isInputClick[key]
		else:
			return False

	text = property(lambda self:self._text)
	enteredText = property(lambda self:self._enteredText)
	mousePos = property(lambda self:self._mousePos)
	oldMousePos = property(lambda self:self._oldMousePos)
	elapsedTime = property(lambda self:self._elapsedTime)
	isResize = property(lambda self:self._isResize)
	oldWindowSize = property(lambda self:self._oldWindowSize)
	newWindowSize = property(lambda self:self._newWindowSize)
	defaultWindowSize = property(lambda self:self._defaultWindowSize)
	multiplicateMouse = property(lambda self:self._multiplicateMouse)
