import sfml as sf
from Widget import Widget
from Active import Active
from functions import isInEllipse
from Widget import Position
import decorator

class CheckCircle(Widget, Active):
	def __init__(self, parent=None, radius=10, position = sf.Vector2(0,0), \
			bigCircleColor=sf.Color.WHITE, \
			smallCircleColor=sf.Color.RED, smallCircleProportion = 0.5,\
			origin = Position.Center):
		Widget.__init__(self, parent, \
				sf.Rectangle(position, sf.Vector2(radius, radius)/0.5))
		Active.__init__(self) 
		self._bigCircle  = sf.CircleShape(radius)
		self._smallCircle = sf.CircleShape(smallCircleProportion * radius)
		self._bigCircle.fill_color = bigCircleColor
		self._smallCircle.fill_color = smallCircleColor
		self._proportion = smallCircleProportion
		self.size = sf.Vector2(radius, radius)/0.5
		self.pos = position
		self.posOrigin = origin
	

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

	def howFocus(self):
		if self._event:
			return isInEllipse(self._event.mousePos, self.getPosOnScreen(False) + self.sizeOnScreen / 2, self.sizeOnScreen/2)

	def setPos(self, pos, withOrigin = True):
		Widget.setPos(self, pos, withOrigin)
		self._bigCircle.position = self.getPos(False) - self.outlineBigCircleThickness
		self._smallCircle.position = self.getPos(False) + \
				(self._bigCircle.global_bounds.size / 2 + 2*self.outlineBigCircleThickness -\
				self._smallCircle.global_bounds.size / 2) + self.outlineSmallCircleThickness

	def setSize(self, size):
		radius = min(size.x, size.y)
		self.radius = radius/2
		Widget.setSize(self, size)
		print(size, "size")
		if radius != 0:
			self._bigCircle.ratio = (size/sf.Vector2(radius, radius))
			self._smallCircle.ratio = (size/sf.Vector2(radius, radius))

	def howActive(self):
		return self.isSelect and self.event and (\
				self.event.getOneMouseClicked(self.howActiveMouse) or\
				self.event.getOnePressedKeys(self.howActiveKeyboard))

	def howSelect(self):
		return Widget.widgetFocus is self

	def activeIt(self):
		self._active = not self._active

	def disactiveIt(self):
		return

	def _setProportion(self, proportion):
		self._proportion = proportion
		self.rect = self.rect

	def _setRadius(self, radius):
		self._bigCircle.radius = radius - 2*self.outlineBigCircleThickness
		self._smallCircle.radius = radius * self._proportion - 2* self.outlineSmallCircleThickness
		Widget.setSize(self, sf.Vector2(radius, radius)/0.5)
		self.pos = self.pos

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
		self.rect = self.rect

	def _setOutlineSmallCircleThickness(self, thickness):
		self._smallCircle.outline_thickness = thickness
		self.rect = self.rect

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
