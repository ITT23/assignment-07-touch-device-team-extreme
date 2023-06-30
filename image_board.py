import pyglet
import os
import math
import numpy as np


COLOR_HOVER = (156, 0, 75)
COLOR_TOUCH = (0, 255, 0)
MAX_NUM_FINGERS_DETECTED = 5


class ImageBoard:
    def __init__(self, window_w, window_h) -> None:
        self.win_w = window_w
        self.win_h = window_h
        self.images = self.read_images()
        self.cursors = self.init_cursors()

    def init_cursors(self):
        cursors = []
        for i in range(0, MAX_NUM_FINGERS_DETECTED):
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
            #img.anchor_x = img.width / 2
            #img.anchor_y = img.height / 2
            img_sprite = pyglet.sprite.Sprite(x=i * (self.win_w / num_images), y=i * (self.win_h / num_images), img=img)
            img_sprite.scale = 0.3
            #img_sprite.anchor_x = img_sprite.width // 2
            #img_sprite.anchor_y = img_sprite.height // 2
            images[img_sprite] = []
        return images
    


    def unit_vector(self, vector):
        """ Returns the unit vector of the vector"""
        return vector / np.linalg.norm(vector)

    def angle_between(self, vector1, vector2):
        """ Returns the angle in radians between given vectors"""
        v1_u = self.unit_vector(vector1)
        v2_u = self.unit_vector(vector2)
        minor = np.linalg.det(
            np.stack((v1_u[-2:], v2_u[-2:]))
        )
        if minor == 0:
            return 0
        return np.sign(minor) * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    

    def rotate_by_angle(self, sprite, x_before, y_before, x_after, y_after):
        center = self.get_center(sprite)
        vector_to_center_before = [(center[0] - x_before), (center[1] - y_before)]
        vector_to_center_after = [(center[0] - x_after), (center[1] - y_after)]
        angle = self.angle_between(vector_to_center_before, vector_to_center_after)
        sprite.rotation += math.degrees(angle)

    def move_sprite(self, sprite, delta):
        if delta:
            sprite.x += delta[0]
            sprite.y += delta[1]

    def scale_calculated(self, sprite, x_before, y_before, x_after, y_after):
        center = self.get_center(sprite)
        vector_to_center_before = [(center[0] - x_before), (center[1] - y_before)]
        vector_to_center_after = [(center[0] - x_after), (center[1] - y_after)]
        len_before = math.sqrt(sum(i**2 for i in vector_to_center_before))
        len_after = math.sqrt(sum(i**2 for i in vector_to_center_after))
        scale_factor = len_after / len_before
        sprite.scale *= scale_factor


    def get_center(self, target_sprite) -> tuple:
        cx1 = target_sprite.x
        cx2 = target_sprite.x + target_sprite.width
        cy1 = target_sprite.y
        cy2 = target_sprite.y + target_sprite.height
        return ((cx1 + cx2) / 2, (cy1 + cy2) / 2)


    def find_target(self, cursor):
        x = cursor['point_of_input'].x
        y = cursor['point_of_input'].y
        visible = cursor['point_of_input'].visible
        for sprite in self.images:
            if visible and x >= sprite.x and x <= (sprite.x + sprite.width) and y >= sprite.y and y <= (sprite.y + sprite.height):
                self.images[sprite].append(cursor)
                return sprite
        

    def update(self, data):
        self.update_cursors(data)
        self.update_images()
        
        
    def update_cursors(self, data):
        if(data):
            print(len(data))
        for i in range(0, MAX_NUM_FINGERS_DETECTED):
            finger_id = str(i)
            try:
                finger_caps = data[finger_id]
                x = finger_caps['x'] * self.win_w
                y = finger_caps['y'] * self.win_h
                dx = x - self.cursors[int(finger_id)]['point_of_input'].x
                dy = y - self.cursors[int(finger_id)]['point_of_input'].y

                #print(abs(dx))


                if ((abs(dx) > 75 and not self.cursors[int(finger_id)]['delta'][0]) or abs(dx) <= 75) and ((abs(dy) > 75 and not self.cursors[int(finger_id)]['delta'][1]) or abs(dy) <= 75):
                    self.cursors[int(finger_id)]['delta'][0] = dx
                    self.cursors[int(finger_id)]['delta'][1] = dy


                # if ((self.cursors[int(finger_id)]['delta'][0] and (math.abs(dx) <= 150)) or not self.cursors[int(finger_id)]['delta'][0]):
                #     self.cursors[int(finger_id)]['delta'][0] = dx
                # if ((self.cursors[int(finger_id)]['delta'][1] and (math.abs(dy) <= 150)) or not self.cursors[int(finger_id)]['delta'][1]):
                #     self.cursors[int(finger_id)]['delta'][1] = dy

                self.cursors[int(finger_id)]['input_type'] = finger_caps['type']
                self.cursors[int(finger_id)]['point_of_input'].visible = True
                self.cursors[int(finger_id)]['point_of_input'].color = COLOR_TOUCH if finger_caps['type'] == 'touch' else COLOR_HOVER
                self.cursors[int(finger_id)]['point_of_input'].x = x
                self.cursors[int(finger_id)]['point_of_input'].y = y
                self.cursors[int(finger_id)]['target'] = self.find_target(self.cursors[int(finger_id)])
            except:
                self.cursors[int(finger_id)]['point_of_input'].visible = False
                continue
        

    def update_images(self):
        for sprite, cursors_on_image in self.images.items():
            if len(cursors_on_image) == 1 and cursors_on_image[0]['input_type'] == 'touch':
                self.move_sprite(sprite, cursors_on_image[0]['delta'])
                
            elif len(cursors_on_image) == 2:
                #if cursors_on_image[0]['input_type'] != cursors_on_image[1]['input_type']:
                hovering_cursor = cursors_on_image[0] #if cursors_on_image[0]['input_type'] == 'hover' else cursors_on_image[1]
                x_after = hovering_cursor['point_of_input'].x
                y_after= hovering_cursor['point_of_input'].y
               
                x_before = x_after - hovering_cursor['delta'][0]
                y_before = y_after - hovering_cursor['delta'][1]
                self.rotate_by_angle(sprite, x_before, y_before, x_after, y_after)
                self.scale_calculated(sprite, x_before, y_before, x_after, y_after)
                #sprite.anchor_x = sprite.width // 2
                #sprite.anchor_y = sprite.height // 2
                # if cursors_on_image[0]['input_type'] != cursors_on_image[1]['input_type']:
                #     rotating_cursor = cursors_on_image[0] if cursors_on_image[0]['input_type'] == 'hover' else cursors_on_image[1]
                #     self.rotate_sprite(sprite, rotating_cursor['delta'], rotating_cursor['point_of_input'].y)
                # elif cursors_on_image[0]['input_type'] == cursors_on_image[1]['input_type'] and cursors_on_image[0]['input_type'] == 'touch':
                #     x1 = cursors_on_image[0]['point_of_input'].x
                #     y1= cursors_on_image[0]['point_of_input'].y
                #     dx1 = cursors_on_image[0]['delta'][0]
                #     dy1 = cursors_on_image[0]['delta'][1]
                #     x2 = cursors_on_image[1]['point_of_input'].x
                #     y2= cursors_on_image[1]['point_of_input'].y
                #     dx2 = cursors_on_image [1]['delta'][0]
                #     dy2 = cursors_on_image[1]['delta'][1]
                #     self.scale_sprite(sprite, x1, y1, x2, y2, dx1, dy1, dx2, dy2)


    def draw(self):
        for sprite in self.images:
            sprite.draw()
            self.images[sprite] = []
        for cursor in self.cursors:
            cursor['point_of_input'].draw()

