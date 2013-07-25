import pyguiml


class Context(pyguiml.Updatable):
	def __init__(self, gameObject, parent=None):
		pyguiml.Updatable.__init__(self, parent)
		self._gameObject = gameObject

	@pyguiml.decorator.forUpdate
	def update(self, render=None):
		pyguiml.Updatable.update(self, render)

	def changeContext(self, contextName):
		self.closeContext()
		self.canUpdate = False
		self.updateAllChild = False

		self._gameObject.currentContext = contextName

	def closeContext(self):
		pass

	def openContext(self):
		pass
