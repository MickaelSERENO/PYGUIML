from Label import Label
from Widget import *
import sfml as sf
from functools import reduce
import decorator

Cut = enum('Character', 'Word')

class TextArray(Widget):
	def __init__(self, parent = None, pos=sf.Vector2(0, 0), sizeX=200,\
			space=5, label=Label(), alignment = Position.TopLeft, cutStyle=Cut.Character):
		Widget.__init__(self, parent,sf.Rectangle(pos, sf.Vector2(sizeX, 0)))

		self._labelList = list()
		self._space = space
		self._label = None
		self._alignment = None
		self._cutStyle = cutStyle

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

	def setSize(self, size, resetOrigin=True):
		Widget.setSize(self, size, resetOrigin)
		if size != self.size:
			for label in self._labelList:
				label.scale = size / self.size

		self.setPos(self.getPos(False), False)

	def setLabel(self, label, resetSize=False):
		self._labelList = list()

		if label.text.string:
			characterIndex = 0
			characterPos = label.text.find_character_pos(0).x

			oldCharacterIndex = characterIndex
			oldCharacterPos = characterPos

			if self._cutStyle == Cut.Character:
				while oldCharacterIndex < len(label.text.string):
					for i in range(oldCharacterIndex, len(label.text.string)):
						characterIndex += 1
						if label.text.find_character_pos(i).x - oldCharacterPos > self.size.x\
								or label.text.string[i] == '\n' or characterIndex > len(label.text.string):

							if i != 0 and label.text.string[i] != '\n':
								characterIndex -= 1

							characterPos = label.text.find_character_pos(characterIndex).x

							self._labelList.append(Label(self, \
								label.text.string[oldCharacterIndex:characterIndex].replace('\n', ''),\
								reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
								self._labelList, self._pos) + \
								sf.Vector2(0, self._space * len(self._labelList)),\
								label.characterSize, label.font,\
								label.style))
							self._labelList[-1].scale = label.scale
							oldCharacterPos = characterPos
							oldCharacterIndex = characterIndex
							break;

			elif self._cutStyle == Cut.Word:
				listeString = label.text.string.split(" ")
				print(listeString)
				i=0
				breakLine = 0
				while i < len(listeString):
					string = listeString[i]
					characterIndex += len(string) + 1
					if i == len(listeString)-1 or label.text.find_character_pos(len(listeString[i+1]) + characterIndex).x - oldCharacterPos >= self.size.x\
							or '\n' in string:
						if '\n' in string and breakLine < len(string.split("\n")):
							string2 = string.split('\n')
							characterIndex = characterIndex + len(string2[breakLine]) - len(string)
							print("break")
							breakLine += 1
							if breakLine < len(string2):
								i-=1
							else:
								breakLine = 0
						if i == len(listeString)-1: 
							characterIndex += 1

						characterPos = label.text.find_character_pos(characterIndex).x

						self._labelList.append(Label(self, \
							label.text.string[oldCharacterIndex:characterIndex].replace('\n', ''),\
							reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
							self._labelList, self._pos) + \
							sf.Vector2(0, self._space * len(self._labelList)),\
							label.characterSize, label.font,\
							label.style))
						self._labelList[-1].globalScale = label.globalScale
						oldCharacterPos = characterPos
						oldCharacterIndex = characterIndex
					i+=1

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

	def removeLine(self, index):
		del self._labelList[index]
		self.pos = self.getPos(False)

	def removeCharacter(self, index):
		label = Label(None, self._label.text.string[0:index] + \
				self._label.text.string[index+1:len(self._label.text.string)], \
				characterSize = self._label.characterSize, font=\
				self._label.font, style = self._label.style, color=\
				self._label.color)
		label.size = self._label.size
		self.setLabel(label)

	def removePlageCharacters(self, plage):
		label = Label(None, self._label.text.string[0:plage.x] + \
				self._label.text.string[plage.y:len(self._label.text.string)], \
				characterSize = self._label.characterSize, font=\
				self._label.font, style = self._label.style, color=\
				self._label.color)
		label.size = self._label.size
		self.setLabel(label)


	def setCanUpdate(self, update):
		for label in self._labelList:
			label.canUpdate = update
		Updatable.setCanUpdate(self, update)

	label = property(lambda self:self._label, setLabel)
	alignment = property(lambda self:self._alignment, _setAlignment)
