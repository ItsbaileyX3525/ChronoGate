from ursina import *
from ursina.prefabs.first_person_controller import *
import threading
import random
import json

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #General player stuff
        self.HitPoints = 100
        self.ManaPoints = 20
        self.Level = 1
        self.Experience = 0
        self.ExperienceNeeded = 100
        
        #Head bobbing crap
        self.bobbing_amount = 0.1
        self.bobbing_speed = 0.1
        self.bobbing_timer = 0.0
        
        #Spells & stuff
        self.CurrentEquiped = 'FireWave'
        self.SpellEquiped = Text(text='Current spell: None',x=-.87,y=-.45)
        self.Spells = ['TimeStop', 'FireWave', ]
        self.Timestop = TimeStop()
        self.Firewave = Firewave()
        
        #Audios for the player
        self.normalFootSteps=Audio('assets/audio/player/footslow.ogg',autoplay=False,loop=False,volume=.5)
        self.sprintFootSteps=Audio('assets/audio/player/footfast.ogg',autoplay=False,loop=False,volume=.5)

        #keybinds
        with open('assets/data/controls.json') as file:
            self.data = json.load(file)

        self.a = self.data['A']
        self.b = self.data['B']
        self.c = self.data['C']
        self.d = self.data['D']
        self.e = self.data['E']
        self.f = self.data['F']
        self.g = self.data['G']
        self.h = self.data['H']
        self.i = self.data['I']
        self.j = self.data['J']
        self.k = self.data['K']
        self.l = self.data['L']
        self.m = self.data['M']
        self.n = self.data['N']
        self.o = self.data['O']
        self.p = self.data['P']
        self.q = self.data['Q']
        self.r = self.data['R']
        self.s = self.data['S']
        self.t = self.data['T']
        self.u = self.data['U']
        self.v = self.data['V']
        self.w = self.data['W']
        self.xb = self.data['X']
        self.yb = self.data['Y']
        self.zb = self.data['Z']
        self.control = self.data['Control']
        self.shift = self.data['Shift']

    def UseMana(self, amount):
        if amount>self.ManaPoints:
            return False
        elif amount<=self.ManaPoints:
            self.ManaPoints -= amount
            return True

    def UseMagic(self):
        spell_map = {
            'TimeStop': self.Timestop.Activate,
            'FireWave': self.Firewave.Activate,
        }
        if self.CurrentEquiped in spell_map and self.CurrentEquiped in self.Spells:
            spell_map[self.CurrentEquiped]()


    def OnLevelUp(self):
        self.Level += 1
        self.ExperienceNeeded *= 2

    def input(self, key):
        if key=='e':
            self.UseMagic()

    def update(self):
        if self.HitPoints <= 0:
            pass #Add death stuff here
        if any(held_keys[key] for key in ['w', 'a', 's', 'd']):
            self.bobbing_timer += self.bobbing_speed
            vertical_offset = abs(math.sin(self.bobbing_timer)) * self.bobbing_amount
            camera.y = vertical_offset

            if not self.normalFootSteps.playing:
                self.normalFootSteps.play()

            if held_keys['shift']:
                if held_keys['w']:
                    playerController.speed = 16
                    self.bobbing_speed = 0.2
                elif held_keys['s']:
                    playerController.speed = 12
                    self.bobbing_speed = 0.15
            else:
                self.sprintFootSteps.stop()
                playerController.speed = 8
                self.bobbing_speed = 0.1
        else:
            self.normalFootSteps.stop()
            self.bobbing_timer = 0.0
            camera.y = 0.0

        self.SpellEquiped.text = f'Current spell: {self.CurrentEquiped}'


class FallingText(Text):
    def __init__(self,position,text='Default Text'):
        super().__init__(ignore=False,text=text,scale=1,position=position)
        self.speed = Vec3(0, 2, 0)
        self.gravity = Vec3(0, -4.81, 0)
        self.max_swerve_speed = 1.0
        self.swerve_speed = random.uniform(-self.max_swerve_speed, self.max_swerve_speed)
        
    def update(self):
        self.speed += self.gravity * time.dt
        self.position += self.speed * time.dt
        self.position += Vec3(self.swerve_speed * time.dt, 0, 0)
        if self.y <= -9:
            destroy(self)


