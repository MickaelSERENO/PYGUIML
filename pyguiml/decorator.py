from Widget import Widget
from Updatable import Updatable

def forDrawing(function):
	def returnForDrawing(self, render=None, *args, **kwargs):
		if self.isDrawing:
			if not render:
				render = self.getRender()
			return function(self, render, *args, **kwargs)
		return Widget.draw(self, render, *args, **kwargs)
	return returnForDrawing

def forUpdate(function):
	def returnForUpdate(self, render=None, *args, **kwargs):
		if self.canUpdate:
			if not render:
				render = self.getRender()
			return function(self, render, *args, **kwargs)
		return Updatable.update(self, render, *args, **kwargs)
	return returnForUpdate
