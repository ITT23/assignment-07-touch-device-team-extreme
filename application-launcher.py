from recognizer import DollarRecognizer, Point
import os
import pyglet
from DIPPID import SensorUDP
import time
import argparse
import sys

PYGLET_WIN_WIDTH = 500
PYGLET_WIN_HEIGHT = 400
MIN_RECORDED_MOUSE_NUMS = 20

class InputManager():

    def __init__(self) -> None:
        self.PORT = 5700
        self.sensor = SensorUDP(self.PORT)
        self.sensor.register_callback('events', self.handle_callback)
        self.points = []
        self.last_input_time = 0
        self.delta_time = 0
        self.threshold_time = 1

    def handle_callback(self, data):
        for finger_id, value in data.items():
            type = value['type']
            x = value['x']
            y = value['y']
            self.points.append(Point(x,y))
            self.last_input_time = time.time()
        
    def check_time(self):
        self.delta_time = time.time() - self.last_input_time
        if self.last_input_time != 0 and self.delta_time > self.threshold_time:
            print(self.delta_time)
            #print("threshold threshed")
            if len(self.points) > 10:
                result = recognizer.recognize(self.points)
                self.open_window(result.name)
            self.last_input_time = 0
            self.delta_time = 0
            self.points.clear()
        
    def open_window(self, recognized_gesture):
        for gesture_id, gesture in enumerate(reader.gestures):
            if recognized_gesture == gesture:
                #print(reader.paths[gesture_id])
                os.system(reader.paths[gesture_id])
                return True
        return False




class MouseInputManager():

    def __init__(self) -> None:
        self.points = [] # mouse detected points
        self.input_recognized = False
    
    def get_mirrored_x(self, x):
        return PYGLET_WIN_WIDTH - x # consitensy with touchbox
    
    def mouse_is_inbounds(self, x, y, canvas_x_y_start, canvas_widht_height): # if mouse is inly in inner bounds of canvas
        if x > canvas_x_y_start + 5 and x < canvas_widht_height - 5 and y > canvas_x_y_start + 5  and y < canvas_widht_height - 5:
            return True
        return False
    
    def window_opened(self, recognized_gesture):      
        for gesture_id, gesture in enumerate(reader.gestures):
            if recognized_gesture == gesture:
                #print(reader.paths[gesture_id])
                os.system(reader.paths[gesture_id])
                return True
        return False



class UIManager():

    def __init__(self) -> None:
        self.canvas_x_y_start = 10
        self.canvas_width_height = 280
        self.shapes = []
        self._create_shapes()
        self.help_image_path = './assets/gesture_help.jpg' # what gestures are possible
        self.help_image = pyglet.image.load(self.help_image_path)
        self.header = pyglet.text.Label("mouse gesture down here:",
                                        font_name="Arial",
                                        font_size=16,
                                        x = 15,
                                        y = 300,
                                        color=(31, 32, 65, 255))
        self.input_text = pyglet.text.Label("input was too short",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 50,
                                        y = 340,
                                        color=(186, 59, 70, 255))
        self.recognition_text = pyglet.text.Label("",
                                        font_name="Arial",
                                        font_size=13,
                                        x = 50,
                                        y = 340,
                                        color=(31, 32, 65, 255))
        self.input_too_short = False # if input points were too short (wrong predictions)

    # canvas borders
    def _create_shapes(self):
        outer_border = pyglet.shapes.Rectangle(0,0,300,400,color=(255,255,255))
        inner_border = pyglet.shapes.Rectangle(self.canvas_x_y_start,self.canvas_x_y_start,
                                               self.canvas_width_height,self.canvas_width_height,
                                               color=(105, 103, 115))
        self.shapes.append(outer_border)
        self.shapes.append(inner_border)

    # draws all ui elements
    def _draw(self):
        self.help_image.blit(300,0,0)
        for shape in self.shapes:
            shape.draw()
        self.header.draw()

    # if input points are too short -> some information for user
    def _draw_short_input(self):
        self.input_text.draw()


class TextFileReader():
    
    def __init__(self) -> None:
        self.file = open('applications.txt')
        self.gestures = []
        self.paths = []
        self._get_user_paths()

    def _get_user_paths(self):
        split_file = []
        for line in self.file:
            split_line = line.split(", ")
            split_file.append(split_line)
        
        for line in split_file:
            self.gestures.append(line[0])
            strip_path = line[1].rstrip('\n')
            self.paths.append(strip_path)
        #print(self.gestures, self.paths)



reader = TextFileReader()
recognizer = DollarRecognizer()
window = pyglet.window.Window(PYGLET_WIN_WIDTH, PYGLET_WIN_HEIGHT)
input_mng = InputManager()
mouse_mng = MouseInputManager()
ui_mng = UIManager()



@window.event
def on_mouse_press(x,y,button,modifier):
    ui_mng.input_too_short = False
    ui_mng.recognition_text.text = ""
    if mouse_mng.mouse_is_inbounds(x, y, ui_mng.canvas_x_y_start, ui_mng.canvas_width_height):
        mouse_mng.points.append(Point(x, y))

@window.event
def on_mouse_drag(x,y,dx,dy,buttins,modifiers):
    if mouse_mng.mouse_is_inbounds(x, y, ui_mng.canvas_x_y_start, ui_mng.canvas_width_height):
        mouse_mng.points.append(Point(x, y))

@window.event
def on_mouse_release(x,y,button,modifiers):
    if len(mouse_mng.points) > MIN_RECORDED_MOUSE_NUMS:
        result = recognizer.recognize(mouse_mng.points)
        mouse_mng.input_recognized = mouse_mng.window_opened(result.name)
        if not mouse_mng.input_recognized:
            ui_mng.recognition_text.text = "input not recognized"
        else:
            ui_mng.recognition_text.text = "input recognized"
    else:
        ui_mng.input_too_short = True
    mouse_mng.points.clear()

@window.event
def on_draw():
    window.clear()
    ui_mng._draw()
    for point in mouse_mng.points:
        circle = pyglet.shapes.Circle(point.x, point.y, 5, color=(237, 155, 64))
        circle.draw()
    if ui_mng.input_too_short:
        ui_mng._draw_short_input()
    if not mouse_mng.input_recognized and not ui_mng.input_too_short:
            ui_mng.recognition_text.draw()
    elif mouse_mng.input_recognized and not ui_mng.input_too_short:
            ui_mng.recognition_text.draw()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Arguments for specifying image extraction')

    parser.add_argument('-in', '--input', type=int, help='0 = touchbox, 1 = mouse')

    args = parser.parse_args()

    if args:
        if args.input == 0:
            print("0")
            while True:
                input_mng.check_time()
        else:
            print("1")
            pyglet.app.run()

    else:
        print("please parse which input device you choose: 0 = touchbox, 1 = mouse")
        sys.exit()