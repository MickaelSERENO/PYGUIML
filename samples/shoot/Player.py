import pyguiml
from Shoot import Shoot
import sfml as sf
from copy import copy

class Player(pyguiml.Widget):
	def __init__(self, parent=None):
		self._texture = sf.Texture.from_file("Ressources/Images/player.png")
		pyguiml.Widget.filesLoading["player"] = self._texture
		self._sprite = sf.Sprite(self._texture)
		self._sprite.ratio = sf.Vector2(20,30)/self._sprite.local_bounds.size
		self._timer = sf.Clock()
		pyguiml.Widget.__init__(self, parent, sf.Rectangle(sf.Vector2(0, 0),\
				sf.Vector2(20, 30)))

	def __del__(self):
		del pyguiml.filesLoading["player"]

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		if self.event:
			move = sf.Vector2()
			if self.event.getPressedKeys(sf.Keyboard.LEFT):
				move.x = -8
			if self.event.getPressedKeys(sf.Keyboard.RIGHT):
				move.x = 8
			if self.event.getPressedKeys(sf.Keyboard.DOWN):
				move.y = 8
			if self.event.getPressedKeys(sf.Keyboard.UP):
				move.y = -8

			move = move + sf.Vector2(0, self.parent[1].speedScroll)
			self.move(move)


			if self.event.getPressedKeys(sf.Keyboard.A) and \
					self._timer.elapsed_time.seconds > 0.10:
				self._timer.restart()
				self.addChild(Shoot(None, "Player", \
						self.getPos(False), sf.Vector2(0, -10)))

		pyguiml.Widget.update(self, render)

	@pyguiml.decorator.forDrawing
	def draw(self, render=None):
		render.draw(self._sprite)

	def setPos(self, pos, withOrigin=True):

		pyguiml.Widget.setPos(self, pos, withOrigin)
		render = self.getRender()
		viewRect = render.getViewRect()
		selfPos = self.getPos(False)
		if selfPos.x < viewRect.left:
			selfPos.x = viewRect.left
		elif selfPos.x + self.size.x > viewRect.left + viewRect.width:
			selfPos.x = viewRect.left + viewRect.width - self.size.x
		if selfPos.y < viewRect.top:
			selfPos.y = viewRect.top
		elif selfPos.y+self.size.y > viewRect.top + viewRect.height:
			selfPos.y = viewRect.top + viewRect.height - self.size.y

		pyguiml.Widget.setPos(self, selfPos, False)
		self._sprite.position = self.getPos(False)
