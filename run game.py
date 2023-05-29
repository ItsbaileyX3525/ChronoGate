from ursina import *
from ursina.prefabs.first_person_controller import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HitPoints = 100
        self.CurrentEquiped = 'TimeStop'
        self.ManaPoints = 20
        self.Spells = ['TimeStop', ]
        self.Timestop = TimeStop()
    
    def UseMana(self, amount):
        if amount>self.ManaPoints:
            print("Not enough mana!")
            return False
        elif amount<=self.ManaPoints:
            self.ManaPoints -= amount
            print("Used mana")
            return True
    
    def UseMagic(self):
        if self.CurrentEquiped == 'TimeStop' and 'TimeStop' in self.Spells:
            self.Timestop.Activate()
        
    def input(self, key):
        if key=='e':
            self.UseMagic()
            print("Used magic")
    
    def update(self):
        if self.HitPoints <= 0:
            print("Dead")

class TimeStop(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.TimestopAudio=Audio('assets/audio/spells/TimeStop/timestop.ogg',autoplay=False,loop=False,volume=1)
        self.ClockTickingAudio=Audio('assets/audio/spells/TimeStop/ClockTicking.ogg',autoplay=False,loop=False,volume=1)
        self.TimeresumeAudio=Audio('assets/audio/spells/TimeStop/timeresume.ogg',autoplay=False,loop=False,volume=1)
        self.TsTimer = 0
        self.TsTimerActive = False
        self.canRun = True
        self.TsCooldown = 0
        self.TsCooldownTimer = False
    
    def Activate(self):
        if self.canRun:
            EnoughMana=player.UseMana(amount=10)
            if EnoughMana:
                if not self.TimestopAudio.playing:
                    self.TimestopAudio.play()
                else:
                    pass
                self.TsTimerActive = True
                self.canRun = False
                print(f"Remaining mana: {player.ManaPoints}")
            elif not EnoughMana:
                print("Not enough mana")
                pass

    def pauseTime(self):
        pass
    
    def resumeTime(self):
        self.TimeresumeAudio.play()
    
    def update(self):
        if self.TsTimerActive:
            self.TsTimer += time.dt
        if self.TsTimer >= 2:
            if not self.ClockTickingAudio.playing:
                self.ClockTickingAudio.play()
        if self.TsTimer >= 7:
            self.TsTimerActive = False
            self.TsTimer = 0
            self.resumeTime()
        
        if self.TsCooldownTimer:
            self.TsCooldown += time.dt
        if self.TsCooldown >= 50:
            self.canRun = True

window.title = "Generic magic game"
app=Ursina(borderless=False,vsync=60)
with open("pyfiles/Scripts/Functions.py", "r") as f:
    exec(f.read())

ground=Entity(model='plane',scale=100,texture='grass',texture_scale=(32,32),collider='box')
player=Player()
playerController=FirstPersonController()
app.run()