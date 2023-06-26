import pyglet
import os
import numpy as np


class ImageBoard:
    def __init__(self) -> None:
        self.images = []
        stairs_img = pyglet.resource.image(os.path.normpath('img/stairs.jpg'))
        tables_img = pyglet.resource.image(os.path.normpath('img/tables.jpg'))
        windows_img = pyglet.resource.image(os.path.normpath('img/windows.jpg'))
        self.stairs= pyglet.sprite.Sprite(x=0, img=stairs_img)
        self.tables = pyglet.sprite.Sprite(x=300, img=tables_img)
        self.windows = pyglet.sprite.Sprite(x=600, img=windows_img)
        self.stairs.scale = 0.25
        self.tables.scale = 0.25
        self.windows.scale = 0.25

    def move(self, x: int, y: int, dx: int, dy: int):
        target_sprite = self.find_target(x, y)
        if not target_sprite:
            return
        target_sprite.x += dx
        target_sprite.y += dy

    def scale(self, x: int, y: int, dx: int, dy: int):
        # TODO: mit abstände machen
        target_sprite = self.find_target(x, y)
        if not target_sprite:
            return
        center = self.get_center(target_sprite)
        vector_drag_to_center = [(center[0] - x), (center[1] - y)]
        vector_movement = [dx, dy]
        dot_product = np.dot(vector_drag_to_center, vector_movement)
        if dot_product > 0:
            # towards -> scale down
            print("scale down")
            target_sprite.scale -= 0.001
        else:
            # away -> scale up
            print("scale up")
            target_sprite.scale += 0.001

    # TODO: only rotate if dx, dy unverändert, ansonsten check scale
    def rotate(self, x: int, y: int, dx: int, dy: int) -> bool:
        target_sprite = self.find_target(x, y)
        if not target_sprite:
            return
        center = self.get_center(target_sprite)
        if (x < center[0]):
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate gegen den uhrzeigersinn")
                target_sprite.rotation -= 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate im uhrzeigersinn")
                target_sprite.rotation += 1
            #target_sprite.rotation += 1
        else:
            if (dx > 0 and dy > 0) or (dx > 0 and dy < 0): 
                print("rotate im uhrzeigersinn")
                target_sprite.rotation += 1
            elif (dx < 0 and dy > 0) or (dx < 0 and dy < 0):
                print("rotate gegen den uhrzeigersinn")
                target_sprite.rotation -= 1
            #target_sprite.rotation -= 1
    

    def get_center(self, target_sprite) -> tuple:
        cx1 = target_sprite.x
        cx2 = target_sprite.x + target_sprite.width
        cy1 = target_sprite.y
        cy2 = target_sprite.y + target_sprite.height
        return ((cx1 + cx2) / 2, (cy1 + cy2) / 2)



    def find_target(self, x: int, y: int):
        if x >= self.stairs.x and x <= (self.stairs.x + self.stairs.width) and y >= self.stairs.y and y <= (self.stairs.y + self.stairs.height):
            return self.stairs
        elif x >= self.tables.x and x <= (self.tables.x + self.tables.width) and y >= self.tables.y and y <= (self.tables.y + self.tables.height):
            return self.tables
        elif x >= self.windows.x and x <= (self.windows.x + self.windows.width) and y >= self.windows.y and y <= (self.windows.y + self.windows.height):
            return self.windows
        
    def draw(self):
        self.stairs.draw()
        self.tables.draw()
        self.windows.draw()
