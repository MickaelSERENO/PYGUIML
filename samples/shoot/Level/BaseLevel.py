import pyguiml
import sfml as sf

class BaseLevel(pyguiml.Updatable):
	def __init__(self, parent=None):
		pyguiml.Updatable.__init__(self, parent)
		self.ennemieList = list()
		self.buildingList = list()
		self.salvePosition = []
		self.buildingPosition = []
		self.salve = 0
		self.speedScroll = 0
		self.moveEnnemie = list(list())
	
	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		if render:
			render.moveView(sf.Vector2(0, self.speedScroll))
			if len(self.salvePosition) > self.salve and \
					render.getViewPosition().y < self.salvePosition[self.salve]:
				self.newSalve()
				self.salve+=1

			copyList = self.moveEnnemie.copy()
			i = 0
			for ennemi, direction, stop in copyList:
				move = sf.Vector2()
				if direction.x < 0 and ennemi.pos.x > stop.x:
					move.x = direction.x
				elif direction.x > 0 and ennemi.pos.x < stop.x:
					move.x = direction.x
				if direction.y < 0 and ennemi.pos.y > stop.y:
					move.y = direction.y
				elif direction.y > 0 and ennemi.pos.y < stop.y:
					move.y = direction.y

				if move == sf.Vector2():
					print(ennemi.pos.x)
					print("here")
					del self.moveEnnemie[i]
					i-=1
				else:
					ennemi.move(move)
				i+=1

		pyguiml.Updatable.update(self, render)

	def newSalve(self):
		pass

	def touchPlayer(self):
		self.parent.player.isTouch()
