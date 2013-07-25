from BaseLevel import BaseLevel
import pyguiml
import sfml as sf
from Ennemie import Ennemie

class Level1(BaseLevel):
	def __init__(self, parent=None):
		BaseLevel.__init__(self, parent)
		self.salvePosition= [-10, -100, -400, -480]
		self.speedScroll = -0.3

	def newSalve(self):
		if self.salve < 4:
			salve = str(self.salve)
			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'0')
			self[salve+'0'].pos = sf.Vector2(300, self.salvePosition[self.salve]) 

			self.addChild(Ennemie(self, "small", self.parent.player), name=salve+'1')
			self[salve+'1'].pos = sf.Vector2(400, self.salvePosition[self.salve]) 

	def updateSalve(self):
		pass
