from Label import Label
from Widget import *
import sfml as sf
from functools import reduce
import decorator

class TextArray(Widget):
	def __init__(self, parent = None, pos=sf.Vector2(0, 0), sizeX=200,\
			space=5, label=Label(), alignment = Position.TopLeft):
		Widget.__init__(self, parent,sf.Rectangle(pos, sf.Vector2(sizeX, 0)))

		self._labelList = list()
		self._space = space
		self._label = None
		self._alignment = None

		self.setLabel(label, False)
		self.alignment = alignment

	@decorator.forUpdate
	def update(self, render=None):
		Widget.update(self, render)

	def setPos(self, pos, withOrigin=True):
		oldPos = self.pos
		Widget.setPos(self, pos, withOrigin)
		for i, label in enumerate(self._labelList):
			label.pos = reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
							self._labelList[0:i], self._pos) + \
							sf.Vector2(0, self._space * i)
	def drawWidget(self, draw=True):
		for label in seld._labelList:
			label.drawWidget(draw)
		Widget.drawWidget(self, draw)

	def setSize(self, size):
		Widget.setSize(self, size)
		if size != self.size:
			for label in self._labelList:
				label.scale = size / self.size

		self.setPos(self.getPos(False), False)

	def setLabel(self, label, resetSize=False):
		self._labelList = list()

		characterIndex = 0
		characterPos = self.pos.x

		oldCharacterIndex = characterIndex
		oldCharacterPos = characterPos
		while oldCharacterIndex < len(label.text.string):
			for i in range(oldCharacterIndex, len(label.text.string)):
				characterIndex += 1
				if label.text.find_character_pos(i).x - oldCharacterPos > self.size.x\
						or label.text.string[i] == '\n' or characterIndex > len(label.text.string):

					if i != 0 and label.text.string[i] != '\n':
						characterIndex -= 1

					characterPos = label.text.find_character_pos(characterIndex).x

					#if label.text.string[oldCharacterIndex:characterIndex] != '\n':

					self._labelList.append(Label(self, \
						label.text.string[oldCharacterIndex:characterIndex].replace('\n', ''),\
						reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
						self._labelList, self._pos) + \
						sf.Vector2(0, self._space * len(self._labelList)),\
						label.characterSize, label.font,\
						label.style))

#						self._labelList[-1].size = sf.Vector2(characterPos - oldCharacterPos, \
#								self._labelList[-1].size.y)
					oldCharacterPos = characterPos
					oldCharacterIndex = characterIndex
					break;
		if resetSize:
			self.size = self.size
		else:
			Widget.setSize(self, sf.Vector2(max([newLabel.size.x for newLabel in self._labelList]+[0]), \
				self._labelList[-1].getPos(False).y + self._labelList[-1].size.y - self._pos.y))
		self._label = label
		self.alignment = self.alignment

	def _setAlignment(self, alignment):
		self._alignment = alignment
		for label in self._labelList:
			if label:
				if alignment == Position.TopLeft or alignment==Position.BottomLeft:
					label.origin = sf.Vector2(0,0)
				elif alignment == Position.TopRight or alignment==Position.BottomRight:
					label.origin = sf.Vector2(self.size.x, 0) - \
							sf.Vector2(label.size.x, 0)
				else:
					label.origin = sf.Vector2(self.size.x - label.size.x, 0)/2

		self.setPos(self.getPos(False), False)

	def setCanUpdate(self, update):
		for label in self._labelList:
			label.canUpdate = update
		Updatable.setCanUpdate(self, update)

	label = property(lambda self:self._label, setLabel)
	alignment = property(lambda self:self._alignment, _setAlignment)
