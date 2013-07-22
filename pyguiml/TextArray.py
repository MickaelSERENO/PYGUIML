from Label import Label
from Widget import *
import sfml as sf
from functools import reduce
from functions import *
import re
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
		self._maxSize = sizeX

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
		for l in self._labelList:
			l.parent=None
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
						if label.text.find_character_pos(i).x - oldCharacterPos > self._maxSize\
								or label.text.string[i] == '\n' or characterIndex > len(label.text.string):

							if i != 0 and label.text.string[i] != '\n':
								characterIndex -= 1

							characterPos = label.text.find_character_pos(characterIndex).x

							self._labelList.append(Label(self, \
								label.text.string[oldCharacterIndex:characterIndex],\
								reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
								self._labelList, self._pos) + \
								sf.Vector2(0, self._space * len(self._labelList)),\
								label.characterSize, label.font,\
								label.style))
							self._labelList[-1].globalScale = label.globalScale
							if re.match(r"^[ \n]*$", self._labelList[-1].text.string):
								print("ok")
								self._labelList[-1].size = sf.Vector2(\
										self._labelList[-1].size.x, self._labelList[-1].characterSize)
							oldCharacterPos = characterPos
							oldCharacterIndex = characterIndex
							break;

			elif self._cutStyle == Cut.Word:
				listeString = re.split("( )", label.text.string)
				print(listeString)
				i=0
				k=0
				breakLine = 0
				haveBreak=None
				while i < len(listeString):
					string = listeString[i]
					if not '\n' in string:
						characterIndex += len(string)
					if i == len(listeString)-1 or label.text.find_character_pos(\
							len(listeString[i+1]) + characterIndex).x - oldCharacterPos >= \
							self._maxSize or '\n' in string:
						if '\n' in string and breakLine < len([s for s in re.split("(\n)", string) if s=='\n']):
							string2 = re.split("(\n)", string)

							while string2[k] != '\n':
								characterIndex+=len(string2[k])
								k+=1
							if string2[k]:
								characterIndex+=1
							k+=1
							breakLine += 1

							if breakLine < len([s for s in string2 if s == '\n']):
								i-=1
							else:
								haveBreak=len(string2[k])
								k=0
								breakLine = 0

						characterPos = label.text.find_character_pos(characterIndex).x
						print(characterPos, characterIndex, "character")
						self._labelList.append(Label(self, \
							label.text.string[oldCharacterIndex:characterIndex],\
							reduce(lambda x, y : x + sf.Vector2(0, y.size.y),\
							self._labelList, self._pos) + \
							sf.Vector2(0, self._space * len(self._labelList)),\
							label.characterSize, label.font,\
							label.style))
						self._labelList[-1].globalScale = label.globalScale

						if re.match(r"^[ \n]*$", self._labelList[-1].text.string):
							self._labelList[-1].size = sf.Vector2(\
									self._labelList[-1].size.x, self._labelList[-1].characterSize)
						oldCharacterPos = characterPos
						oldCharacterIndex = characterIndex
						if haveBreak:
							characterIndex+=haveBreak
							haveBreak=None
					i+=1
		print(len(self._labelList), "len")

		if resetSize:
			self.size = self.size
		else:
			Widget.setSize(self, sf.Vector2(max([newLabel.size.x for newLabel in self._labelList]), \
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


	def getCharacterPos(self, index):
		if index < len(self._label.text.string):
			somme = 0
			i=0
			while i < len(self._labelList) and index > somme + \
					len(self._labelList[i].text.string):
				somme += len(self._labelList[i].text.string)
				i+=1
			return self._labelList[i].text.find_character_pos(index - somme)

	def getCharacterIndex(self, pos):
		if len(self._labelList) == 0:
			return None
		elif pos.y <= self._labelList[-1].getPos(False).y:
			return 0
		elif pos.y >= self._labelList[-1].getPos(False).y + \
				self._labelList[-1].y:
			return len(self._label.text.string) - 1
		
		i = 0
		while not (pos.y > self._labelList[i].getPos(False).y and \
				pos.y < self._labelList[i].getPos(False).y + spacing + \
				self._labelList[i].size.y):
			i += 1
		x=0
		if pos.x < self._labelList[i].getPos(False).x:
			x=0
		elif pos.x > self._labelList[i].getPos(False).x + self._labelList[i].size.x:
			x = len(self._labelList[i].text.string)-1
		else:
			while not (x-1 < len(self._labelList[i].text.string) and \
					x > self._labelList[-1].text.find_character_pos(x) and x < \
					self._labelList[-1].text.find_character_pos(x+1)):
				x+=1
		return x + sum([len(label) for label in self._labelList[0:i]])

	def removeLine(self, index):
		self._labelList[index].parent = None
		del self._labelList[index]
		self.pos = self.getPos(False)

	def getLine(self, index):
		return self._labelList[index]

	def getNumberLine(self):
		return len(self._labelList)

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
