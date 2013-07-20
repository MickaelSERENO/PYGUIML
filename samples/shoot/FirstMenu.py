import pyguiml
import sfml as sf
from Context import Context

class FirstMenu(pyguiml.SelectionMenu, Context):
	def __init__(self, gameObject, parent=None, rect=sf.Rectangle(),\
			alignment = pyguiml.Position.Center, spacing=sf.Vector2(0, 5), \
			autoDefineSize = True, select=False, active=False, \
			alwaysUpdateSelection=True, alwaysUpdateActivation=True, \
			permanentSelection=True, permanentActivation=True, \
			changeRight = sf.Keyboard.RIGHT, changeLeft = sf.Keyboard.LEFT,\
			changeTop = sf.Keyboard.UP, changeBottom = sf.Keyboard.DOWN):
		Context.__init__(self, gameObject, parent)
		pyguiml.SelectionMenu.__init__(self, parent, rect, alignment, spacing, autoDefineSize, select, \
				active, alwaysUpdateSelection, alwaysUpdateSelection, permanentSelection, \
				permanentActivation, changeRight, changeLeft, changeTop, changeBottom)

		self.addWidget(pyguiml.Button(self, pyguiml.Label(None, "Start Game",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf"))), sf.Vector2(0, 0))
		self.addNameOnWidget(self.child[-1], "Start Game")
		self.addWidget(pyguiml.Button(self, pyguiml.Label(None, "Option",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf"))), sf.Vector2(0, 1))
		self.addNameOnWidget(self.child[-1], "Option")
		self.addWidget(pyguiml.Button(self, pyguiml.Label(None, "Crédit",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf"))), sf.Vector2(0, 2))
		self.addNameOnWidget(self.child[-1], "Credit")

		self.addWidget(pyguiml.Button(self, pyguiml.Label(None, "Quitter",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf"))), sf.Vector2(0, 3), name="Quit")

		self.posOrigin = pyguiml.Position.Center
		self.pos = (gameObject.size)/2
		self.setAllActiveMouseKeyboard(sf.Keyboard.RETURN, sf.Mouse.LEFT)

		self._background = pyguiml.Image(None, "Ressources/Images/FirstMenu.jpg", delTextureCreated = False)
#		gameObject.backgroundImage = self._background

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		pyguiml.SelectionMenu.update(self, render)
		if self._currentSelect and self.currentSelect.isActive:
			if self.currentSelect is self.getChild("Quit"):
				self._gameObject.close()
			else:
				self.changeContext(self.getNameOnWidget(self.currentSelect))

	def closeContext(self):
		self.permanentSelection = False
		self.permanentActivation = False
		self.deselectIt()
		self.disactiveIt()
		print("ok")
		self._gameObject.backgroundImage = None

	def openContext(self):
		self.permanentSelection = True
		self.permanentActivation = True
		self.selectIt()
		self.activeIt()
		self._gameObject.backgroundImage = self._background
