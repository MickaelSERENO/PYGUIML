import pyguiml
from FirstMenu import FirstMenu
from Option import Option
from Credit import Credit
from StartGame import StartGame
from DataManager import *
import sfml as sf

class Game(pyguiml.Window):
	def __init__(self, videoMode=sf.VideoMode(800, 600, 32), title="game",\
			parent=None, framerateLimit=60, backgroundColor = sf.Color.BLACK,\
			backgroundImage = pyguiml.Image()):
		pyguiml.Window.__init__(self, videoMode, title, parent, framerateLimit,\
				backgroundColor, backgroundImage)
		self.dataManager = DataManager()
		firstMenu = FirstMenu(self, self, permanentActivation=True)
		self.addChild(firstMenu, name="First Menu")
		self.addChild(Option(self, self), name='Option')
		self.addChild(Credit(self, self), name="Credit")
		self.addChild(StartGame(self, self), name="StartGame")
		self._currentContext = None
		self._context = [firstMenu, self["Option"], self["Credit"], self["StartGame"]]

		for context in self._context:
			context.canUpdate = False
			context.updateAllChild = False

		self._changeContext("First Menu")

	def _changeContext(self, contextName):
		self._currentContext = self[contextName]
		self[contextName].openContext()
		self[contextName].canUpdate = self[contextName].updateAllChild=True

	currentContext = property(lambda self:self._currentContext, _changeContext)
