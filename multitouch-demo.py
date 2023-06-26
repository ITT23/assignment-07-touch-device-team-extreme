import cv2
import pyglet
from PIL import Image
import sys
from image_board import ImageBoard


#window = pyglet.window.Window(fullscreen = True)
window = pyglet.window.Window(800, 500)
board = ImageBoard()
hover = pyglet.shapes.Circle(0, 0, 5, color=(156, 0, 75))


@window.event
def on_key_press(symbol, modifiers):
    """
    handle key press: quit on Q
    """
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


# TODO: use touch events here
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    # TODO: move if single touch
    board.move(x, y, dx, dy)
    # TODO: if multi touch: scale or rotate (no movement for one finger with rotation)
    #board.scale(x, y, dx, dy)
    #board.rotate(x, y, dx, dy)


# TODO: use hover events here
@window.event 
def on_mouse_motion(x, y, t, modifiers):
    hover.x = x
    hover.y = y


@window.event
def on_draw():
    window.clear()
    board.draw()
    hover.draw()


pyglet.app.run()
