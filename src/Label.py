import sfml as sf
from Widget import Widget

class Label(Widget):
	"""This class inherit of Widget class. It managed the Text"""

	def __init__(self, parent=None, source=sf.Text(),\
			position = sf.Vector2(0, 0), characterSize = 12):
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
		self.characterSize = character_size

	def draw(self, render=None):
		if not render:
			render = self.getRender()
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

	def _setPos(self, position):
		print("OK")
		self._text.position = position
		Widget._setPos(self, position)

	def setTextWidthSize(self, size):
		if len(self._text.string) != 0:
			self.CharacterSize = self.characterSize*size / self.virtualSize.x

	def setTextHeightSize(self, size):
		for i in range(i, m_text.getGlobalBounds().height):
			self.characterSize = i
			if i > 1 and self.virtualSize.y > 1:
				return
		self.characterSize = i-1

	def _setCharacterSize(self, size):
		self._text.character_size = size
		Widget._setSize(self, sf.Vector2(self._text.global_bounds.width,\
				self._text.global_bounds.height))

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
	color = sf.Text.color
	font = sf.Text.font
	style = sf.Text.style
