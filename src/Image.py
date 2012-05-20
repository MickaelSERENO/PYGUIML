from Widget import Widget
import sfml as sf

class Image(Widget):
	"""This class create an Image
	Cette classe créé une image"""
	def __init__(self, parent=0, source=sf.Sprite(), rect=sf.FloatRect(0,0,0,0)):
		"""source can be a sf.Texture, a bytes string or a sf.Sprite() type"""
		Widget.__init__(self, parent, rect)
		self._texture = sf.Texture

		if isinstance(source, bytes):
			self._texture = sf.Texture.load_from_file(source)

		elif isinstance(source, sf.Image):
			self._texture = sf.Texture.load_from_image(source)

		elif isinstance(source, sf.Texture):
			self._texture = sf.Texture(source)

		elif isinstance(source, sf.Sprite):
			self._texture = source.texture

		else:
			raise TypeError("source is not sf.Image type or sf.Texture type or sf.Sprite type or bytes type")

		self._sprite = sf.Sprite(self._texture)

		# if rect == sf.FloatRect(0,0,0,0):
		if rect.width == 0 and rect.height == 0:
			self.rect = self._sprite.global_bounds
		else:
			self.rect = rect

	def setSource(self, source):
		"""This Methode set the object's sprite with a texture, a sprite, a image or a bytes string type"""
		if isinstance(source, bytes):
			self._texture = sf.Texture.load_from_file(source)

		elif isinstance(source, sf.Texture):
			self._texture = sf.Texture(source)

		elif isinstance(source, sf.Image):
			self._texture = sf.Texture.load_from_image(source)

		elif isinstance(source, sf.Sprite):
			self._texture = source.texture

		self._sprite = sf.Sprite(self._texture)
		self.rect = self.rect

	def update(self, drawable):
		"""This methode update the object : it can add drawable in the drawable list"""
		if self._isDrawing:
			drawable.append(self._sprite)
		Widget.update(self, drawable)

	def _setPos(self, position):
		Widget._setPos(self, position)
		self._sprite.position = position

	def _setDimensions(self, size):
		if self._sprite.texture:
				self._sprite.scale = sf.Vector2f(size.x / self.sprite.local_bounds.width, size.y / self.sprite.local_bounds.height)

		Widget._setDimensions(self, size)

	def setTextureRect(self, rect):
		self.sprite.texture_rect(rect)

	def setRotation(self, angle):
		self.sprite.rotate(angle)

	def setOrigin(self, origin):
		self._sprite.origin = origin

	def setOriginMiddle(self):
		self.setOrigin(self.size.x/2, self.size.y/2)

	def setOriginRight(self):
		self.setOrigin(self.size.x, 0)

	def setColor(self, color):
		self._sprite.color = color

	def setColorPixel(self, pos, color):
		"""This methode change the pixel color in the position pos. Pos is a Vector2f type"""

		image = self._texture.copy_to_image()
		image.set_pixel(x, y, color)
		self.sprite = image

	def setPlageColor(self, rect, color):
		"""This methode set a pixels plage and set there color"""
		try:
			if rect.left + rect.width > self.dimensions.x or rect.top + rect.height > self.dimensions.y:
				raise ValueError("FATAL ERROR : The Plage color don't can be in the sprite")
		except ValueError:
			print("FATAL ERROR : The Plage color don't can be in the sprite")
		
		i = 0
		j = 0
		while i > rect.width:
			while j > rect.height:
				self.setColorPixel(rect.left + i, rect.top + j, color)
				j += 1
			i += 1

	def lighten(self, rect = sf.FloatRect(0, 0, 0, 0)):
		"""This methode lighten the image"""
		rect2 = rect
		rect3 = self.rect
		if rect == sf.FloatRect(0, 0, 0, 0):
			rect2 = rect3
	
		#Test if the rect is a correct value
		try:
			if rect2.left + rect2.width > self.dimensions.x or rect2.top + rect2.height > self.dimensions.y:
				raise ValueError("FATAL ERROR : The Plage color don't can be in the sprite")
		except ValueError:
			print("FATAL ERROR : The Plage color don't can be in the sprite")

		image = self._texture.copy_to_image()
		i = rect2.left
		j = rect2.top
		while i < (rect2.left + rect2.width):
			while j < (rect2.top + rect2.height):
				pixel = image.get_pixel(i, j)
				c = float(pixel.r)/255
				pixel.r = 255*(3*c*c-2*c*c*c)
				c = float(pixel.g)/255
				pixel.g = 255*(3*c*c-2*c*c*c)
				c = float(pixel.b)/255
				pixel.b = 255*(3*c*c-2*c*c*c)
				image.set_pixel(i, j, pixel)
				j += 1
			i += 1
		self.sprite = image;

	def _getSprite(self):
		return self._sprite

	def _getTexture(self):
		return self._texture

	sprite = property(_getSprite, setSource)
	texture = property(_getTexture)
	pos = property(Widget._getPos, _setPos)
	dimensions = property(Widget._getDimensions, _setDimensions)
