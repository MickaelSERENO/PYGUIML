from Widget import Widget
import sfml as sf
import decorator
from Active import Active

class CheckBox(Widget, Active):
	def __init__(self, parent=None, rect=sf.Rectangle(sf.Vector2(0,0), sf.Vector2(30,30))):
		Widget.__init__(self, parent, rect)
		Active.__init__(self)
		self._rectangle = sf.RectangleShape(rect.size)
		self._line = [sf.VertexArray(sf.PrimitiveType.LINES, 2),\
				sf.VertexArray(sf.PrimitiveType.LINES, 2)]

		self.outlineRectangleColor = sf.Color.WHITE
		self.outlineRectangleThickness = 2
		self.crossColor = sf.Color.BLACK
		self.rect = rect

	@decorator.forUpdate
	def update(self, render=None):
		Active.update(self)
		Widget.update(self,render)

	@decorator.forDrawing
	def draw(self, render=None):
		if render:
			render.draw(self._rectangle)
			if self.isActive:
				render.draw(self._line[0])
				render.draw(self._line[1])

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)
		self._rectangle.position = self.getPos(False) + \
				sf.Vector2(self.outlineRectangleThickness,\
				self.outlineRectangleThickness)

		self._line[0][0].position = self.getPos(False) + \
				sf.Vector2(self.outlineRectangleThickness,\
				self.outlineRectangleThickness)

		self._line[0][1].position = self.getPos(False) + self.size - \
				sf.Vector2(self.outlineRectangleThickness,\
				self.outlineRectangleThickness)

		self._line[1][0].position = self.getPos(False) +\
				sf.Vector2(0, self.size.y) +  \
				sf.Vector2(self.outlineRectangleThickness,\
				-self.outlineRectangleThickness)

		self._line[1][1].position = self.getPos(False) + \
				sf.Vector2(self.size.x, 0) + \
				sf.Vector2(-self.outlineRectangleThickness,\
				self.outlineRectangleThickness)
				
	def setSize(self, size):
		Widget.setSize(self, size)
		self._rectangle.size = size -\
				sf.Vector2(2*self.outlineRectangleThickness,\
				2*self.outlineRectangleThickness)
		self.pos = self.pos

	def howSelect(self):
		return Widget.widgetFocus is self

	def howActive(self):
		return self.isSelect and self.event and \
				(self.event.getOneMouseClicked(self.howActiveMouse) or\
				self.event.getOnePressedKeys(self.howActiveKeyboard))

	def activeIt(self):
		self._active = not self._active

	def disactiveIt(self):
		return

	def _setCrossColor(self, color):
		for line in self._line:
			for dote in line:
				dote.color = color

	def _setOutlineRectangleColor(self, color):
		self._rectangle.outline_color = color

	def _setFillRectangleColor(self, color):
		self._rectangle.fill_color = color

	def _setOutlineRectangleThickness(self, size):
		self._rectangle.outline_thickness = size
		self.size = self.size

	outlineRectangleColor=property(lambda self:self._rectangle.outline_color,\
				lambda self, color:self._setOutlineRectangleColor(color))
	outlineRectangleThickness =\
			property(lambda self:self._rectangle.outline_thickness,\
				lambda self, size:self._setOutlineRectangleThickness(size))
	fillRectangleColor = property(lambda self:self._rectangle.fill_color,\
			lambda self, color:self._setFillRectangleColor(color))

	crossColor = property(lambda self:self._line[0].color,\
			lambda self, color:self._setCrossColor(color))
