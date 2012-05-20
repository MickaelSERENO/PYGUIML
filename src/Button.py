from Widget import Widget
from Label import Label
from Image import Image
import sfml as sf

class Button(Widget):
	"""This Widget is a Button. It regrouped a guiml.Image and guiml.Label. With it, you can use a real Button."""
	def __init__(self, parent, text=Label(), image=Image(), rect=sf.FloatRect(0,0,0,0)):
		Widget.__init__(self, parent, rect)
		
		self._text = text.getCopyWidget()
		self._textLighten = text.getCopyWidget()
		self._image = image.getCopyWidget()
		self._imageLighten = image.getCopyWidget()

		self._imageLighten.lighten()
		self._textLighten.lighten()

		self._currentImage = self._image
		self._currentText = self._text

		if self._image.dimensions.x != 0 and self._image.dimensions.y != 0 :
			self._hasImage = True
		else:
			self._hasImage = False

		if self._text.dimensions.y != 0 and self._text.dimensions.x != 0 :
			self._hasText = True
		else:
			self._hasText = False

		if rect.width != 0 and rect.height != 0 :
			self.rect = rect

		elif self._hasImage:
			self.rect = self._image.rect

		elif self._hasText:
			self.rect = self._text.rect

		self._isSelect = False
		self._isActive = False
		self._isSelectCopy = False
		self._isActiveCopy = False

		self._howActiveKeyboard = sf.Keyboard.ESCAPE
		self._howActiveMouse = sf.Mouse.LEFT

	def update(self, drawable):
		if self._isDrawing:
			self.cursorInButton()

			if self._isSelect and (self.getEvent().getOneMouseClicked(self._howActiveMouse) or self.getEvent().getOnePressedKeys(self._howActiveKeyboard)):
				self._isActive = True
			else:
				self._isActive = False

		Widget.update(self, drawable)

	def centerLabel(self):
		"""Set The text at the button's middle"""

		self._text.setOriginMiddle()
		self._text._setPos = sf.Vector2f(self.pos.x + self.dimensions.x / 2, self.pos.y + self.dimensions.y / 2)
		self._textLighten.setOriginMiddle()
		self._textLighten.pos = sf.Vector2f(self.pos.x + self.dimensions.x / 2, self.pos.y + self.dimensions.y / 2)

	def cursorInButton(self):
		"""See if the Cursor is in the Button or no. After, it lightUp the Button if the Button is select"""

		if self.getEvent().isMouseInRect(self.rect) or self._isSelectCopy:
			self._isSelect = True
			self.lightUpDrawable()
		else:
			self._isSelect = False
			self.lightUpDrawable(False)

	def lightUpDrawable(self, lighten = True):
		"""Light Up the Button if lighten is True value"""

		if lighten:
			if self._hasImage:
				self._imageLighten.parent = self
				self._image.parent = 0
				self._currentImage = self._imageLighten
				
			if self._hasText:
				self._textLighten.parent = self
				self._text.parent = 0
				self._currentText = self._textLighten

		else:
			if self._hasImage:
				self._imageLighten.parent = 0
				self._image.parent = self
				self._currentImage = self._image

			if self._hasText:
				self._textLighten.parent = 0
				self._text.parent = self
				self._currentText = self._text

	def _setDimensions(self, dimensions):
		self._image.dimensions = dimensions
		self._imageLighten.dimensions = dimensions
		self._text.setTextWidthSize(dimensions.x)
		self._textLighten.setTextWidthSize(dimensions.x)
		Widget._setDimensions(self, dimensions)
		self.centerLabel()

	def _setPos(self, pos):
		self._image.pos = pos
		self._imageLighten.pos = pos
		self._text.pos = pos
		self._textLighten.pos = pos
		Widget._setPos(self, pos)
		self.centerLabel()
		print(pos.x, pos.y)

	def _getIsDrawing(self):
		return self.__isDrawing

	def _drawWidget(drawing):
		self._text._isDrawing = drawing
		self._textLighten._isDrawing = drawing
		self._image._isDrawing = drawing
		self._imageLighten._isDrawing = drawing
		self._isDrawing = drawing

	def _getImage(self):
		return self._image

	def _setImage(self, image):
		"""image is a Image type"""

		self._image = image.getCopyWidget()
		self._imageLighten = image.getCopyWidget()
		self._imageLighten.lighten()

		if image.dimensions.x != 0 and image.dimensions.y != 0:
			self._hasImage = True
			self.rect = self.rect

		else:
			self._hasImage = False

	def _getText(self):
		return self._text

	def _setText(self, text):
		"""text is Label type"""

		self._text = text.getCopyWidget()
		self._textLighten = text.getCopyWidget()
		self._textLighten.lighten()

		if text.dimensions.x != O and text.dimensions.y != 0:
			self._hasText = True
			self.rect = self.rect

		else:
			self._hasText = False

	def _getHasLabel(self):
		return self._hasLabel

	def _getHasImage(self):
		return self._hasImage

	image = property(_getImage, _setImage)
	text = property(_getText, _setText)
	hasLabel = property(_getHasLabel)
	hasImage = property(_getHasImage)
	pos = property(Widget._getPos, _setPos)
	dimensions = property(Widget._getDimensions, _setDimensions)
