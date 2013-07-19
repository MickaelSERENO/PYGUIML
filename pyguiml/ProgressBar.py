from Widget import *
from Image import Image
import sfml as sf

class ProgressBar(Widget):
	def __init__(self, parent=None, rect=sf.Rectangle(), \
			widgetBackground=None, widgetForground=None, \
			start=0, orientation = Direction.Horizontal):
		Widget.__init__(self, parent, rect)
		self._currentValue = start
		self._widgetBackground = widgetBackground
		if self._widgetBackground:
			self._widgetBackground.setParent(self)
		self._widgetForground = widgetForground
		if self._widgetForground:
			self._widgetForground.setParent(self)
		else:
			self._widgetForground = Image(self, sf.Image.create(20, 20, sf.Color.GREEN))

		self._orientation = orientation
		self.rect = self.rect

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)
		if self._widgetBackground:
			self._widgetBackground.setPos(self.getPos(False), False)
		if self._widgetForground:
			self._widgetForground.setPos(self.getPos(False), False)

	def setSize(self, size, resetOrigin=True):
		Widget.setSize(self, size, resetOrigin)
		if self._widgetBackground:
			self._widgetBackground.setSize(self.getSize(False), False)
		if self._widgetForground:
			self._widgetForground.setSize(self.getSize(False), False)
		self._setCurrentValue(self.currentValue)

	def _setCurrentValue(self, value):
		"""Value is in 0 and 1"""
		if value > 1:
			value = 1
		elif value < 0:
			value = 0

		self._currentValue=value
		if self.orientation == Direction.Horizontal and self._widgetForground:
			self._widgetForground.clipRect = sf.Rectangle(sf.Vector2(), \
					sf.Vector2(value*self.size.x, self.size.y))
		elif self.orientation == Direction.Vertical and self._widgetForground:
			self._widgetForground.clipRect = sf.Rectangle(sf.Vector2(), \
					sf.Vector2(self.size.x, value*self.size.y))

	def _setBackgroundWidget(self, widget):
		if self._widgetBackground:
			self._widgetBackground.parent = 0
		self._widgetBackground = widget
		if self._widgetBackground:
			self._widgetForground.setParent(self, 0)
		self.rect = self.rect

	def _setForgroundWidget(self, widget):
		if self._widgetForground:
			self._widgetForground.parent = 0
		self._widgetForground = widget
		if self._widgetForground:
			self._widgetForground.setParent(self, 1)
		self.rect = self.rect

	def _setOrientation(self, orientation):
		self._orientation = orientation
		self.currentValue = self.currentValue

	currentValue = property(lambda self:self._currentValue, _setCurrentValue)
	forgroundWidget = property(lambda self:self._widgetForground, \
			_setForgroundWidget)
	backgroundWidget = property(lambda self:self._widgetBackground, \
			_setBackgroundWidget)
	orientation = property(lambda self:self._orientation, \
			_setOrientation)
