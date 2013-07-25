import pyguiml
import sfml as sf
from Shoot import Shoot
import random
from math import sin, atan, cos, copysign

class Ennemie(pyguiml.Widget):
	pyguiml.Widget.filesLoading["smallEnnemie"] = \
			sf.Texture.from_file("Ressources/Images/smallEnnemie.png")
	pyguiml.Widget.filesLoading["bigEnnemie"] = \
			sf.Texture.from_file("Ressources/Images/bigEnnemie.png")
	def __init__(self, parent, typeEnnemie, player):
		self._sprite = None
		self.live = 1
		if typeEnnemie == "big":
			self._sprite = sf.Sprite(pyguiml.Widget.filesLoading["bigEnnemie"])
			self.live = 3
		else:
			self._sprite = sf.Sprite(pyguiml.Widget.filesLoading["smallEnnemie"])

		self.player = player
		self.timer = sf.Clock()
		self.vitesseShoot = 5

		pyguiml.Widget.__init__(self, parent, self._sprite.global_bounds)
		self.canFocus=False

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		if self.timer.elapsed_time.seconds > 0.40 and self.isDrawing:
			self.timer.restart()
			chance = sf.Vector2(random.uniform(-100, 100), random.uniform(-0.3, 0.3))
			pos = self.pos
			vector = self.player.pos + chance - pos

			self.addChild(Shoot(None, "Ennemie", \
					self.getPos(False), sf.Vector2(\
					abs(self.vitesseShoot * cos(atan(vector.y / vector.x))) * copysign(1, vector.x), \
					copysign(1, vector.y) * abs(self.vitesseShoot * sin(atan(vector.y / vector.x))))))
		elif not self.isDrawing and len(self.child)==0:
			self.parent = None
			return

		pyguiml.Widget.update(self, render)

	@pyguiml.decorator.forDrawing
	def draw(self, render=None):
		render.draw(self._sprite)

	def setPos(self, pos, withOrigin=True):
		pyguiml.Widget.setPos(self, pos, withOrigin)
		self._sprite.position = self.getPos(False)

	def touchPlayer(self):
		self.parent.touchPlayer()

	def isTouch(self):
		self.live -= 1
		if self.live == 0:
			self.parent.ennemieList.remove(self)
			self.isDrawing = False
