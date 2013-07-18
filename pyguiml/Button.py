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
	def __init__(self, parent=None, text=None, image=None, rect=sf.Rectangle()):
		Widget.__init__(self, parent, rect)
		Active.__init__(self)
		
		self._text = text
		self._textSelect = text
		self._textActive = self._textSelect
		self._currentText = self._text

		self._image = image
		self._imageSelect = image
		self._imageActive = self._imageSelect
		self._currentImage = self._image

		self._useCharacterSize = None

		self._hasImage = False
		self._hasLabel = False

		if image:
			self._imageSelect.lighten()
			self._image.canFocus = self._imageSelect.canFocus = False
			self._image.isStaticToView =\
					self._imageSelect.isStaticToView = False
			self._hasImage = True
		if text:
			self._textSelect.lighten()
			self._text.canFocus = self._textSelect.canFocus = False
			self._text.isStaticToView =\
					self._textSelect.isStaticToView = False
			self._hasLabel = True

		if rect != sf.Rectangle():
			self.rect = rect

		elif self._hasImage:
			self.rect = self._image.rect

		elif self._hasLabel:
			self.rect = self._text.rect

		self.drawWidget(True)

	@decorator.forUpdate
	def update(self, render=None):
		Active.update(self)
		Widget.update(self, render)

	@decorator.forDrawing
	def draw(self, render=None):
		if render:
			if(self._currentImage):
				render.draw(self._currentImage.sprite)
			if(self._currentText):
				render.draw(self._currentText.text)

	def centerLabel(self):
		"""Set The text at the button's middle"""
		if self._text:
			self._text.posOrigin = Position.Center
			self._textSelect.posOrigin = Position.Center
			self._textActive.posOrigin = Position.Center

	def howSelect(self):
		return Widget.widgetFocus is self

	def selectIt(self):
		Active.selectIt(self)
		self.changeStatus()

	def deselectIt(self):
		Active.deselectIt(self)
		self.changeStatus()

	def activeIt(self, force=False):
		Active.activeIt(self)
		self.changeStatus()

	def disactiveIt(self, force=True):
		Active.disactiveIt(self)
		self.changeStatus()

	def howActive(self):
		return self.isSelect and self.event and \
				(self.event.getOneMouseClicked(self.howActiveMouse[0]) or\
				self.event.getOnePressedKeys(self.howActiveKeyboard[0]))

	def changeStatus(self):
		if self.isSelect:
			if self._image:
				self._imageSelect.parent = self
				self._image.parent = 0
				self._imageActive.parent = 0
				self._currentImage = self._imageSelect
				
			if self._text:
				self._textSelect.parent = self
				self._text.parent = 0
				self._textActive.parent = 0
				self._currentText = self._textSelect

		elif self.isActive:
			if self._image:
				self._imageSelect.parent = 0
				self._imageActive.parent = self
				self._image.parent = 0
				self._currentImage = self._imageActive

			if self._text:
				self._textSelect.parent = 0
				self._textActive.parent = self
				self._text.parent = 0
				self._currentText = self._textActive
		else:
			if self._image:
				self._imageSelect.parent = 0
				self._imageActive.parent = 0
				self._image.parent = self
				self._currentImage = self._image

			if self._text:
				self._textSelect.parent = 0
				self._textActive.parent = 0
				self._text.parent = self
				self._currentText = self._text

	def drawWidget(self, draw=True):
		if self._text:
			self._text.isDrawing = draw
			self._textSelect.isDrawing = draw
		if self._image:
			self._image.isDrawing = draw
			self._imageSelect.isDrawing = draw
		Widget.drawWidget(self, draw)

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)

		if self.hasImage:
			self._image.setPos(self.getPos(False), False)
			self._imageSelect.setPos(self.getPos(False), False)
		if self.hasLabel:
			self._text.setPos(self.getPos(False) + self.size/2)
			self._textSelect.setPos(self.getPos(False) + self.size/2)

	def setSize(self, size):
		Widget.setSize(self, size)
		if self.hasImage:
			self._image.size = self.size
			self._imageSelect.size = self.size

		if self.hasLabel and not self.useCharacterSize:
			self._text.setTextWidthSize(self.size.x)
			self._textSelect.setTextWidthSize(self.size.x)

			if self.size.y > 0 and \
					self._text.size.y > self.size.y :
				self._text.setTextHeightSize(self.size.y)
				self._textSelect.setTextHeightSize(self.virtyalSize.y)
		self.centerLabel()

	def _setImage(self, image):
		"""image is a Image type"""

		self._image = image
		self._imageSelect = image
		self._imageSelect.lighten()

		if image:
			self._image.canFocus = self._imageSelect.canFocus = False
			self._image.isStaticToView = \
					self._imageSelect.isStaticToView = False

		self.rect = self.virtualRect
	def _setText(self, text):
		"""text is Label type"""

		self._text = text.getCopyWidget()
		self._textSelect = text.getCopyWidget()
		self._textSelect.lighten()
		if text:
			self._text.canFocus = self._textSelect.canFocus = False
			self._text.isStaticToView = \
					self._textSelect.isStaticToView = False

		self.rect = self.virtualRect
		self.updateSelection()
		self.centerLabel()

	def _setUseCharacterSize(self, use=True):
		self._useCharacterSize = use
	
	def _setCharacterSize(self, size):
		if self.hasLabel:
			self._text.characterSize = size
			self._textSelect.characterSize = size
		self.useCharacterSize = True

	image = property(lambda self:self._currentImage, _setImage)
	text = property(lambda self:self._currentText, _setText)
	basicText = property(lambda self:self._text)
	basicImage = property(lambda self:self._image)
	textSelect = property(lambda self:self._textSelect)
	imageSelect= property(lambda self:self._imageSelect)
	hasLabel = property(lambda self:bool(self._text))
	hasImage = property(lambda self:bool(self._image))
	characterSize =property(lambda self:self._text.characterSize,\
			_setCharacterSize)
	useCharacterSize = property(lambda self:self._useCharacterSize,\
			_setUseCharacterSize)

