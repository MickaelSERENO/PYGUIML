import sfml as sf

def rectCollision(rect1,rect2):
	return (rect1.left + rect1.width <= rect2.left or \
		rect1.left >= rect2.left + rect2.width or \
		rect1.top + rect1.height <= rect2.top or \
		rect1.top >= rect2.top+rect2.height)

def circle(x, centerx, centery, size):
	y1 = (2*centery + sqrt(4*(-(x-centerx)*(x-centerx)+size*size)))/2
	y2 = (2*centery - sqrt(4*(-(x-centerx)*(x-centerx)+size*size)))/2
	return sf.Vector2f(y1, y2)

