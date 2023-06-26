import cv2
import pyglet
from PIL import Image
import sys
from image_board import ImageBoard


#window = pyglet.window.Window(fullscreen = True)
window = pyglet.window.Window(800, 500)
board = ImageBoard()


@window.event
def on_key_press(symbol, modifiers):
    """
    handle key press: quit on Q
    """
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    #board.move(x, y, dx, dy)
    #board.scale(x, y, dx, dy)
    board.rotate(x, y, dx, dy)


@window.event
def on_draw():
    window.clear()
    board.draw()


pyglet.app.run()
