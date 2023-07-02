import cv2
import pyglet
from PIL import Image
import sys
from image_board import ImageBoard
from DIPPID import SensorUDP


PORT = 5700
sensor = SensorUDP(PORT)

window = pyglet.window.Window(fullscreen = True)
board = ImageBoard(window.width, window.height)


@window.event
def on_key_press(symbol, modifiers):
    """
    handle key press: quit on Q, restart on R
    """
    if symbol == pyglet.window.key.R:
        board.cursors = board.init_cursors()
        board.images = board.read_images()
    if symbol == pyglet.window.key.Q:
        window.set_fullscreen(False)
        window.close()
        sys.exit(0)


@window.event
def on_draw():
    if sensor.has_capability('events'):
        board.update(sensor.get_value('events'))
    else:
        board.update(None)
    window.clear()
    board.draw()
    

pyglet.app.run()
