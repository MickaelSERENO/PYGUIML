from Widget import *
from Active import *
from Button import Button
from Label import Label
from Image import Image

import sfml as sf

class Slide(Widget, Active):
	def __init__(self, parent=None, rect=sf.Rectangle(), select=False, active=False, \
			alwaysUpdateSelection=True, alwaysUpdateActivation=True, \
			permanentSelection=False, permanentActivation=False, step=1, \
			values=sf.Vector2(0, 100), startValue=0, orientation=Direction.Horizontal, inStep=1):
		Widget.__init__(self, parent, rect)
		Active.__init__(self, select, active, alwaysUpdateSelection, alwaysUpdateActivation, \
				permanentSelection, permanentActivation)
		if orientation == Direction.Horizontal:
			self._howActiveKeyboard = [sf.Keyboard.LEFT, sf.Keyboard.RIGHT]
		else:
			self._howActiveKeyboard = [sf.Keyboard.UP, sf.Keyboard.DOWN]

		self._currentValue = None
		self._limitValue=values
		self._step = step
		self._inStep = inStep

		self._background = None
		self._forground = None
		if orientation == Direction.Horizontal:
			self._background = Button(self, image=Image(None, \
					sf.Image.create(rect.width, rect.height, sf.Color.WHITE)))
			self._forground = Button(self, image=Image(None, \
					sf.Image.create(rect.width*inStep*step/(values.y - values.x), rect.height, sf.Color.CYAN)))
		else:
			self._background = Button(self, image=Image(None, \
					sf.Image.create(rect.width, rect.height, sf.Color.WHITE)))
			self._forground = Button(self, image=Image(None, \
					sf.Image.create(rect.width, rect.height*inStep*step/(values.y - values.x), sf.Color.CYAN)))

		self._isMoving=False
		self._mousePosMoving = sf.Vector2(0, 0)
		self._oldCurrentValue = 0

		self._forground.posOrigin = Position.Center
		self._mousePos = sf.Vector2()
		self._orientation = orientation
		self.currentValue = startValue
		if orientation == Direction.Vertical:
			self.size = self.size

	def update(self, render=None):
		Widget.update(self, render)
		Active.update(self)

	def setPos(self, pos, withOrigin=True):
		Widget.setPos(self, pos, withOrigin)
		self._updateSlidePosition()

	def setSize(self, pos, resetOrigin=True):
		if self._orientation == Direction.Horizontal:
			self._background.size = self.size
			self._forground.size = sf.Vector2(self.size.x*self._inStep*self.step/\
					(self._limitValue.y - self._limitValue.x), self.size.y)
		else:
			self._background.size = self.size
			self._forground.size = sf.Vector2(self.size.x, self.step * self._inStep/\
					(self._limitValue.y - self._limitValue.x)*self.size.y)
		self._updateSlidePosition()

	def howFocus(self):
		return False

	def howSelect(self):
		return self._background.isSelect or self._forground.isSelect or self._isMoving

	def howActive(self):
		return self.isSelect or self._forground.isActive

	def activeIt(self, force=False):
		done = False
	
		if self._getIsMoving():
			if self.orientation == Direction.Horizontal:
				self._currentValue = self._oldCurrentValue +\
						self._limitValue.y*\
						(self.event.mousePos.x - self.getPosOnScreen(False).x - \
						self._mousePosMoving.x)/(self.sizeOnScreen.x-self._forground.size.x)
			else:
				self._currentValue = self._oldCurrentValue + self._limitValue.y*\
						(self.event.mousePos.y - self.getPosOnScreen(False).y - \
						self._mousePosMoving.y)/(self.sizeOnScreen.y-self._forground.size.y)
			done = True

		elif self._background.isActive:
			done = True
			print("ok")
			if self._orientation == Direction.Horizontal:
				self._currentValue = self._limitValue.y *\
						(self.event.mousePos.x - self._forground.size.x/2 - self.getPosOnScreen(False).x)/\
						(self.sizeOnScreen.x-self._forground.size.x)

			else:
				self._currentValue = self._limitValue.y *\
						(self.event.mousePos.y - self.getPosOnScreen(False).y-self._forground.size.y/2)/\
						(self.sizeOnScreen.y-self._forground.size.y)

		elif self.isSelect and self.event:
			if self.event.getOnePressedKeys(self.howActiveKeyboard[0]):
				self._currentValue -= self.step
				done = True
			elif self.event.getOnePressedKeys(self.howActiveKeyboard[1]):
				self._currentValue += self.step
				done = True

		if done:
			self._updateSlidePosition()
		Active.activeIt(self, force)

	def _setOrientation(self, orientation):
		self._orientation = orientation
		self.size = self.size
		self._updateSlidePosition()

	def _setCurrentValue(self, value):
		self._currentValue = value
		self._updateSlidePosition()

	def _setStep(self, step):
		self._step = step
		self.size = self.size

	def _setInStep(self, inStep):
		self._inStep = inStep
		self.size = self.size
		self._updateSlidePosition()

	def _setBackgroundButton(self, button):
		self._background.parent =0
		self._background=button
		self._background.setParent(self, 0)
		self.size = self.size

	def _setForgroundButton(self, button):
		self._background.parent =0
		self._background=button
		self._background.setParent(self, 0)
		self.size = self.size

	def _updateSlidePosition(self):
		if self._currentValue < self._limitValue.x:
			self._currentValue = self._limitValue.x

		elif self._currentValue > self._limitValue.y:
			self._currentValue = self._limitValue.y

		self._background.setPos(self.getPos(False), False)
		if self._orientation == Direction.Horizontal:
			self._forground.pos = sf.Vector2(self.getPos(False).x + self._forground.size.x/2 +\
					(self.size.x-self._forground.size.x)/\
					(self._limitValue.y - self._limitValue.x)*\
					(self._currentValue - self._limitValue.x), self.getPos(False).y + self.size.y/2)
		else:
			self._forground.pos = sf.Vector2(self.getPos(False).x + self.size.x/2,\
					self.getPos(False).y + self._forground.size.y/2 +\
					(self.size.y-self._forground.size.y)/\
					(self._limitValue.y - self._limitValue.x)*\
					(self._currentValue - self._limitValue.x))
		if not self._isMoving:
			self._oldCurrentValue = self.currentValue

	def _getIsMoving(self):
		if not self._isMoving and self._event:
			self._isMoving = self._forground.isActive
			if self._isMoving:
				self._mousePosMoving = self._event.mousePos
				self._oldCurrentValue = self._currentValue

		elif not (self._event and (self._event.getPressedKeys(self._forground.howActiveKeyboard[0]) or \
				self._event.getMouseClicked(self._forground.howActiveMouse[0]))):
			self._isMoving = False

		return self._isMoving

	currentValue = property(lambda self:self._currentValue, _setCurrentValue)
	step = property(lambda self:self._step, _setStep)
	orientation = property(lambda self:self._orientation, _setOrientation)
	slideMoving = property(lambda self:self._isMoving)
	inStep = property(lambda self:self._inStep, _setInStep)
	forgroundButton = property(lambda self:self._forground, _setForgroundButton)
	backgroundButton = property(lambda self:self._forground, _setBackgroundButton)