class TimeStop():
    def __init__(self):
        self.TimestopAudio=Audio('assets/audio/spells/TimeStop/timestop.ogg',autoplay=False,loop=False,volume=1)
        self.ClockTickingAudio=Audio('assets/audio/spells/TimeStop/ClockTicking.ogg',autoplay=False,loop=False,volume=1)
        self.TimeresumeAudio=Audio('assets/audio/spells/TimeStop/timeresume.ogg',autoplay=False,loop=False,volume=1)
        self.canRun = True
        self.enemyTimestopped = False
        self.resume=Sequence(Wait(7),Func(self.resumeTime),auto_destroy=False)
        self.ticking=Sequence(Wait(2),Func(self.ClockTickingAudio.play),auto_destroy=False)
        self.canRunAgain=Sequence(Wait(50),Func(setattr, self, 'canRun', True),auto_destroy=False)
        self.loadanims=threading.Thread(target=self.loadAnims).start()

    def loadAnims(self):
        self.e=Animation(parent=camera.ui,name='assets/textures/spells/time/ts.gif',scale=(2,1),visible=False)

    def Activate(self):
        if self.canRun:
            EnoughMana=player.UseMana(amount=10)
            if EnoughMana:
                if not self.TimestopAudio.playing:
                    self.TimestopAudio.play()
                else:
                    pass
                self.pauseTime()
            elif not EnoughMana:
                FallingText(text='Not enough mana!',position=(0,0,0))
        else:
            FallingText(text='Spell cooling down!',position=(0,0,0))

    def pauseTime(self):
        self.enemyTimestopped = True
        self.canRun = False
        self.resume.start()
        self.ticking.start()

    def resumeTime(self):
        self.enemyTimestopped = False
        self.TimeresumeAudio.play()
        self.canRunAgain.start() 
    
class Firewave(Entity):
    def __init__(self, add_to_scene_entities=False, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.model='cirlce'
        self.texture='assets/textures/spells/fire.jpg'
        self.FireballAudio = Audio('assets/audio/spells/FireShot.ogg')
        self.canRun =  True
        self.Activated = False
        self.canRunAgain=Sequence(Wait(1),Func(setattr, self, 'canRun', True),auto_destroy=False)
        self.baseDamageAmount = 12
        self.damageMultipler = 1
        
    def Activate(self):
        if self.canRun:
            EnoughMana=player.UseMana(10)
            if EnoughMana:
                if not self.FireballAudio.playing:
                    self.FireballAudio.play()
                else:
                    pass
                self.shootFirewave()
            elif not EnoughMana:
                FallingText(text='Not enough mana!',position=(0,0,0))
        else:
            FallingText(text='Spell cooling down!',position=(0,0,0))
                  
    def shootFirewave(self):
        damageAmount = self.baseDamageAmount * self.damageMultipler
        for enemy in enemyList:
            distFromPlayer=distance_2d(playerController, enemy)
            if distFromPlayer<=6:
                enemy.hitPoints -= damageAmount
            else:
                pass
        
   
    def update(self):
        pass#if self.Activated:

    
class EnemyNormal(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.hitPoints = 20
        self.mana = 0
        self.model = 'cube'
        self.color = color.red
        self.inRange = False
        self.inRangeAttack = False
        self.touchingBorder = False
        self.y = 1
        self.spells = []

    def MovementToPlayer(self):
        self.position += self.forward * time.dt

    def OnDeath(self):
        player.Experience += random.randint(1,5)
        destroy(self)

    def update(self):
        self.dist = distance(playerController.position, self.position)
        if 1.5 < self.dist < 18:
            self.inRange = True
            self.inRangeAttack = False
        elif self.dist < 1.5:
            self.inRangeAttack = True
            self.inRange = False
        elif self.dist > 18:
            self.inRange = False
            self.inRangeAttack = False
        if self.inRange and not player.Timestop.enemyTimestopped:
            self.look_at_2d(playerController.position, 'y')
            self.MovementToPlayer()
        elif self.inRangeAttack:
            if not player.Timestop.enemyTimestopped:
                self.look_at_2d(playerController.position, 'y')
                pass
        else:
            if not self.touchingBorder and not player.Timestop.enemyTimestopped:
                self.position += self.forward * time.dt * 2
        if self.hitPoints<=0:
            self.OnDeath()


window.title = "ChronoGate - Playground"

app=Ursina(borderless=False,vsync=60,development_mode=True,use_ingame_console=True,fullscreen=False)
PlayerSensitvity=(40,40)
enemyList=[]
playerController=FirstPersonController()
player=Player()
playerController.mouse_sensitivity = PlayerSensitvity
enemyList.append(EnemyNormal(x=20))
enemyList.append(EnemyNormal(x=40))
GROUND=Entity(model='plane',scale=1000,texture='grass',texture_scale=(32,32),collider='box')
Sky(texture='assets/textures/misc/sky.jpg')


def input(key):
    if held_keys['control'] and key=='h':
        window.console.text_field.enabled = not window.console.text_field.enabled
window.console.text_input = "Fuckyoubatman"
window.console.text_field.enabled = not window.console.text_field.enabled
app.run()