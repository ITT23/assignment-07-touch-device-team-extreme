#from recognizer import DollarRecognizer, Point
import os
import pyglet
from dollarpy import Recognizer, Template, Point
from DIPPID import SensorUDP
import time
import argparse
import sys

PYGLET_WIN_WIDTH = 500
PYGLET_WIN_HEIGHT = 400
MIN_RECORDED_MOUSE_NUMS = 20

class RecognizerManager():

    def __init__(self) -> None:
        self.templ_circle = Template("circle", [Point(127,141),Point(124,140),Point(120,139),Point(118,139),Point(116,139),Point(111,140),Point(109,141),
                                                Point(104,144),Point(100,147),Point(96,152),Point(93,157),Point(90,163),Point(87,169),Point(85,175),Point(83,181),
                                                Point(82,190),Point(82,195),Point(83,200),Point(84,205),Point(88,213),Point(91,216),Point(96,219),Point(103,222),
                                                Point(108,224),Point(111,224),Point(120,224),Point(133,223),Point(142,222),Point(152,218),Point(160,214),
                                                Point(167,210),Point(173,204),Point(178,198),Point(179,196),Point(182,188),Point(182,177),Point(178,167),
                                                Point(170,150),Point(163,138),Point(152,130),Point(143,129),Point(140,131),Point(129,136),Point(126,139)]);
        self.templ_star = Template("star", [Point(75,250),Point(75,247),Point(77,244),Point(78,242),Point(79,239),Point(80,237),Point(82,234),Point(82,232),
                                             Point(84,229),Point(85,225),Point(87,222),Point(88,219),Point(89,216),Point(91,212),Point(92,208),Point(94,204),
                                             Point(95,201),Point(96,196),Point(97,194),Point(98,191),Point(100,185),Point(102,178),Point(104,173),Point(104,171),
                                             Point(105,164),Point(106,158),Point(107,156),Point(107,152),Point(108,145),Point(109,141),Point(110,139),Point(112,133),
                                             Point(113,131),Point(116,127),Point(117,125),Point(119,122),Point(121,121),Point(123,120),Point(125,122),Point(125,125),
                                             Point(127,130),Point(128,133),Point(131,143),Point(136,153),Point(140,163),Point(144,172),Point(145,175),Point(151,189),
                                             Point(156,201),Point(161,213),Point(166,225),Point(169,233),Point(171,236),Point(174,243),Point(177,247),Point(178,249),
                                             Point(179,251),Point(180,253),Point(180,255),Point(179,257),Point(177,257),Point(174,255),Point(169,250),Point(164,247),
                                             Point(160,245),Point(149,238),Point(138,230),Point(127,221),Point(124,220),Point(112,212),Point(110,210),Point(96,201),
                                             Point(84,195),Point(74,190),Point(64,182),Point(55,175),Point(51,172),Point(49,170),Point(51,169),Point(56,169),
                                             Point(66,169),Point(78,168),Point(92,166),Point(107,164),Point(123,161),Point(140,162),Point(156,162),Point(171,160),
                                             Point(173,160),Point(186,160),Point(195,160),Point(198,161),Point(203,163),Point(208,163),Point(206,164),Point(200,167),
                                             Point(187,172),Point(174,179),Point(172,181),Point(153,192),Point(137,201),Point(123,211),Point(112,220),Point(99,229),
                                             Point(90,237),Point(80,244),Point(73,250),Point(69,254),Point(69,252)]);
        self.templ_caret = Template("caret", [Point(79,245),Point(79,242),Point(79,239),Point(80,237),Point(80,234),Point(81,232),Point(82,230),Point(84,224),
                                              Point(86,220),Point(86,218),Point(87,216),Point(88,213),Point(90,207),Point(91,202),Point(92,200),Point(93,194),
                                              Point(94,192),Point(96,189),Point(97,186),Point(100,179),Point(102,173),Point(105,165),Point(107,160),Point(109,158),
                                              Point(112,151),Point(115,144),Point(117,139),Point(119,136),Point(119,134),Point(120,132),Point(121,129),Point(122,127),
                                              Point(124,125),Point(126,124),Point(129,125),Point(131,127),Point(132,130),Point(136,139),Point(141,154),Point(145,166),
                                              Point(151,182),Point(156,193),Point(157,196),Point(161,209),Point(162,211),Point(167,223),Point(169,229),Point(170,231),
                                              Point(173,237),Point(176,242),Point(177,244),Point(179,250),Point(181,255),Point(182,257)]);
        self.recognizer = Recognizer([self.templ_circle, self.templ_caret, self.templ_star])
       
        

# DIPPID input
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
        
    # recognition only starts after a second of no input 
    # prevents recognition of every single touch/hover point
    def check_time(self):
        self.delta_time = time.time() - self.last_input_time
        if self.last_input_time != 0 and self.delta_time > self.threshold_time:
            #print(self.delta_time)
            if len(self.points) > 10:
                #result = recognizer.recognize(self.points)
                result = recognizer.recognizer.recognize(self.points)
                self.open_window(result[0])
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



# Mouse gesture recognition
class MouseInputManager():

    def __init__(self) -> None:
        self.points = [] # mouse detected points
        self.input_recognized = False
    
    def get_mirrored_x(self, x):
        return PYGLET_WIN_WIDTH - x # consitensy with touchbox
    
    def mouse_is_inbounds(self, x, y, canvas_x_y_start, canvas_widht_height): # if mouse is only in inner bounds of canvas
        if x > canvas_x_y_start + 5 and x < canvas_widht_height - 5 and y > canvas_x_y_start + 5  and y < canvas_widht_height - 5:
            return True
        return False
    
    def window_opened(self, recognized_gesture):      
        for gesture_id, gesture in enumerate(reader.gestures):
            if recognized_gesture == gesture:
                os.system(reader.paths[gesture_id])
                return True
        return False


# pyglet window ui 
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
recognizer = RecognizerManager()
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
        #result = recognizer.recognize(mouse_mng.points)
        result = recognizer.recognizer.recognize(mouse_mng.points)
        mouse_mng.input_recognized = mouse_mng.window_opened(result[0])
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

    if args.input == 0:
        window.set_visible(False)
        while True:
            input_mng.check_time()
    elif args.input == 1:
        pyglet.app.run()
    else:
        print("please parse which input device you choose: 0 = touchbox, 1 = mouse")
        sys.exit(0)