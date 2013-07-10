import sfml as sf
from Widget import Widget
from Active import Active
import decorator

class CheckCircle(Widget, Active):
	def __init__(self, parent, radius=10, position = sf.Vector2(0,0), \
			bigCircleColor=sf.Color.WHITE, \
			smallCircleColor=sf.Color.RED, smallCircleProportion = 0.5,\
			origin = "radius"):
		Widget.__init__(self, parent, \
				sf.Rectangle(position, sf.Vector2(radius, radius)))
		Active.__init__(self) 
		self._bigCircle  = sf.CircleShape(radius)
		self._smallCircle = sf.CircleShape(smallCircleProportion * radius)
		self._bigCircle.fill_color = bigCircleColor
		self._smallCircle.fill_color = smallCircleColor
		self._proportion = smallCircleProportion
		if origin == "radius":
			origin = sf.Vector2(radius, radius)
		self._origin = origin
		self.size = sf.Vector2(radius, radius)/0.5
		self.pos = position
	
	@decorator.forUpdate
	def update(self, render=None):
		Widget.update(self, render)
		Active.update(self)

	@decorator.forDrawing
	def draw(self, render=None):
		if render:
			render.draw(self._bigCircle)
			if self.isActive:
				render.draw(self._smallCircle)

	def setPos(self, pos, withOrigin = True):
		Widget.setPos(self, pos, withOrigin)
		self._bigCircle.position = self.virtualPos - self.outlineBigCircleThickness
		self._smallCircle.position = self.virtualPos + \
				(self._bigCircle.radius + 2*self.outlineBigCircleThickness -\
				self._smallCircle.radius) + self.outlineSmallCircleThickness

	def setSize(self, size):
		radius = min(size.x, size.y)
		self.radius = radius/2
		Widget.setSize(self, size)
		self._bigCircle.scale(size/radius)
		self._smallCircle.scale(size/radius)

	def howActive(self):
		return self.isSelect and self.event and \
				(self.event.getOneMouseClicked(self.howActiveMouse) or\
				self.event.getOnePressedKeys(self.howActiveKeyboard))

	def howSelect(self):
		return Widget.widgetFocus is self

	def activeIt(self):
		self._active = not self._active

	def disactiveIt(self):
		return

	def _setProportion(self, proportion):
		self._proportion = proportion
		self.rect = self.virtualRect

	def _setRadius(self, radius):
		self._bigCircle.radius = radius - 2*self.outlineBigCircleThickness
		self._smallCircle.radius = radius * self._proportion - 2* self.outlineSmallCircleThickness
		Widget.setSize(self, sf.Vector2(radius, radius)/0.5)
		self.pos = self.virtualPos

	def _setFillBigCircleColor(self, color):
		self._bigCircle.fill_color = color

	def _setFillSmallCircleColor(self, color):
		self._smallCircle.fill_color = color

	def _setOutlineBigCircleColor(self, color):
		self._bigCircle.outline_color = color

	def _setOutlineSmallCircleColor(self, color):
		self._smallCircle.outline_color = color

	def _setOutlineBigCircleThickness(self, thickness):
		self._bigCircle.outline_thickness = thickness
		self.rect = self.virtualRect

	def _setOutlineSmallCircleThickness(self, thickness):
		self._smallCircle.outline_thickness = thickness
		self.rect = self.virtualRect

	radius = property(lambda self:self._bigCircle.radius, _setRadius)
	proportion = property(lambda self:self._proportion, _setProportion)
	fillBigCircleColor = property(lambda self:self._bigCircle.fill_color,\
			_setFillBigCircleColor)
	fillSmallCircleColor = property(lambda self:self._smallCircle.fill_color,\
			_setFillSmallCircleColor)

	outlineSmallCircleColor = property(lambda self:self._smallCircle.outline_color,\
			_setOutlineSmallCircleColor)
	outlineBigCircleColor = property(lambda self:self._bigCircle.outline_color,\
			_setFillBigCircleColor)

	outlineBigCircleThickness = property(lambda self:self._bigCircle.outline_thickness,\
			_setFillBigCircleColor)
	outlineSmallCircleThickness = property(lambda self:self._smallCircle.outline_thickness,\
			_setOutlineSmallCircleThickness)
