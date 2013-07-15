from Label import Label
from Widget import *
import sfml as sf
from functools import reduce

class TextArray(Widget):
	def __init__(self, parent = None, pos=sf.Vector2(0, 0), sizeX=200,\
			space=5, label=Label()):
		Widget.__init__(self, parent, pos, sf.Rectangle(pos, sf.Vector2(sizeX, 0)))

		self._labelList = list()

		self._label = None
		self.setLabel(label, False)


	def setPos(self, pos, withOrigin=True):
		oldPos = self.pos
		Widget.setPos(self, pos, withOrigin)
		for label in self._label:
			label.move

	def setLabel(self, label, resetSize=False):
		self._labelList = list()

		characterIndex = 0
		characterPos = 0

		oldCharacterIndex = characterIndex
		oldCharacterPos = characterPos
		while oldCharacterIndex < len(label.text.string):
			for i in range(oldCharacterIndex, len(label.text.string)):
				
				if label.text.find_character_pos(i) - self.pos.x > self.size.x\
						or label.text.string[i] == '\n':
					if i != 0 and label.text.string[i] != '\n':
						characterIndex -= 1

					characterPos = label.text.find_character_pos(characterPos)			

					if label.text.string[oldCharacterIndex:i+1] != '\n':
						self._labelList.append(Label(self, \
							label.text.string[oldCharacterIndex:i+1].replace('\n', ''),\
							reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
							self._labelList, self.pos) + self._space * len(self._labelList),\
							label.characterSize, label.font,\
							label.style))

						self._labelList[-1].size = sf.Vector2(characterPos.x - oldCharacterPos.x, \
								label.size.y)
					oldCharacterPos = characterPos
					characterIndex = i
					break;

		if resetSize:
			self.size = self.size
		else:
			Widget.setSize(self, sf.Vector2(max([newLabel.size.x for newLabel in self._labelList]), \
				self._labelList[-1].getPos(False).y + self._labelList[-1].size.y - self._pos.y))

	label = property(lambda self:self._label, setLabel)
