import sfml as sf
from Widget import Widget
import decorator

class Label(Widget):
	"""This class inherit of Widget class. It managed the Text"""

	def __init__(self, parent=None, source=sf.Text(),\
			position = sf.Vector2(0, 0), characterSize = 12, font=None, \
			style=sf.Text.REGULAR):
		"""parent is a widget objet, source a str objet or a sf.Text objet,
		position is a sf.Vector2 objet and characterSize is a int objet"""

		if isinstance(source, str):
			Widget.__init__(self, parent, sf.Rectangle(position, sf.Vector2(\
					characterSize * len(source), characterSize)))
			self._text = sf.Text(source, character_size = characterSize)

		elif isinstance(source, sf.Text):
			Widget.__init__(self, parent, sf.Rectangle(position, sf.Vector2(\
					characterSize * len(source.string), characterSize)))
			self._text = source
			self.characterSize = characterSize

		else:
			raise TypeError("Source is not a str objet or a sf.Text object")

		self.canFocus = False
		self.characterSize = characterSize
		if font:
			self.font = font
		self.rect = self.rect

	@decorator.forDrawing
	def draw(self, render=None):
		if render:
			render.draw(self._text)

	def lighten(self):
		"""Lighten the Text"""

		pixel = self._text.color

		c = float(pixel.r)/255
		pixel.r = 255*(3*c*c-2*c*c*c)
		c = float(pixel.g)/255
		pixel.g = 255*(3*c*c-2*c*c*c)
		c = float(pixel.b)/255
		pixel.b = 255*(3*c*c-2*c*c*c)
		
		self._text.color = pixel

	def rotate(self, angle):
		self._text.rotate(angle)

	def setPos(self, position, withOrigin = True):
		Widget.setPos(self, position, withOrigin)
		self._text.position = self.getPos(False)

	def _setFont(self, font):
		self._text.font = font
		self.size = self.size

	def _setStyle(self, style):
		self._text.style = style
		self.size = self.size

	def _setColor(self, color):
		self._text.color = color

	def setTextWidthSize(self, size):
		if len(self._text.string) != 0 and self.size.x != 0:
			self.characterSize = self.characterSize*size / self.size.x

	def setTextHeightSize(self, size):
		if len(self._text.string) != 0 and self.size.y != 0:
			self.characterSize = self.characterSize*size / self.size.y

	def _setCharacterSize(self, size):
		self._text.character_size = size
		self.size = sf.Vector2(self._text.global_bounds.width,\
				self._text.global_bounds.height)

	def _setSize(self, size):
		self._text.scale = sf.Vector2(size.x/self._text.local_bounds.width,\
				size.y/self._text.local_bounds.height)
		Widget._setSize(self, sf.Vector2(self._text.local_bounds.width,\
				self._text.local_bounds.height))

	def _setSource(self, source):
		if isinstance(source, str):
			self._text = sf.Text(source, character_size = self._text.character_size)
		elif isinstance(source, sf.Text):
			self._text = source

	text = property(lambda self:self._text, _setSource)
	characterSize = property(lambda self:self._text.character_size,\
			_setCharacterSize)
	color = property(lambda self:self._text.color, _setColor)
	font = property(lambda self:self._text.font, _setFont)
	style = property(lambda self:self._style, _setStyle)
