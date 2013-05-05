from Widget import Widget
import sfml as sf
import decorator
from Active import Active

class CheckBox(Widget, Active):
	def __init__(self, parent, rect):
		Active.__init__(self)
		Widget.__init__(self)
		self._rectangle = sf.RectangleShape(rect.size)
		self._line = [sf.VertexArray(sf.PrimitiveType.LINES, 2),\
				sf.VertexArray(sf.PrimitiveType.LINES, 2)]
		self.howActiveKeyboard = sf.Keyboard.SPACE
		self.howActiveMouse = sf.Mouse.LEFT

		self.outlineColorRectangle = sf::Color::WWHITE
		self.outlineThickness = 2
		self.crossColor = sf::Color::BLACK
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

	def _setSize(self, size):
