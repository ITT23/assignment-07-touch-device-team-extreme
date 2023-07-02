import pyglet
import os
import math
import random
import numpy as np


COLOR_HOVER = (156, 0, 75)
COLOR_TOUCH = (0, 255, 0)


class ImageBoard:
    def __init__(self, window_w, window_h, fingers) -> None:
        self.win_w = window_w
        self.win_h = window_h
        self.max_fingers_detected = fingers
        self.images = self.read_images()
        self.cursors = self.init_cursors()

    def init_cursors(self):
        """
        the system detects a maximum of five fingers on the screen
        """
        cursors = []
        for i in range(0, self.max_fingers_detected):
            detected_finger = dict()
            detected_finger['point_of_input'] = pyglet.shapes.Circle(-5, -5, 7, color=COLOR_HOVER)
            detected_finger['delta'] = [None, None]
            detected_finger['target'] = None
            detected_finger['input_type'] = None
            cursors.append(detected_finger)
        return cursors

    def read_images(self):
        images = dict()
        num_images = len(os.listdir(os.path.normpath('img')))
        for i, filename in enumerate(os.listdir(os.path.normpath('img'))):
            img = pyglet.resource.image(f'img/{filename}')
            # set anchor to rotate images towards its center
            img.anchor_x = img.width // 2  
            img.anchor_y = img.height // 2
            img_sprite = pyglet.sprite.Sprite(x=i * (self.win_w / num_images), y=i * (self.win_h / num_images), img=img)
            # random size and orientation
            img_sprite.scale = random.randint(3, 5) / 10
            img_sprite.rotation = random.randint(0, 360)
            img_sprite.x += img_sprite.width / 2
            img_sprite.y += img_sprite.height / 2
            images[img_sprite] = []
        return images

    def angle_between(self, vector1, vector2):
        """
        get angle between two vectors
        """
        v1_normalized = vector1 / np.linalg.norm(vector1)
        v2_normalized = vector2 / np.linalg.norm(vector2)
        minor = np.linalg.det(np.stack((v1_normalized[-2:], v2_normalized[-2:])))
        if minor == 0:
            return 0
        return np.sign(minor) * np.arccos(np.clip(np.dot(v1_normalized, v2_normalized), -1.0, 1.0))
    
    def get_center(self, target_sprite) -> tuple:
        """
        get center of sprite
        """
        cx1 = target_sprite.x
        cx2 = target_sprite.x + target_sprite.width
        cy1 = target_sprite.y
        cy2 = target_sprite.y + target_sprite.height
        return ((cx1 + cx2) / 2, (cy1 + cy2) / 2)

    def find_target(self, cursor):
        """
        find cursor's underlying target sprite
        """
        x = cursor['point_of_input'].x
        y = cursor['point_of_input'].y
        visible = cursor['point_of_input'].visible
        for sprite in self.images:
            if visible and x >= sprite.x - sprite.width/2 and x <= (sprite.x + sprite.width/2) and y >= sprite.y - sprite.height / 2 and y <= (sprite.y + sprite.height/2):
                self.images[sprite].append(cursor)
                return sprite
    

    '''----------------------------------------------------------------------'''


    def rotate_sprite(self, sprite, x_before, y_before, x_after, y_after):
        """
        rotate sprite based on angle between vector before-to-center and after-to-center of finger position
        """
        center = self.get_center(sprite)
        vector_to_center_before = [(center[0] - x_before), (center[1] - y_before)]
        vector_to_center_after = [(center[0] - x_after), (center[1] - y_after)]
        angle = self.angle_between(vector_to_center_before, vector_to_center_after)
        sprite.rotation += math.degrees(angle)

    def move_sprite(self, sprite, delta):
        """
        move sprite based on delta finger position
        caution: if delta is high, the finger recognizer swapped fingers, ignore this for movement 
        """
        if delta[0] and delta[1] and abs(delta[0]) < 75 and abs(delta[1]) < 75:
            sprite.x += delta[0]
            sprite.y += delta[1]
        
    def scale_sprite(self, sprite, x_before, y_before, x_after, y_after):
        """
        scale sprite based on ratio between vector magnitude of before-to-center and after-to-center of finger position
        """
        center = self.get_center(sprite)
        vector_to_center_before = [(center[0] - x_before), (center[1] - y_before)]
        vector_to_center_after = [(center[0] - x_after), (center[1] - y_after)]
        len_before = math.sqrt(sum(i**2 for i in vector_to_center_before))
        len_after = math.sqrt(sum(i**2 for i in vector_to_center_after))
        scale_factor = len_after / len_before
        sprite.scale *= scale_factor


    '''----------------------------------------------------------------------'''
 
        
    def update(self, data):
        self.update_cursors(data)
        self.update_images()
        
    def update_cursors(self, data):
        for i in range(0, self.max_fingers_detected):
            finger_id = str(i)
            try:
                # set finger's new coordinates, delta of movement, input type and target sprite
                finger_caps = data[finger_id]
                x = finger_caps['x'] * self.win_w
                y = finger_caps['y'] * self.win_h
                dx = x - self.cursors[int(finger_id)]['point_of_input'].x
                dy = y - self.cursors[int(finger_id)]['point_of_input'].y

                self.cursors[int(finger_id)]['delta'][0] = dx
                self.cursors[int(finger_id)]['delta'][1] = dy
                self.cursors[int(finger_id)]['input_type'] = finger_caps['type']
                self.cursors[int(finger_id)]['point_of_input'].visible = True
                self.cursors[int(finger_id)]['point_of_input'].color = COLOR_TOUCH if finger_caps['type'] == 'touch' else COLOR_HOVER
                self.cursors[int(finger_id)]['point_of_input'].x = x
                self.cursors[int(finger_id)]['point_of_input'].y = y
                self.cursors[int(finger_id)]['target'] = self.find_target(self.cursors[int(finger_id)])
            except:
                # if no finger detected, set cursor point invisible
                self.cursors[int(finger_id)]['point_of_input'].visible = False
                continue
        
    def update_images(self):
        """
        update sprites based on touch input:
        if there is one touching finger on a sprite, move it
        if there are two touching fingers on a sprite, scale and/or rotate it
        """
        for sprite, cursors_on_image in self.images.items():
            if len(cursors_on_image) == 1 and cursors_on_image[0]['input_type'] == 'touch':
                self.move_sprite(sprite, cursors_on_image[0]['delta'])
            elif len(cursors_on_image) == 2 and cursors_on_image[0]['input_type'] == 'touch' and cursors_on_image[1]['input_type'] == 'touch':
                hovering_cursor = cursors_on_image[0] 
                x_after = hovering_cursor['point_of_input'].x
                y_after= hovering_cursor['point_of_input'].y
                x_before = x_after - hovering_cursor['delta'][0]
                y_before = y_after - hovering_cursor['delta'][1]
                self.rotate_sprite(sprite, x_before, y_before, x_after, y_after)
                self.scale_sprite(sprite, x_before, y_before, x_after, y_after)
        
    def draw(self):
        for sprite in self.images:
            sprite.draw()
            self.images[sprite] = []
        for cursor in self.cursors:
            cursor['point_of_input'].draw()

