from Widget import Widget
from functions import circle
import math
import sfml as sf

class Image(Widget):
	"""This class create an Image
	Cette classe créé une image"""

	textures = dict()

	def __init__(self, parent=0, source=sf.Sprite(), delTextureCreated=True,\
			rect= sf.FloatRect(0,0,0,0)):
		"""source can be a sf.Texture, a bytes string or a sf.Sprite() type"""
		Widget.__init__(self, parent, rect)
		self.focus = False
		self._sizeRoundEdge = 0
		self.delTextureCreated = delTextureCreated
		self._textureCreated = dict()

		self.setSource(source)

		if rect.width == 0 and rect.height == 0:
			self.rect = self._sprite.global_bounds
		else:
			self.rect = rect

	def __del__(self):
		if self.delTextureCreated:
			for keyi in self._textureCreated.keys():
				del Image.textures[key]

	def draw(self,render=None):
		if not render:
			render = self.getRender()
		if render:
			render.draw(self._sprite)

	def roundEdge(self,size):
		if self._sprite.texture:
			image = sprite.texture.copy_to_image()
			for i in range(int(size)):
				topLeft = circle(i,size,size,size)
				bottomLeft = circle(i, size,\
						self._sprite.texture.size.y - size, size)

				topRight = circle(i + self._sprite.texture.size.x - size,\
						self._sprite.texture.size.x - size, size, size)
				bottomRight = circle(i + self._sprite.texture.size.x - size,\
						self._sprite.texture.size.x - size,\
						self._sprite.texture.size.y - size, size)

				for j in range(int(topLeft.y)):
					pixel = image.get_pixel(sf.Vector2f(i,j))
					pixel.a = 255 * (1 - \
							max(min((math.sqrt((i-size)**2 +\
							(j-size)**2)-size+1)/2, 1), 0))
					image.set_pixel(i, j, pixel)

				for j in range(int(self._sprite.texture.size.y-1),\
						int(bottomLeft.y), -1):
					pixel = image.get_pixel(sf.Vector2f(i,j))
					pixel.a = 255 * (1 - \
							max(min((math.sqrt((i-size)**2 +\
							(j-size-self._sprite.texture.size.y)**2)-\
							size+1)/2,1), 0))
					image.set_pixel(i, j, pixel)

				for j in range(int(topRight.y)):
					pixel = image.get_pixel(sf.Vector2f(i,j))
					pixel.a = 255 * (1 - \
							max(min((math.sqrt(\
							(i-size-self._sprite.texture.size.x)**2 +\
							(j-size)**2)-size+1)/2, 1), 0))
					image.set_pixel(i, j, pixel)

				for j in range(int(self._sprite.texture.size.y-1),\
						int(bottomRight.y), -1):
					pixel = image.get_pixel(sf.Vector2f(i,j))
					pixel.a = 255 * (1 - \
							max(min((math.sqrt(\
							(i-size-self._sprite.texture.size.x)**2 +\
							(j-size-self._sprite.texture.size.y)**2)-\
							size+1)/2,1), 0))
					image.set_pixel(i, j, pixel)

				self.setSource(image)
				self._sizeRoundEdge = size

		else:
			render = sf.RenderTexture
			render.size = sf.Vector2f(m_virtualSize.x, m_virtualSize.y)
			render.draw(m_sprite)
			render.display()
			self.setSource(render.texture)
			roundEdge(size)

	def setSource(self, source):
		"""This Methode set the object's sprite with a texture,
		a sprite, a image or a bytes string type"""

		texture = sf.Texture()
		keyTexture = str()
		keyTexture = "texture"+str(len(Image.textures))

		if isinstance(source, bytes):
			if source in Widget.filesLoading:
				texture = Widget.filesLoading(source)
			else:
				texture = sf.Texture.load_from_file(source)
				Widget.filesLoading[source] = texture

		elif isinstance(source, sf.Image):
			texture = sf.Texture.load_from_image(source)
			self._textureCreated[keyTexture]=texture

		elif isinstance(source, sf.Texture):
			texture = sf.Texture(source)
			self._textureCreated[keyTexture]=texture

		elif isinstance(source, sf.Sprite):
			texture = source.texture
			self._textureCreated[keyTexture]=texture

		else:
			raise TypeError("source is not sf.Image type or\
					sf.Texture type or sf.Sprite type or bytes type")

		if not isinstance(source,bytes):
			Image.textures[keyTexture]=texture

		self._sprite = sf.Sprite(texture)
		self.rect = self.rect

	def setPos(self, position, withOrigin):
		Widget.setPos(self, position, withOrigin)
		self._sprite.position = self.virtualPos

	def setDimensions(self, size):
		Widget.setDimensions(self, size)
		if self._sprite.texture:
				self._sprite.scale = sf.Vector2f(self.virtualDimensions.x /\
						self.sprite.local_bounds.width,\
						self.virtualDimensions.y /\
						self.sprite.local_bounds.height)

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
		"""This methode change the pixel color in the position pos.
		Pos is a Vector2f type"""

		image = self._texture.copy_to_image()
		image.set_pixel(x, y, color)
		self.sprite = image

	def setPlageColor(self, rect, color):
		"""This methode set a pixels plage and set there color"""
		try:
			if rect.left + rect.width > self.dimensions.x or\
					rect.top + rect.height > self.dimensions.y:
				raise ValueError("ERROR : \
						The Plage color don't can be in the sprite")
		except ValueError:
			print("ERROR : The Plage color don't can be in the sprite")
		
		else:
			image = self._texture.copy_to_image()
			for i in range(rect.left, rect.left + rect.width):
				for j in range(rect.top, rect.top + rect.height):
					image.set_pixel(i, j, color)
			sel.setSource(image)

	def lighten(self, rect = sf.FloatRect(0, 0, 0, 0)):
		"""This methode lighten the image"""
		rect2 = rect
		if rect == sf.FloatRect(0, 0, 0, 0):
			rect2 = self.rect
	
		#Test if the rect is a correct value
		try:
			if rect2.left + rect2.width > self.dimensions.x or\
					rect2.top + rect2.height > self.dimensions.y:
				raise ValueError("ERROR :\
						The Plage color don't can be in the sprite")
		except ValueError:
			print("ERROR : The Plage color don't can be in the sprite")

		else:
			image = self._texture.copy_to_image()
			for i in range(rect2.left, rect2.left + rect2.width):
				for j in range(rect2.top, rect2.top + rect2.height):
					pixel = image.get_pixel(i, j)
					c = float(pixel.r)/255
					pixel.r = 255*(3*c*c-2*c*c*c)
					c = float(pixel.g)/255
					pixel.g = 255*(3*c*c-2*c*c*c)
					c = float(pixel.b)/255
					pixel.b = 255*(3*c*c-2*c*c*c)
					image.set_pixel(i, j, pixel)
			self.setSource(image)

	sprite = property(lambda self:self._sprite, setSource)
	texture = property(lambda self:self._texture, setSource)
	sizeRoundEdge = property(lambda self:self._sizeRoundEdge, roundEdge) 
	textureCreated = property(lambda self:self._textureCreated)
