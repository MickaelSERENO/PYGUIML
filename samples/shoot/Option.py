import pyguiml
from Context import Context
import sfml as sf

class Option(Context):
	def __init__(self, gameObject, parent=None):
		Context.__init__(self, gameObject, parent)
		self.addChild(pyguiml.SelectionMenu(None, spacing=sf.Vector2(30, 15), \
				autoDefineSize = True, alignment=pyguiml.Position.TopLeft, \
				permanentActivation=True, permanentSelection=True), name="Layout Menu")

		self["Layout Menu"].addWidget(pyguiml.Label(None, "Difficulté",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf")), sf.Vector2(0, 0))

		self["Layout Menu"].addWidget(\
				pyguiml.Button(self, pyguiml.Label(None, "Facile", characterSize=24, \
				font=sf.Font.from_file("DejaVuSans.ttf"), color=sf.Color.GREEN)),\
				sf.Vector2(1, 0), name="Easy")
		self["Layout Menu"].addWidget(\
				pyguiml.Button(self, pyguiml.Label(None, "Normale", characterSize=24, \
				font=sf.Font.from_file("DejaVuSans.ttf"), color=sf.Color.GREEN)),\
				sf.Vector2(2, 0), name="Medium")
		self["Layout Menu"].addWidget(\
				pyguiml.Button(self, pyguiml.Label(None, "Difficile", characterSize=24, \
				font=sf.Font.from_file("DejaVuSans.ttf"), color=sf.Color.GREEN)),\
				sf.Vector2(3, 0), name="Hard")

		self["Layout Menu"].addWidget(pyguiml.Label(None, "Nombre de vie",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf")), sf.Vector2(0, 1))
		self["Layout Menu"].addWidget(pyguiml.Label(None, "Volume",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf")), sf.Vector2(0, 2))

		self["Layout Menu"].addWidget(pyguiml.Button(None, pyguiml.Label(None, "Terminer",\
				characterSize=24, font=sf.Font.from_file("DejaVuSans.ttf")), \
				pyguiml.Image(None, "Ressources/Images/FinishButton.jpg"), \
				sf.Rectangle(sf.Vector2(0, 0), sf.Vector2(100, 50))),\
				sf.Vector2(0, 3), name="Finish")
		
		self["Layout Menu"].addWidget(pyguiml.Slide(None, rect=sf.Rectangle(sf.Vector2(), \
				sf.Vector2(500, 25)), step=5, inStep=1, values=sf.Vector2(0, 100)),\
				sf.Vector2(1, 2), sf.Vector2(3, 1), name="Volume Value")

		self._background = pyguiml.Image(None, "Ressources/Images/image.jpg", delTextureCreated = False)
		self["Layout Menu"].setAllActiveMouseKeyboard(sf.Keyboard.RETURN, sf.Mouse.LEFT)
		self["Layout Menu"].getChild("Volume Value").howActiveKeyboard = [sf.Keyboard.LEFT, sf.Keyboard.RIGHT]

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		pyguiml.Updatable.update(self, render)
		if self["Layout Menu"].getChild("Finish").isActive:
			self.changeContext("First Menu")

	def closeContext(self):
		self["Layout Menu"].permanentSelection= False
		self["Layout Menu"].deselectIt()
		self["Layout Menu"].permanentActivation = False
		self["Layout Menu"].disactiveIt()
		self._gameObject.backgroundImage = None

	def openContext(self):
		self["Layout Menu"].permanentSelection= True
		self["Layout Menu"].permanentActivation = True
		self._gameObject.backgroundImage = self._background
		self["Layout Menu"].currentSelect = self["Layout Menu"][(sf.Vector2(2, 0))]
