from BaseLevel import BaseLevel
import pyguiml
import sfml as sf
from Ennemie import Ennemie

class Level1(BaseLevel):
	def __init__(self, parent=None):
		BaseLevel.__init__(self, parent)
		self.salvePosition= [-10, -50, -150, -380]
		self.speedScroll = -0.3

	def newSalve(self):
		salve = str(self.salve)
		if salve=='0':
			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(300, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'1')
			self[salve+'1'].pos = sf.Vector2(400, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

		if salve == '1':
			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(100, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'1')
			self[salve+'1'].pos = sf.Vector2(380, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(450, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'1')
			self[salve+'1'].pos = sf.Vector2(600, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

		if salve == '2':
			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(-30, self.salvePosition[self.salve] + 50) 
			self.moveEnnemie.append([self[salve+'0'], sf.Vector2(1, 0), sf.Vector2(50, 0)])
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(830, self.salvePosition[self.salve] + 50) 
			self.moveEnnemie.append([self[salve+'0'], sf.Vector2(-1, 0), sf.Vector2(670, 0)])
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(350, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(550, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(250, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(670, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

		elif salve == '3':
			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(-30, self.salvePosition[self.salve] + 50) 
			self.moveEnnemie.append([self[salve+'0'], sf.Vector2(1, 0), sf.Vector2(50, 0)])
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(830, self.salvePosition[self.salve] + 50) 
			self.moveEnnemie.append([self[salve+'0'], sf.Vector2(-1, 0), sf.Vector2(670, 0)])
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(350, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(550, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(250, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "big", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(670, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(350, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(550, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(150, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(750, self.salvePosition[self.salve]) 
			self.ennemieList.append(self.child[-1])
