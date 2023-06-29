import pyglet
import os
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
            detected_finger['point_of_input'] = pyglet.shapes.Circle(0, 0, 7, color=COLOR_HOVER)
            detected_finger['delta'] = [0, 0]
            detected_finger['target'] = None
            detected_finger['input_type'] = None
            cursors.append(detected_finger)
        return cursors

    def read_images(self):
        images = dict()
        num_images = len(os.listdir(os.path.normpath('img')))
        for i, filename in enumerate(os.listdir(os.path.normpath('img'))):
            img = pyglet.resource.image(f'img/{filename}')
            img_sprite = pyglet.sprite.Sprite(x=i * (self.win_w / num_images), y=i * (self.win_h / num_images), img=img)
            img_sprite.scale = 0.3
            images[img_sprite] = []
        return images



    def move_sprite(self, sprite, delta):
        print(sprite)
        print(delta)
        sprite.x += delta[0]
        sprite.y += delta[1]


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
    

    def get_center(self, target_sprite) -> tuple:
        cx1 = target_sprite.x
        cx2 = target_sprite.x + target_sprite.width
        cy1 = target_sprite.y
        cy2 = target_sprite.y + target_sprite.height
        return ((cx1 + cx2) / 2, (cy1 + cy2) / 2)



    def find_target(self, cursor):
        x = cursor['point_of_input'].x
        y = cursor['point_of_input'].y
        for sprite in self.images:
            if x >= sprite.x and x <= (sprite.x + sprite.width) and y >= sprite.y and y <= (sprite.y + sprite.height):
                self.images[sprite].append(cursor)
                return sprite
        

    def update(self, data):
        self.update_cursors(data)
        self.update_images()
        
        
    def update_cursors(self, data):
        self.cursors = self.cursors[:len(data)]
        for finger_id, finger_caps in data.items():
            if int(finger_id) < MAX_NUM_FINGERS_DETECTED:
                x = finger_caps['x'] * self.win_w
                y = finger_caps['y'] * self.win_h
                self.cursors[int(finger_id)]['delta'][0] = x - self.cursors[int(finger_id)]['point_of_input'].x
                self.cursors[int(finger_id)]['delta'][1] = y - self.cursors[int(finger_id)]['point_of_input'].y
                self.cursors[int(finger_id)]['input_type'] = finger_caps['type']
                self.cursors[int(finger_id)]['point_of_input'].color = COLOR_TOUCH if finger_caps['type'] == 'touch' else COLOR_HOVER
                self.cursors[int(finger_id)]['point_of_input'].x = x
                self.cursors[int(finger_id)]['point_of_input'].y = y
                self.cursors[int(finger_id)]['target'] = self.find_target(self.cursors[int(finger_id)])
        

    def update_images(self):
        for sprite, cursors_on_image in self.images.items():
            if len(cursors_on_image) == 1 and cursors_on_image[0]['input_type'] == 'touch':
                self.move_sprite(sprite, cursors_on_image[0]['delta'])
            if len(cursors_on_image) == 2:
                if cursors_on_image[0]['input_type'] != cursors_on_image[1]['input_type']:
                    rotating_cursor = cursors_on_image[0] if cursors_on_image[0]['input_type'] == 'hover' else cursors_on_image[1]
                    self.rotate_sprite(sprite, rotating_cursor['delta'], rotating_cursor['point_of_input'].y)
                #elif cursors_on_image[0]['input_type'] == cursors_on_image[1]['input_type'] and cursors_on_image[0]['input_type'] == 'touch':
                #    self.scale_sprite(sprite, )


    def draw(self):
        for sprite in self.images:
            sprite.draw()
            self.images[sprite] = []
        for cursor in self.cursors:
            cursor['point_of_input'].draw()

