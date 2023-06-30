from recognizer import DollarRecognizer, Point
import os
import pyglet
from DIPPID import SensorUDP
import time

# TODO: text file reading and automated mapping?

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
            print("threshold threshed")
            if len(self.points) > 10:
                result = recognizer.recognize(self.points)
                self.open_window(result.name)
            self.last_input_time = 0
            self.delta_time = 0
            self.points.clear()
        
    def open_window(self, gesture):
        
        if gesture == 'circle':
            #os.system('firefox') # other linux: /usr/bin/firefox 
            print('circle')
        elif gesture == 'star':
            print("star")
            #os.sytem('blender')
        elif gesture == 'caret':
            print("caret")
            #os.system('gimp')



class MouseInputManager():

    def __init__(self) -> None:
        self.points = [] # mouse detected points
        self.input_recognized = False
    
    def get_mirrored_x(self, x, width):
        return width - x # consitensy with touchbox
    
    def mouse_is_inbounds(self, x, y, canvas_x_y_start, canvas_widht_height): # if mouse is inly in inner bounds of canvas
        if x > canvas_x_y_start + 5 and x > canvas_widht_height and y > canvas_x_y_start and y < canvas_widht_height:
            return True
        return False
    
    def open_window(self, gesture):      
        if gesture == 'circle':
            #os.system('firefox') # other linux: /usr/bin/firefox 
            print('circle')
        elif gesture == 'star':
            print("star")
            #os.sytem('blender')
        elif gesture == 'caret':
            print("caret")
            #os.system('gimp')



class UIManager():

    def __init__(self) -> None:
        self.canvas_x_y_start = 10
        self.canvas_width_height = 280
        self.shapes = []
        self._create_shapes()
        self.help_image_path = './assets/input_help_task03.png' # what gestures are possible
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

        print(self.gestures, self.paths)

recognizer = DollarRecognizer()
input_mng = InputManager()
mouse_mng = MouseInputManager()
ui_mng = UIManager()
reader = TextFileReader()


#if __name__ == "__main__":

    #while True:
        #input_mng.check_time()
