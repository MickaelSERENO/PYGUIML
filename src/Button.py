from Widget import Widget
from Widget import Position
from Label import Label
from Image import Image
from Active import Active
import decorator
import sfml as sf

class Button(Widget, Active):
	"""This Widget is a Button. It regrouped a guiml.Image and guiml.Label.
	With it, you can use a real Button."""
	def __init__(self, parent, text=None, image=None, rect=sf.Rectangle()):
		Widget.__init__(self, parent, rect)
		Active.__init__(self)
		
		self._text = text
		self._textLighten = text
		self._currentText = self._text

		self._image = image
		self._imageLighten = image
		self._currentImage = self._image
		self._useCharacterSize = None

		if image:
			self._imageLighten.lighten()
			self._image.canFocus = self._imageLighten.canFocus = False
			self._image.isStaticToView =\
					self._imageLighten.isStaticToView = False
		if text:
			self._textLighten.lighten()
			self._image.canFocus = self._imageLighten.canFocus = False
			self._text.isStaticToView =\
					self._textLighten.isStaticToView = False

		if rect == sf.Rectangle() and not(self._image or self._text):
			self.rect = rect

		elif self._hasImage:
			self.rect = self._image.rect

		elif self._hasLabel:
			self.rect = self._text.rect

		self.howActiveKeyboard = sf.Keyboard.SPACE
		self.howActiveMouse = sf.Mouse.LEFT
		self.drawWidget(True)

	@decorator.forUpdate
	def update(self, render=None):
		Active.update(self)
		Widget.update(self, render)

	@decorator.forDrawing
	def draw(self, render=None):
		if render:
			render.draw(self._currentImage)
			render.draw(self._currentText)

	def centerLabel(self):
		"""Set The text at the button's middle"""
		if self._text:
			self._text.posOrigin = Position.Center
			self._textLighten = Position.Center

	def howSelect(self):
		return Widget.widgetFocus is self

	def selectIt(self):
		self.lightUpDrawable(True)

	def deselectIt(self):
		self.lightUpDrawable(False)

	def howActive(self):
		return self.isSelect and self.event and \
				(self.event.getOneMouseClicked(self.howActiveMouse) or\
				self.event.getOnePressedKeys(self.howActiveKeyboard))

	def lightUpDrawable(self, lighten = True):
		"""Light Up the Button if lighten is True value"""

		if lighten:
			if self._image:
				self._imageLighten.parent = self
				self._image.parent = 0
				self._currentImage = self._imageLighten
				
			if self._text:
				self._textLighten.parent = self
				self._text.parent = 0
				self._currentText = self._textLighten

		else:
			if self._image:
				self._imageLighten.parent = 0
				self._image.parent = self
				self._currentImage = self._image

			if self._text:
				self._textLighten.parent = 0
				self._text.parent = self
				self._currentText = self._text

	def drawWidget(self, draw=True):
		if self._text:
			self._text.isDrawing = True
			self._textLighten.isDrawing = True
		if self._image:
			self._image.isDrawing = True
			self._imageLighten.isDrawing = True
		Widget.drawWidget(self, draw)

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)

		if self.hasImage:
			self._image.pos = self.pos
			self._imageLighten.pos = self.pos
		if self.hasLabel:
			self._text.pos = self.pos + self.size/2
			self._textLighten.pos = self.pos + self.size/2

	def _setSize(self, size):
		Widget._setSize(self, size)

		if self.hasImage:
			self._image.size = self.virtualSize
			self._imageLighten.size = self.virtualSize

		if self.hasLabel and not self.useCharacterSize:
			self._text.setTextWidthSize(self.virtualSize.x)
			self._textLighten.setTextWidthSize(self.virtualSize.x)

			if self.virtualSize.y > 0 and \
					self._text.virtualSize.y > self.virtualSize.y :
				self._text.setTextHeightSize(self.virtualSize.y)
				self._textLighten.setTextHeightSize(self.virtyalSize.y)

	def _drawWidget(drawing):
		self._text._isDrawing = drawing
		self._textLighten._isDrawing = drawing
		self._image._isDrawing = drawing
		self._imageLighten._isDrawing = drawing
		self.isDrawing = drawing

	def _setImage(self, image):
		"""image is a Image type"""

		self._image = image
		self._imageLighten = image
		self._imageLighten.lighten()

		if image:
			self._image.canFocus = self._imageLighten.canFocus = False
			self._image.isStaticToView = \
					self._imageLighten.isStaticToView = False

		self.rect = self.rect
	def _setText(self, text):
		"""text is Label type"""

		self._text = text.getCopyWidget()
		self._textLighten = text.getCopyWidget()
		self._textLighten.lighten()
		if text:
			self._text.canFocus = self._textLighten.canFocus = False
			self._text.isStaticToView = \
					self._textLighten.isStaticToView = False

		self.rect = self.rect
		self.updateSelection()
		self.centerLabel()

	def _setUseCharacterSize(self, use=True):
		self._useCharacterSize = use
	
	def _setCharacterSize(self, size):
		if self.hasLabel:
			self._text.characterSize = size
			self._textLighten.characterSize = size
		self.useCharacterSize = True

	image = property(lambda self:self._currentImage, _setImage)
	text = property(lambda self:self._currentText, _setText)
	basicText = property(lambda self:self._text)
	basicImage = property(lambda self:self._image)
	textLighten = property(lambda self:self._textLighten)
	imageLighten= property(lambda self:self._imageLighten)
	hasLabel = property(lambda self:bool(self._text))
	hasImage = property(lambda self:bool(self._image))
	characterSize =property(lambda self:self._text.characterSize,\
			_setCharacterSize)
	useCharacterSize = property(lambda self:self._useCharacterSize,\
			_setUseCharacterSize)

