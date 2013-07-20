import pyguiml
from Context import Context
import sfml as sf

class Credit(Context):
	def __init__(self, gameObject, parent=None):
		Context.__init__(self, gameObject, parent)
		label = pyguiml.Label(None, source="Ce jeu vous a été présenté par Gaulois94, grâce à la SFML. \n\n\n\n\n\n\n\n\n\n\n\n\n Il a pour but de montrer l'efficacité de la SFML, et sert surtout de test pour PYGUIML : une lib faites pour la SFML en python. Ce jeu est tout simplement un petit shootem up, assez simple", font=sf.Font.from_file("DejaVuSans.ttf"))

		self.addChild(pyguiml.TextArray(self, sizeX=gameObject.view.size.x, label=label, cutStyle=pyguiml.Cut.Word), name="Text")
		self["Text"].posOrigin = pyguiml.Position.Center
		self["Text"].pos = gameObject.view.size/2

	@pyguiml.decorator.forUpdate
	def update(self, render):
		render.moveView(sf.Vector2(0, 1))
		if render.getViewPosition().y > self["Text"].getPos(False).y + self["Text"].size.y + \
				10:
			self.changeContext("First Menu")
		pyguiml.Updatable.update(self, render)

	def closeContext(self):
		self._gameObject.resetView()
