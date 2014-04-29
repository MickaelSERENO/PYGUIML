from Widget import *
from Render import Render
from Image import Image
from Button import Button
from Label import Label
from Updatable import Updatable
import decorator
import sfml as sf

class Frame(Render, sf.RenderTexture):
    def __init__(self, parent=None, rect=sf.Rectangle(), backgroundColor=sf.Color.BLACK,\
            title=str(), backgroundImage=Image(), drawTitleButton = True,\
            buttonTitleImage=None, \
            characterSizeTitle=12):
        sf.RenderTexture.__init__(self, rect.size.x, rect.size.y)
        Render.__init__(self, parent, rect, backgroundColor, title, backgroundImage)
        self._buttonMoveFrame = None

        if type(title) == str:
            self._title = title
            self._buttonMoveFrame = Button(self, Label(None, self.title, font = sf.Font.from_file("DejaVuSans.ttf")), \
                buttonTitleImage, sf.Rectangle(sf.Vector2(0,0),\
                sf.Vector2(self.size.x, characterSizeTitle)))

        else:
            self._title = title.text.string
            self._buttonMoveFrame = Button(self, title, buttonTitleImage, \
                    sf.Rectangle(sf.Vector2(), sf.Vector2(self.size.x, \
                    title.size.y)))

        self._buttonMoveFrame.isStaticToView = True
        self.resetView()
        self._frameSprite = sf.Sprite(self.texture)
        if not drawTitleButton:
            self._buttonMoveFrame.isDrawing = False

        self._isMoving = False
        self._mousePosMoving = sf.Vector2(0, 0)
        self.rect = self.rect

    @decorator.forUpdate
    def update(self, render=None):
        if self.canUpdate:
            if self._event and self.isMoving:
                self.move(render.convertScreenCoordToTargetPoint(\
                        self._event.mousePos - self._mousePosMoving))
                self._mousePosMoving = self._event.mousePos

            self.clear(self.backgroundColor)
            Updatable.updateFocus(self)
            Updatable.update(self)
            self.display()
            if render:
                render.draw(self._frameSprite)

    def _setTitle(self, button):
        self._buttonMoveFrame = button
        self._buttonMoveFrame.setSize(sf.Vector2(self.size.x, button.size.y))
        self._buttonMoveFrame.setParent(self, pos=1)
        Render._setTitle(self, button.text.text.string)

    def setSize(self, size, resetOrigin=True):
        self.create(size.x, size.y)
        Widget.setSize(self, size)
        self._buttonMoveFrame.size = sf.Vector2(size.x, self._buttonMoveFrame.size.y)

    def setPos(self, pos, withOrigin=True):
        Widget.setPos(self, pos, withOrigin)
        self._frameSprite.position = self.getPos(False)

    def draw(self, drawable, states):
        if self.canDrawing:
            return sf.RenderTexture.draw(self, drawable, states)

    
    def setImageBackgroundButton(self, image):
        self._buttonMoveFrame.image = image

    def _setUpdateButtonMoveFrame(self, canUpdate):
        self._buttonMoveFrame.canUpdate = canUpdate

    def _getIsMoving(self):
        if not self._isMoving and self._event:
            self._isMoving = self._buttonMoveFrame.isActive
            self._mousePosMoving = self._event.mousePos

        elif not (self._event and (self._event.getPressedKeys(self._buttonMoveFrame.howActiveKeyboard[0]) or \
                self._event.getMouseClicked(self._buttonMoveFrame.howActiveMouse[0]))):
            self._isMoving = False

        return self._isMoving

    draw = sf.RenderTexture.draw
    updateFocus = Updatable.updateFocus
    isMoving = property(lambda self:self._getIsMoving())
    updateButtonMoveFrame = property(lambda self:self._buttonMoveFrame.canUpdate, \
            _setUpdateButtonMoveFrame)
    size = property(lambda self : self.getSize(), setSize)
