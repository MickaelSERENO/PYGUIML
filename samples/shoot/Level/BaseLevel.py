import pyguiml
import sfml as sf

class BaseLevel(pyguiml.Updatable):
	def __init__(self, parent=None):
		pyguiml.Updatable.__init__(self, parent)
		self.ennemisList = list()
		self.buildingList = list()
		self.salvePosition = []
		self.buildingPosition = []
		self.salve = 0
		self.speedScroll = 0
	
	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		if render:
			render.moveView(sf.Vector2(0, self.speedScroll))
			if len(self.salvePosition) > self.salve and \
					render.getViewPosition().y < self.salvePosition[self.salve]:
				print("new")
				self.salve+=1
				self.newSalve()

		self.updateSalve()
		pyguiml.Updatable.update(self, render)

	def newSalve(self):
		pass

	def updateSalve(self):
		pass

	def touchPlayer(self):
		self.parent.removeLive()
