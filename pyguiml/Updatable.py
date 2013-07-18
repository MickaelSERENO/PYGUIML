import sfml as sf
from EventManager import EventManager

class Updatable:
	"""Basic class who can update a child hierarchy"""
	_focusIsChecked = False
	def __init__(self, parent=0):
		self._changeWindow = False
		self._event = None
		self._child = list()
		self._childDictName = dict()
		self._parent = None
		self.canUpdate = True
		self.canFocus = True
		self.updateAllChild = True
		self.setParent(parent)

	def __del__(self):
		self.parent = 0
		for it in self._child:
			self.removeChild(it)

	def __getitem__(self, value):
		return self.getChild(value)

	def getChild(self, value):
		if type(value) is str:
			try:
				return self._childDictName[value]
			except KeyError:
				print("Child ", value, " doesn't exist")
				return None
		elif type(value) is int:
			try:
				return self._child[value]
			except IndexError:
				print("Child on index ", value, " doesn't exist")
				return None

		elif isinstance(value, Updatable):
			if self.isChild(child):
				index = -1
				name = None
				for child, i in enumerate(self._child):
					if child is value:
						index = i
						break;

				for key, item in self._childDictName:
					if item is value:
						name = key
						break

				return index, name

			else:
				return None

		else:
			return None


	def updateFocus(self):
		for child in self._child[::-1]:
			if self._focusIsChecked:
				return
			if child.canFocus:
				child.updateFocus()
			else:
				Updatable.updateFocus(child)

	def update(self, render=None):
		"""THIS methode Update all child of this Widget. 
		It launch them Update() for drawing there"""

		if self.updateAllChild:
			for child in self._child:
				child.update(render)
			self._changeWindow=False
	
	def removeChild(self, child):
		"""Remove child in the object"""
		try:
			if isinstance(child, Updatable):
				self._child.remove(child)
				for key, value in self._childDictName.items():
					if value is child:
						del self._childDictName[key]
						break
			elif isinstance(child, int):
				index = child
				child = self._child[child]

				for key, value in self._childDictName.items():
					if value is child:
						del self._childDictName[key]
				del self._child[index]

			else:
				for key, value in self._childDictName.items():
					if key is child:
						del self._childDictName[key]
						self._child.remove(value)
						break

			return True
		except ValueError:
			print("child is not a child of self._child")
			return False
		except IndexError:
			print("can't find the child index in self._child")
			return False
		else:
			return True

		child._parent = 0

	def addChild(self, child, pos="End", name=None):
		"""child become a widget's child"""
		if child._parent is not self:
			child.setParent(self,pos, name)
	
		if pos=="End":
			pos = len(self._child)
		if not self.isChild(child) and child:
			self._child.insert(pos, child)

		if name and self.isChild(child):
			self._childDictName[name]=child

	def isChild(self, child):
		""" This methode say if child is a widget's child"""
		return child in self._child
	
	def getEventFromRootParent(self):
		if isinstance(self._parent, Updatable):
			return self._parent.getEventFromRootParent()
		return None

	def getRender(self):
		if isinstance(self._parent, Updatable):
			return self._parent.getRender()
		else:
			return None

	def setParent(self, parent, pos="End", name=None):
		"""Set the Updatable's parent"""

		if isinstance(self._parent, Updatable):
			if self._parent.isChild(self):
				self._parent.removeChild(self)

		self._parent = parent

		if isinstance(self._parent, Updatable):
			self._parent.addChild(self, pos, name)
		self._updateEvent()

	def _getParentList(self):
		parentList = []
		if self._parent:
			parentList.append(self._parent)
			parentList.extend(self._parent._getParentList())
		return parentList

	def addNameOnWidget(self, widget, name):
		self._childDictName[name] = widget

	def getNameOnWidget(self, widget):
		key = None
		for key, value in self._childDictName.items():
			if value is widget:
				return key

	def _updateEvent(self):
		for child in self._child:
			if child:
				child._updateEvent()
		event = self._event
		self._event = self.getEventFromRootParent()

		if event is not self._event:
			self._changeWindow = True


	parent = property(lambda self:self._parent,\
			lambda self, parent: self.setParent(parent))
	child = property(lambda self:self._child)
	changeWindow = property(lambda self:self._changeWindow)
	event = property(lambda self:self._event)
	parentList = property(lambda self:self._getParentList())
