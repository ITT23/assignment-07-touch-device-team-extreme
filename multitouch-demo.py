import cv2
import pyglet
from PIL import Image
import sys
from image_board import ImageBoard
from DIPPID import SensorUDP

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800


PORT = 5700
sensor = SensorUDP(PORT)

#window = pyglet.window.Window(fullscreen = True)
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
board = ImageBoard(WINDOW_WIDTH, WINDOW_HEIGHT)



@window.event
def on_key_press(symbol, modifiers):
    """
    handle key press: quit on Q
    """
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


# # TODO: use touch events here
# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     # TODO: move if single touch
#     board.move(x, y, dx, dy)
#     # TODO: if multi touch: scale or rotate (no movement for one finger with rotation)
#     #board.scale(x, y, dx, dy)
#     #board.rotate(x, y, dx, dy)


# # TODO: use hover events here
# @window.event 
# def on_mouse_motion(x, y, t, modifiers):
#     hover.x = x
#     hover.y = y


@window.event
def on_draw():
    if sensor.has_capability('events'):
        board.update(sensor.get_value('events'))
    window.clear()
    board.draw()
    
    


#def handle_callback(data):
    
    
    # for img in board.images:
    #     for cursor in cursors:
    #        if cursors[int(finger_id)]['target'] == img:
               







    # if len(data) == 2:
    #     print("MULTI")
    #     # multitouch detected
    #     caps1 = data['0']
    #     caps2 = data['1']
        
    #     type1 = caps1['type']
    #     x1 = caps1['x'] * WINDOW_WIDTH
    #     y1 = caps1['y'] * WINDOW_HEIGHT
    #     dx1 = x1 - hover.x
    #     dy1 = y1 - hover.y

    #     hover.y = y1 
    #     hover.x = x1 

    #     type2 = caps2['type']
    #     x2 = caps2['x'] * WINDOW_WIDTH
    #     y2 = caps2['y'] * WINDOW_HEIGHT
    #     dx2 = x2 - hover2.x
    #     dy2 = y2 - hover2.y

    #     hover2.y = y2 
    #     hover2.x = x2 

    #     if type1 == type2 and type1 == 'touch':
    #         board.scale(x1, y1, x2, y2, dx1, dy1, dx2, dy2)
        #elif type1 != type2:
        #    if type1 == 'touch':
        #        board.rotate(x1, y1, dx1, dy1)
        #    elif type2 == 'touch':
        #        board.rotate(x2, y2, dx2, dy2)

        
    # elif len(data) == 1:
    #     print("SINGLE")
    #     type = data['0']['type']
    #     x = data['0']['x'] * WINDOW_WIDTH
    #     y = data['0']['y'] * WINDOW_HEIGHT
    #     dx = x - hover.x
    #     dy = y - hover.y

    #     hover.y = y 
    #     hover.x = x 
    #     if type == 'touch': # or type == 'hover':
    #         board.move(x, y, dx, dy)

#sensor.register_callback('events', handle_callback)

pyglet.app.run()
