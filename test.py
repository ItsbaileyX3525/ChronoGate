from ursina import *
import threading

app = Ursina(borderless=False,vsync=True)

box = Entity(model="cube", texture="white_cube", collider="box")
box.search_count = 0
prev_box = Entity(model="cube", texture="white_cube", color=color.orange, alpha=0.2, visible=False)

wall = Entity(model="cube", texture="white_cube", collider="box", scale_z=4.0, scale_y=3.0, x=5.0, alpha=0.5)

ed = EditorCamera()

speed = 5.0
#Thanks to squiggle for this example
def search():
    for _ in range(20):
        if box.hit:
            # Adjust for half width of box (move backwards in direction came from).
            # A bit more than half the width for precision reasons and stuff.
            width_back_x = box.x - 0.5001 
            if box.intersects():
                box.x = (box.prev_x + width_back_x) / 2.0 # Mid point.
            else:
                box.x = (box.prev_x + box.x) / 2.0 # Mid point.
        else:
            box.x = (box.x + box.end_x) / 2.0 # Mid point.
        prev_box.x = box.prev_x
        box.prev_x = box.x

        if box.intersects():
            box.color = color.red
        else:
            box.color = color.white

        box.search_count += 1

def input(key):
    if key == "space" and box.search_count == 0:
        box.start_x = box.x
        box.x += speed
        box.end_x = box.x
        box.prev_x = box.start_x
        if box.intersects():
            box.color = color.red
        else:
            box.color = color.white
        prev_box.visible = True
        prev_box.x = box.start_x
        search()
    if key == "r":
        box.x = box.start_x
        box.search_count = 0
        prev_box.visible = False

app.run()