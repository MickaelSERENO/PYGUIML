import pyguiml
import sfml as sf

class Shoot(pyguiml.Widget):
	pyguiml.Widget.filesLoading["playerLaser"]=\
			sf.Texture.from_file("Ressources/Images/playerLaser.png")
	pyguiml.Widget.filesLoading["ennemieLaser"]=\
			sf.Texture.from_file("Ressources/Images/ennemieLaser.png")

	def __init__(self, parent, load, pos, direction):
		self._sprite=None
		if load=="Player":
			self._sprite=sf.Sprite(pyguiml.Widget.filesLoading["playerLaser"])
		else:
			self._sprite=sf.Sprite(pyguiml.Widget.filesLoading["ennemieLaser"])
		self.load = load
		self._direction = direction
		pyguiml.Widget.__init__(self, parent, \
				sf.Rectangle(pos, self._sprite.global_bounds.size))
		self.canFocus=False

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		if render:
			if not render.isInView(self.rect):
				self.__del__()
				return
		if self.load == "Ennemie" and pyguiml.functions.rectCollision(self.rect, self.parent.player.rect):
			self.parent.touchPlayer()
			self.parent.removeChild(self)
		elif self.load=="Player":
			for ennemie in self.parent.parent[1].ennemieList:
				if pyguiml.functions.rectCollision(self.rect, ennemie.rect):
					ennemie.isTouch()
					self.parent.removeChild(self)
					return
		self.move(self._direction)
		pyguiml.Widget.update(self, render)

	@pyguiml.decorator.forDrawing
	def draw(self, render=None):
		if render:
			render.draw(self._sprite)
		pyguiml.Widget.draw(self, render)

	def setPos(self, pos, withOrigin=True):
		pyguiml.Widget.setPos(self, pos, withOrigin)
		self._sprite.position = self.getPos(False)