#####################################################################################

    def rotate_sprite(self, sprite, delta, y):
        dx = delta[0]
        dy = delta[1]
        center = self.get_center(sprite)
        if (y < center[1]):
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate gegen den uhrzeigersinn")
                sprite.rotation -= 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate im uhrzeigersinn")
                sprite.rotation += 1
        else:
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate im uhrzeigersinn")
                sprite.rotation += 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate gegen den uhrzeigersinn")
                sprite.rotation -= 1



    def move(self, x: int, y: int, dx: int, dy: int):
        target_sprite = self.find_target(x, y)
        if not target_sprite:
            return
        target_sprite.x += dx
        target_sprite.y += dy


            # TODO: only rotate if dx, dy unverändert, ansonsten check scale
    def rotate(self, x: int, y: int, dx: int, dy: int) -> bool:
        target_sprite = self.find_target(x, y)
        if not target_sprite:
            return
        center = self.get_center(target_sprite)
        if (y < center[1]):
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate gegen den uhrzeigersinn")
                target_sprite.rotation -= 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate im uhrzeigersinn")
                target_sprite.rotation += 1
        else:
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate im uhrzeigersinn")
                target_sprite.rotation += 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate gegen den uhrzeigersinn")
                target_sprite.rotation -= 1



    def scale(self, x1: int, y1: int, x2: int, y2: int, dx1: int, dy1: int, dx2: int, dy2: int):
        target_sprite1 = self.find_target(x1, y1)
        target_sprite2 = self.find_target(x2, y2)
        if not target_sprite1 or not target_sprite2 or target_sprite1 != target_sprite2:
            return
        
        center = self.get_center(target_sprite1)
        vector_drag_to_center1 = [(center[0] - x1), (center[1] - y1)]
        vector_movement1 = [dx1, dy1]
        dot_product1 = np.dot(vector_drag_to_center1, vector_movement1)
        vector_drag_to_center2 = [(center[0] - x2), (center[1] - y2)]
        vector_movement2 = [dx2, dy2]
        dot_product2 = np.dot(vector_drag_to_center2, vector_movement2)

        if dot_product1 > 0 and dot_product2 > 0:
            # towards -> scale down
            print("scale down")
            target_sprite1.scale -= 0.05
        elif dot_product1 < 0 and dot_product2 < 0:
            # away -> scale up
            print("scale up")
            target_sprite1.scale += 0.05


    def scale_sprite(self, sprite, x1: int, y1: int, x2: int, y2: int, dx1: int, dy1: int, dx2: int, dy2: int):
        center = self.get_center(sprite)
        vector_drag_to_center1 = [(center[0] - x1), (center[1] - y1)]
        vector_movement1 = [dx1, dy1]
        dot_product1 = np.dot(vector_drag_to_center1, vector_movement1)
        vector_drag_to_center2 = [(center[0] - x2), (center[1] - y2)]
        vector_movement2 = [dx2, dy2]
        dot_product2 = np.dot(vector_drag_to_center2, vector_movement2)

        if dot_product1 > 0 and dot_product2 > 0:
            # towards -> scale down
            print("scale down")
            sprite.scale -= 0.05
        elif dot_product1 < 0 and dot_product2 < 0:
            # away -> scale up
            print("scale up")
            sprite.scale += 0.05

