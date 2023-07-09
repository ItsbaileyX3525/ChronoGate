"""
This py file is used for testing out the spells before they are added to the main game!
You can still play this as you see fit, to choose a certain spell change player.CurrentEquiped to something in the
dictionary of player.Spells
"""



from ursina import *
from ursina.prefabs.first_person_controller import *
from ursina.prefabs.health_bar import HealthBar
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader
import threading
import random
import json
import glob
import random
main_directory = Path(__file__).resolve().parent

file_pattern = str(main_directory / 'assets/data/controls.json')
files = glob.glob(file_pattern)
if files:
    controlsPath = files[0]
class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35 
        self.jumping = False
        self.air_time = 0

        self.traverse_target = scene
        self.ignore_list = [self, ]

        for key, value in kwargs.items():
            setattr(self, key ,value)

        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y

    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys[playerControllerWalkW] - held_keys[playerControllerWalkS])
            + self.right * (held_keys[playerControllerWalkD] - held_keys[playerControllerWalkA])
            ).normalized()

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity

    def input(self, key):
        if key == 'space':
            self.jump()

    def jump(self):
        if not self.grounded:
            return
        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        self.air_time = 0
        self.grounded = True

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

class Player(Entity):
    def __init__(self,playerName=None, **kwargs):
        super().__init__(**kwargs)
        #General player stuff
        self.playerName = playerName

        self.HitPoints = 100
        self.MaxHitPoints = 100
        self.ManaPoints = 20
        self.MaxManaPoints = 50
        self.Level = 1
        self.Experience = 0
        self.ExperienceNeeded = 100
        
        #Head bobbing crap
        self.bobbing_amount = 0.1
        self.bobbing_speed = 0.1
        self.bobbing_timer = 0.0
        
        #Spells & stuff
        self.CurrentEquiped = 'TimeStop'
        self.SpellEquiped = Text(text='Current spell: None',x=-.87,y=-.45)
        self.Spells = ['TimeStop', 'FireWave', ]
        self.Timestop = TimeStop()
        #self.Firewave = Firewave() - Being made still
        
        #Audios for the player
        self.normalFootSteps=Audio('assets/audio/player/footslow.ogg',autoplay=False,loop=False,volume=.5)
        self.sprintFootSteps=Audio('assets/audio/player/footfast.ogg',autoplay=False,loop=False,volume=.5)

        if self.playerName is None or len(self.playerName) == 0:
            self.names=["Thistlethorn","Moonshadow","Fernbloom","Wildroot","Oakleaf","Stormcaller", "Sunflower","Rivermist","Forestsong"]
            self.playerName = random.choice(self.names)

        #Ui stuff
        UI=camera.ui
        self.backgroundHolder=Entity(parent=UI,model='quad',color=color.gray,scale=(.65,.15),x=-.45,y=.4)
        self.Name = Text(text=self.playerName,y=.46,x=-.46)
        if len(self.playerName) >= 7:
            self.Name.x=-.47
        self.profile=Entity(parent=UI,model='quad',texture='assets/textures/misc/Placeholder.png',scale=.15,y=.4,x=-.75)
        self.HealthBar = HealthBar(parent=UI,bar_color=rgb(77,255,77),x=-.65,y=.42, roundness=.5,scale=(.5,.025),max_value=self.MaxHitPoints)
        self.HealthBar.value=self.HitPoints;self.HealthBar.animation_duration=0
        self.ManaBar = HealthBar(parent=UI,bar_color=rgb(0,128,255),x=-.65,y=.38, roundness=.5,scale=(.5,.025),max_value=self.MaxManaPoints)
        self.ManaBar.value=self.ManaPoints;self.ManaBar.animation_duration=0

        #keybinds
        with open(controlsPath) as file:
            self.data = json.load(file)

        self.walkForward = playerControllerWalkW
        self.strafeLeft = playerControllerWalkA
        self.walkBackward = playerControllerWalkS
        self.strafeRight = playerControllerWalkD
        self.interact = playerControllerInteract
        self.sprint = self.data['Shift']


    def UseMana(self, amount):
        if amount>self.ManaPoints:
            return False
        elif amount<=self.ManaPoints:
            self.ManaPoints -= amount
            return True

    def UseMagic(self):
        spell_map = {
            'TimeStop': self.Timestop.Activate,
            #'FireWave': self.Firewave.Activate,
        }
        if self.CurrentEquiped in spell_map and self.CurrentEquiped in self.Spells:
            spell_map[self.CurrentEquiped]()


    def OnLevelUp(self):
        self.Level += 1
        self.ExperienceNeeded *= 2

    def input(self, key):
        if key==player.interact and not application.paused:
            self.UseMagic()

    def update(self):
        if self.HitPoints <= 0:
            pass
            #DeathScreen()
        if any(held_keys[key] for key in [self.walkForward, self.walkBackward, self.strafeRight, self.strafeLeft]):
            self.bobbing_timer += self.bobbing_speed
            vertical_offset = abs(math.sin(self.bobbing_timer)) * self.bobbing_amount
            camera.y = vertical_offset

            if not self.normalFootSteps.playing:
                self.normalFootSteps.play()

            if held_keys[self.sprint]:
                if held_keys[self.walkForward]:
                    playerController.speed = 16
                    self.bobbing_speed = 0.2
                elif held_keys[self.walkBackward]:
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
        self.ManaBar.value=self.ManaPoints
        self.ManaBar.max_value=self.MaxManaPoints
        self.HealthBar.value=self.HitPoints
        self.HealthBar.max_value=self.MaxHitPoints


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
        self.canRunAgain=Sequence(Wait(6),Func(setattr, self, 'canRun', True),auto_destroy=False)
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
        self.model = 'cube'
        self.color = color.red
        self.collider='box'
        self.inRange = False
        self.inRangeAttack = False
        self.touchingBorder = False
        self.y = 2
        self.scale_y=2
        self.attackSeq = Sequence(Func(self.Attack),Wait(1),loop=True)
        self.shader=lit_with_shadows_shader

    def MovementToPlayer(self):
        self.position += self.forward * time.dt

    def update(self):
        self.dist = distance(playerController.position, self.position)
        if 1.5 < self.dist < 18:
            self.inRange = True
            self.inRangeAttack = False
        elif self.dist <= 1.5:
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
                if self.attackSeq.paused:
                    self.attackSeq.start()
                    print("Started")
        else:
            if not self.touchingBorder and not player.Timestop.enemyTimestopped:
                self.position += self.forward * time.dt * 2
        if not self.inRangeAttack and not self.attackSeq.paused:
            self.attackSeq.finish()

    def Attack(self):
        damage = random.randint(1, 5)
        player.HitPoints -= damage

window.title = "ChronoGate - Playground"

app=Ursina(borderless=False,vsync=60,development_mode=True,fullscreen=False)
PlayerSensitvity=(40,40)
enemyList=[]
playerControllerWalkW = 'w'
playerControllerWalkS = 's'
playerControllerWalkA = 'a'
playerControllerWalkD = 'd'
playerControllerInteract = 'e'
GROUND=Entity(model='plane',scale=1000,texture='grass',texture_scale=(32,32),collider='box')
playerController=FirstPersonController()
player=Player(y=3)
playerController.mouse_sensitivity = PlayerSensitvity
enemyList.append(EnemyNormal(x=20))
enemyList.append(EnemyNormal(x=40))

Sky(texture='assets/textures/misc/sky.jpg')

app.run()