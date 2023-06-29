from recognizer import DollarRecognizer, Point
import os
import pyglet
from DIPPID import SensorUDP
import time

class InputManager():

    def __init__(self) -> None:
        self.PORT = 5700
        self.sensor = SensorUDP(self.PORT)
        self.sensor.register_callback('events', self.handle_callback)
        self.points = []
        self.last_input_time = 0
        self.delta_time = 0
        self.threshold_time = 1 # ms

    def handle_callback(self, data):
        for finger_id, value in data.items():
            type = value['type']
            x = value['x']
            y = value['y']
            self.points.append(Point(x,y))
            if self.last_input_time == 0:
                self.last_input_time = time.time()
        
    def check_time(self):
        self.delta_time = time.time() - self.last_input_time
        if self.last_input_time != 0 and self.delta_time > self.threshold_time:
            print("threshold threshed")
            if len(self.points) > 10:
                result = recognizer.recognize(self.points)
                print(result.name)
                self.open_window(result.name)
            self.last_input_time = 0
            self.delta_time = 0
            self.points.clear()
    
    def open_window(self, gesture):
        
        if gesture == 'circle':
            os.system('firefox') # other linux: /usr/bin/firefox 
        elif gesture == 'caret':
            os.sytem('blender')
        elif gesture == 'left_sq_bracket':
            os.system('gimp')

recognizer = DollarRecognizer()
input_man = InputManager()

if __name__ == "__main__":
    while True:

        input_man.check_time()