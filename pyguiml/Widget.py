import sfml as sf
from EventManager import EventManager
from copy import copy
from Updatable import Updatable
import functions

def enum(*seq, **keys):
    enums = dict(zip(seq,range(len(seq))),**keys)
    return type("Enum", (), enums);

Position = enum('TopLeft','TopRight','Center','BottomLeft','BottomRight')
Direction = enum('Vertical', 'Horizontal')

class Widget(Updatable):
    """Basic class for create Widgets"""

    filesLoading = dict()
    widgetFocus = None

    def __init__(self, parent=0, rect=sf.Rectangle()):
        Updatable.__init__(self,parent)
        self._isDrawing = True
        self._isStaticToView = False
        self.canFocus = True
        self.movingAllChild = False
        self._posStatic = False

        self._origin = sf.Vector2(0,0)
        self._posOrigin = Position.TopLeft

        self._pos = sf.Vector2(rect.left,rect.top)
        self._size = rect.size
        self._scale = sf.Vector2(1,1)
        self._relativeSizeOnView = None
        self._relativePositionOnView = None
        self.clipRect = None
        self.clipChild = True

    def __del__(self):
        self.parent = None

    def getCopyWidget(self):
        """This methode return a copy of this Widget.
        The object's parent and self are reset at 0."""
        copyWidget = copy(self)
        copyWidget._parent = 0
        copyWidget._self = list()
        return copyWidget

    def updateFocus(self):
        Updatable.updateFocus(self)
        if self.canFocus and not Updatable._focusIsChecked:
            if self.canUpdate and self.howFocus():
                Widget.widgetFocus = self
                Updatable._focusIsChecked = True
                return

    def howFocus(self):
        return isinstance(self._event, EventManager) and Updatable.getRender(self).isInView(self.rect) and \
                self._event.isMouseInRect(self.getRectOnScreen(True))

    def update(self, render=None):
        if not render:
            render = Updatable.getRender(self)

        if render and render is not self:
            if self._changeWindow:
                self.relativeSizeOnView = self.relativeSizeOnView
                self.relativeSizeOnView = self.relativeSizeOnView
                if self._isStaticToView:
                    self.setPosStatic(self._posStatic, False)

            if self.isDrawing and render.isInView(self.getRect(True)):
                if type(self.clipRect) is sf.Rectangle:
                    if self.clipChild:
                        render.clipping(self.draw, self.clipRect, self.getPos(False), super().update)
                    else:
                        render.clipping(self.draw, self.clipRect, self.getPos(False))
                        super().update(render)
                else:
                    self.draw(render)
                    super().update(render)
            else:
                super().update(render)
            
        else:
            super().update(render)

    def draw(self, render=None):
        """Draw the Widget on the render"""
        pass
            
    def drawWidget(self, draw=True):
        """If you want thatt at the next update your
        widget will be drawing or not"""
        self._isDrawing = draw

    def drawAllWidget(self, drawing):
        """If you want to show the Widget, put drawing to true"""
        for self in self._self:
            if isinstance(self,Widget):
                self._isDrawing = True

    def move(self, moving):
        """This methode move the widgets. moving is a sf.Vector2 type"""
        self.setPos(self._pos + moving, False)

    def setPosOnScreen(self, position, withOrigin=True):
        render = Updatable.getRender(self)
        if not self._isStaticToView and render:
            self.setPos(render.convertScreenCoordToTargetPoint(position), withOrigin)
        elif not render and not self._isStaticToView:
            self.setPos(position, withOrigin)

    def scale(self, scale):
        self.size *= scale

    def _setScale(self, scale):
        """scale is a sf.Vector2 type.
        This methode set the size of the widget"""
        self._scale = scale
        self.scale(scale / self._scale)

    def addSize(self, addingSize):
        """This methode add a size at the widget.
        addingSize is a sf.Vector2 type"""
        self.size = sf.Vector2(self.size.x+addingSize.x,\
                self.size.y + addingSize.y)
    
    def setPos(self, pos, withOrigin=True):
        if self.movingAllChild:
            for child in self._child:
                if isinstance(child, Widget):
                    self.move(pos.x - self._pos.x, \
                            pos.y - self._pos.y)

        if self._relativePositionOnView == None:
            if withOrigin:
                self._pos = pos + self._origin
            else:
                self._pos = pos

        else:
            self.relativePositionOnView = self._relativePositionOnView

    def setSize(self, size, resetOrigin=True):
        if self._relativeSizeOnView == None:
            self._size = size
            if resetOrigin:
                self._setOriginPos(self._posOrigin)

        else:
            self.relativePositionOnView = self._relativePositionOnView

    def setIsStaticToView(self, new, resetPos=True):
        """Methode for set your widget static on the view or not"""
        self._isStaticToView = copy(new)
        if not self._posStatic:
            self._posStatic = self._pos
        if resetPos and self._isStaticToView:
            self.setPosStatic(self._posStatic, False)

    def getPosOnScreen(self, withOrigin=True, withClipping=False):
        render = Updatable.getRender(self)
        if render is not None:
            return render.convertTargetPointToScreenCoord(self.getPos(withOrigin, withClipping))
        else:
            return self.getPos(withOrigin, withClipping)

    def getPosStatic(self, withOrigin=True):
        if withOrigin:
            return self._posStatic-self._origin
        return self._posStatic

    def getPos(self, withOrigin=True, withClipping=False):
        pos = copy(self._pos)
        if withOrigin:
            pos = pos - self._origin

        if withClipping:
            parentList = reversed([self]+self.parentList)
            clipRect = None
            root = None
            clipRect = None
            for parent in parentList:
                if isinstance(parent, Widget) and parent.clipRect and parent.clipChild:
                    root = parent
                    if clipRect:
                        if clipRect.position.x < parent.clipRect.position.x +\
                                parent.getPos(False).x:
                            clipRect.position.x = parent.clipRect.position.x + parent.getPos(False).x

                        if clipRect.position.y < parent.clipRect.position.y +\
                                parent.getPos(False).y:
                            clipRect.position.y = parent.clipRect.position.y + parent.getPos(False).y
                    else:
                        clipRect = copy(parent.clipRect)
                        clipRect = copy(parent.clipRect)
                        clipRect.position += parent.getPos(False)

            if root:
                pos.x = max(pos.x, clipRect.position.x)
                pos.y = max(pos.y, clipRect.position.y)

        return pos

    def getSize(self, withClipping=False):
        size = copy(self._size)
        pos = self.getPos(False, True)
        if withClipping:
            parentList = reversed([self]+self.parentList)
            root = None
            clipRect = None
            for parent in parentList:
                if isinstance(parent, Widget) and parent.clipRect and parent.clipChild:
                    root = parent

                    if clipRect:
                        if clipRect.position.x < parent.clipRect.position.x +\
                                parent.getPos(False).x:

                            clipRect.width = min(\
                                    parent.clipRect.width, clipRect.position.x + clipRect.width -\
                                    parent.clipRect.position.x - parent.getPos(False).x)

                            clipRect.position.x = parent.clipRect.position.x + parent.getPos(False).x

                        else:
                            clipRect.width = min(parent.clipRect.position.x + \
                                    parent.getPos(False).x + parent.clipRect.width-clipRect.position.x, \
                                    parent.clipRect.width)

                        if clipRect.position.y < parent.clipRect.position.y +\
                                parent.getPos(False).y:
                            clipRect.height= min(\
                                    parent.clipRect.height, clipRect.position.y + clipRect.height -\
                                    parent.clipRect.position.y - parent.getPos(False).y)
                            clipRect.position.y = parent.clipRect.position.y + parent.getPos(False).y
                        else:
                            clipRect.height = min(parent.clipRect.position.y + \
                                    parent.getPos(False).y + parent.clipRect.height-clipRect.position.y, \
                                    parent.clipRect.height)
                        clipRect.width = max(0, clipRect.width)
                        clipRect.height = max(0, clipRect.height)
                    else:
                        clipRect = copy(parent.clipRect)
                        clipRect.position += parent.getPos(False)

            if root:
                clipRect.width = max(0, clipRect.width)
                clipRect.height = max(0, clipRect.height)
                size.x = min(size.x, clipRect.size.x)
                if clipRect.left > pos.x + self._size.x or \
                        clipRect.left + clipRect.width < pos.x:
                    size.x = 0
                elif clipRect.left < pos.x and clipRect.left + clipRect.width > pos.x + size.x:
                    size.x = size.x
                else:
                    size.x = size.x - (clipRect.position.x - pos.x)

                size.y = min(size.y, clipRect.size.y)
                if clipRect.top > pos.y + self._size.y or \
                        clipRect.top + clipRect.height < pos.y:
                    size.y = 0
                elif clipRect.top < pos.y and clipRect.top + clipRect.height > pos.y + size.y:
                    size.x = size.x
                else:
                    size.y = size.y - (clipRect.position.y - pos.y)

            size.x = max(size.x, 0)
            size.y = max(size.y, 0)

        return size

    def _setOrigin(self, newOrigin):
        """Change the origin of the widget"""
        self.move(newOrigin-self.origin)
        self._origin = newOrigin
        self._posOrigin = None

    def setPosStatic(self, pos, withOrigin=True, setIsStaticToView=True):
        if withOrigin:
            self._posStatic=pos + self._origin
        else:
            self._posStatic=pos

        if setIsStaticToView:
            self._isStaticToView=True
        render = self.getRender()
        if render and self._isStaticToView:
            self.setPos(self._posStatic+render.getViewPosition(), False)

    def _setOriginPos(self, position):
        back = copy(self._origin)

        if position == Position.TopLeft:
            self._origin = sf.Vector2(0,0)
        elif position == Position.TopRight:
            self._origin = sf.Vector2(-self.size.x,0)
        elif position == Position.Center:
            self._origin = self.size/-2
        elif position == Position.BottomLeft:
            self._origin = sf.Vector2(0,-self.size.y)
        elif position == Position.BottomRight:
            self._origin = self.size/-1

        self.move(self._origin-back)
        self._posOrigin = position

    def getSizeOnView(self, withClipping=False):
        render = Updatable.getRender(self)
        if render:
            return self.getSize(withClipping) * render.size / render.view.size * render.viewport.size
        else:
            return self.getSize(withClipping)

    def getSizeOnScreen(self, withClipping=False):
        scale = sf.Vector2(1,1)
        render = Updatable.getRender(self)

        if render is not self:
            if render.view.size.x != 0 and render.view.size.y != 0:
                scale = render.sizeOnScreen / render.view.size * render.viewport.size

        return self.getSize(withClipping) * scale
    
    def getRectOnScreen(self, withClipping=False):
        return sf.Rectangle(self.getPosOnScreen(False, withClipping),\
                self.getSizeOnScreen(withClipping))

    def setAbsolutePosOnView(self, pos, withOrigin=True):
        render = Updatable.getRender(self)
        origin = sf.Vector2(0, 0)
        render = self.getRender()
        if render:
            self.setPos(pos + render.getViewPosition(), withOrigin)
        else:
            self.setPos(pos, withOrigin)

    def getRect(self, withClipping=False):
        return sf.Rectangle(self.getPos(False, withClipping), self.getSize(withClipping))

    def _setRect(self, rect):
        """rect is a sf.Rectangle type.
        This methode set the size and the positions of the widget"""
        self.setSize(rect.size)
        self.setPos(rect.position, False)

    def _setRelativePositionOnView(self, scale):
        render = Updatable.getRender(self)
        if render and scale:
            self._relativePositionOnView = None
            self.pos = render.getViewSizeWithViewportWithZoom() * scale
        self._relativePositionOnView = scale

    def _setRelativeSizeOnView(self, scale, resetOrigin = True):
        render = Updatable.getRender(self)
        if render and scale:
            self._relativePositionOnView = None
            self.setSize(render.getViewSizeWithViewportWithZoom() * scale, resetOrigin)
        self._relativePositionOnView = scale

    isStaticToView = property(lambda self : self._isStaticToView, \
            lambda self,static: self.setIsStaticToView(static))

    origin = property(lambda self: self._origin,\
            lambda self,origin : self._setOrigin(origin))
    posOrigin = property(lambda  self: self._posOrigin,\
            lambda self,position : self._setOriginPos(position))

    size = property(lambda self : self.getSize(), \
            lambda self, dimension : self.setSize(dimension))

    pos = property(lambda self: self.getPos(), \
            lambda self,pos : self.setPos(pos))
    posOnScreen = property(lambda self:self.getPosOnScreen(),\
            lambda self,position:self.setPosOnScreen(position))
    sizeOnScreen = property(lambda self:self.getSizeOnScreen())

    rect = property(lambda self:self.getRect(), \
            lambda self, rect:self._setRect(rect))
    rectOnScreen = property(lambda self:self.getRectOnScreen())
    globalScale = property(lambda self:self._scale,\
            lambda self,newScale : self._setScale(newScale))
    event = property(lambda self:self._event)
    isDrawing = property(lambda self:self._isDrawing,\
            lambda self,draw:self.drawWidget(draw))
    relativePositionOnView=property(lambda self:self._relativePositionOnView,\
            lambda self,scale:self._setRelativePositionOnView(scale))
    relativeSizeOnView=property(lambda self:self._relativeSizeOnView,\
            lambda self,scale:self._setRelativeSizeOnView(scale))
    sizeOnView = property(lambda self : self.getSizeOnView())
    posStatic = property(lambda self:self._posStatic, \
            setPosStatic)
