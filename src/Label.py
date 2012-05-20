import sfml as sf
from Widget import Widget

class Label(Widget):
	"""This class inherit of Widget class. It managed the Text"""

	def __init__(self, parent=0, source=sf.Text(), position = sf.Vector2f(0, 0), characterSize = 12):
		"""parent is a widget objet, source a str objet or a sf.Text objet, position is a sf.Vector2f objet and characterSize is a int objet"""

		if isinstance(source, str):
			Widget.__init__(self, parent, sf.FloatRect(position.x, position.y, characterSize * len(source), characterSize))
			self._text = sf.Text(source, character_size = characterSize)
		elif isinstance(source, sf.Text):
			Widget.__init__(self, parent, sf.FloatRect(position.x, position.y, characterSize * len(source.string), characterSize))
			self._text = source
		else:
			raise TypeError("Source is not a str objet or a sf.Text object")

	def update(self, drawable):
		"""Draw self.text"""
		if self._isDrawing:
			drawable.append(self._text)
		Widget.update(self, drawable)

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

	def setOrigin(self, origin):
		"""This methode set the object's origin"""

		self._text.origin = origin

	def setOriginMiddle(self):
		"""This methode set the object's origin at the middle of him"""
		self.setOrigin(sf.Vector2f(self._text.global_bounds.left + self._dimensions.x, self._text.global_bounds.top + self._dimensions.y))

	def setDefaultOrigin(self):
		"""This methode set the origin at the default(at the Left and Top of him)"""
		self.setOrigin(sf.Vector2f(self._text.global_bounds.left, self._text.global_bounds.top))

	def rotate(self, angle):
		self._text.rotate(angle)

	def setStyle(self, style):
		self._text.style(style)

	def _setPos(self, position):
		print("OK")
		self._text.position = position
		Widget._setPos(self, position)

	def setFontText(self, font):
		self._text.font = font

	def setTextWidthSize(self, size):
		self.setCharacterSize(size / len(self._text.string));

	def setCharacterSize(self, size):
		self._text.character_size = size
		Widget._setDimensions(self, sf.Vector2f(self._text.global_bounds.width, self._text.global_bounds.height))

	def setColor(self, color):
		self._text.color = color

	def _setDimensions(self, size):
		self._text.scale = sf.Vector2f(size.x/self._text.local_bounds.width, size.y/self._text.local_bounds.height)
		Widget._setDimensions(self, sf.Vector2f(self._text.local_bounds.width, self._text.local_bounds.height))
	
	def _getText(self):
		return self._text

	def _setSource(self, source):
		if isinstance(source, str):
			self._text = sf.Text(source, character_size = self._text.character_size)
		elif isinstance(source, sf.Text):
			self._text = source

	text = property(_getText, _setSource)
	pos = property(Widget._getPos, _setPos)
	dimensions = property(Widget._getDimensions, _setDimensions)
