from ursina import *

class TSEffect(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Bubbles = []
        self.to_be_destroyed = []
        self.Bubble1 = Entity(model='circle',color=color.gray,alpha=.32,scale=.3)
        self.Bubble2 = Entity(model='circle',color=color.gray,alpha=.32,scale=.2)
        self.Bubble3 = Entity(model='circle',color=color.gray,alpha=.32,scale=.1)
        self.Bubbles.append(self.Bubble1)
        self.Bubbles.append(self.Bubble2)
        self.Bubbles.append(self.Bubble3)
    
    def update(self):
        for e in self.Bubbles:
            e.scale += Vec3(0.1, 0.1, 0.1) * 3
            if e.scale_x >= 12:
                self.Bubbles.remove(e)
                self.to_be_destroyed.append(e)
        for e in self.to_be_destroyed:
            destroy(e)

        self.to_be_destroyed.clear()
app = Ursina()

Tseffect=TSEffect()

app.run()
