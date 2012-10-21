from copy import copy
from EventManager import EventManager

class Updatable():
	def __init__(self, parent):
		self._parent = None
		self._child = list()
		self.parent = parent
		self._changeWindow = False

	def __del__(self):
		if self._parent:
			self._parent.removeChild(self)

		for child in self._child:
			if child:
				del child

	def _setParent(self, parent, pos=-1):
		if self._parent is not None:
			self._parent.addChild(self)

		oldEvent = getEventManager()
		self._parent = parent
		newEvent = getEventManager()

		if(newEvent is not oldEvent):
			self._changeWindow = True

	def _getParent(self):
		return self._parent

	parent=property(_setParent, _getParent)
