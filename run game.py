from ursina import *
from ursina.prefabs.first_person_controller import *
import threading
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
        self.CurrentEquiped = 'TimeStop'
        self.SpellEquiped = Text(text='Current spell: None',x=-.87,y=-.45)
        self.Spells = ['TimeStop', 'FireWave', ]
        self.Timestop = TimeStop()
        #self.Firewave = Firewave()
        
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
        input_handler.rebind('a', '')
        input_handler.rebind('b', '')
        input_handler.rebind('c', '')
        input_handler.rebind('d', '')
        input_handler.rebind('e', '')
        input_handler.rebind('f', '')
        input_handler.rebind('g', '')
        input_handler.rebind('h', '')
        input_handler.rebind('i', '')
        input_handler.rebind('j', '')
        input_handler.rebind('k', '')
        input_handler.rebind('l', '')
        input_handler.rebind('m', '')
        input_handler.rebind('n', '')
        input_handler.rebind('o', '')
        input_handler.rebind('p', '')
        input_handler.rebind('q', '')
        input_handler.rebind('r', '')
        input_handler.rebind('s', '')
        input_handler.rebind('t', '')
        input_handler.rebind('u', '')
        input_handler.rebind('v', '')
        input_handler.rebind('w', '')
        input_handler.rebind('x', '')
        input_handler.rebind('y', '')
        input_handler.rebind('z', '')
        input_handler.rebind('shift', '')
        input_handler.rebind(self.w, 'w')
        input_handler.rebind(self.c, 'c')
        input_handler.rebind(self.b, 'b')
        input_handler.rebind(self.a, 'a')
        input_handler.rebind(self.s, 's')
        input_handler.rebind(self.d, 'd')
        input_handler.rebind(self.f, 'f')
        input_handler.rebind(self.e, 'e')
        input_handler.rebind(self.g, 'g')
        input_handler.rebind(self.h, 'h')
        input_handler.rebind(self.i, 'i')
        input_handler.rebind(self.j, 'j')
        input_handler.rebind(self.k, 'k')
        input_handler.rebind(self.l, 'l')
        input_handler.rebind(self.m, 'm')
        input_handler.rebind(self.n, 'n')
        input_handler.rebind(self.o, 'o')
        input_handler.rebind(self.p, 'p')
        input_handler.rebind(self.q, 'q')
        input_handler.rebind(self.r, 'r')
        input_handler.rebind(self.s, 's')
        input_handler.rebind(self.t, 't')
        input_handler.rebind(self.u, 'u')
        input_handler.rebind(self.v, 'v')
        input_handler.rebind(self.w, 'w')
        input_handler.rebind(self.xb, 'x')
        input_handler.rebind(self.yb, 'y')
        input_handler.rebind(self.zb, 'z')
        input_handler.rebind(self.shift, 'shift')


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
        if key=='e' and not application.paused:
            self.UseMagic()

    def update(self):
        if self.HitPoints <= 0:
            DeathScreen()
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

class TimeStop(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.TimestopAudio=Audio('assets/audio/spells/TimeStop/timestop.ogg',autoplay=False,loop=False,volume=1)
        self.ClockTickingAudio=Audio('assets/audio/spells/TimeStop/ClockTicking.ogg',autoplay=False,loop=False,volume=1)
        self.TimeresumeAudio=Audio('assets/audio/spells/TimeStop/timeresume.ogg',autoplay=False,loop=False,volume=1)
        self.canRun = True
        self.resume=Sequence(Wait(7),Func(self.resumeTime),auto_destroy=False)
        self.ticking=Sequence(Wait(2),Func(self.ClockTickingAudio.play),auto_destroy=False)
        self.canRunAgain=Sequence(Wait(50),Func(setattr, self, 'canRun', True),auto_destroy=False)
        self.loadanims=threading.Thread(target=self.loadAnims).start()

    def loadAnims(self):
        self.e=Animation(parent=camera.ui,name='assets/textures/spells/time/ts.gif',scale=(2,1),visible=False)

    def Activate(self):
        if self.canRun:
            EnoughMana=player.UseMana(amount=10)
            print("used mana")
            if EnoughMana:
                if not self.TimestopAudio.playing:
                    self.TimestopAudio.play()
                else:
                    pass
                self.pauseTime()
                print(f"Remaining mana: {player.ManaPoints}")
            elif not EnoughMana:
                pass

    def pauseTime(self):
        global enemyTimestopped
        enemyTimestopped = True
        self.canRun = False
        self.resume.start()
        self.ticking.start()

    def resumeTime(self):
        global enemyTimestopped
        enemyTimestopped = False
        self.TimeresumeAudio.play()
        self.canRunAgain.start()

class EnemyNormal(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.model = 'cube'
        self.color = color.red
        self.inRange = False
        self.inRangeAttack = False
        self.touchingBorder = False
        self.y = 1

    def MovementToPlayer(self):
        self.position += self.forward * time.dt

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
        if self.inRange and not enemyTimestopped:
            self.look_at_2d(playerController.position, 'y')
            self.MovementToPlayer()
        elif self.inRangeAttack:
            if not enemyTimestopped:
                self.look_at_2d(playerController.position, 'y')
                pass
        else:
            if not self.touchingBorder and not enemyTimestopped:
                self.position += self.forward * time.dt * 2

class MenuScreenDeath(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Entities = []
        self.model='quad'
        self.texture='assets/textures/menu/background.jpg'
        self.scale=[16,9]

        self.startAudio = Audio('assets/audio/menu/start.ogg',autoplay=False,loop=False)
        self.clickAudio = Audio('assets/audio/menu/click.ogg',autoplay=False,loop=False)
        self.click2Audio = Audio('assets/audio/menu/click1.ogg',autoplay=False,loop=False)

        self.mouseSens = 4

        self.btnX = 0.2
        self.btnY = 0.075

        self.btnColor = rgb(0,0,0,30)
        self.btnHcolor = rgb(0,0,0,50)
        self.optMenuP = Entity(position=(2,0),parent=camera.ui)
        self.shopMenuP = Entity(position=(2,0),parent=camera.ui)
        self.volume_sliderP = Entity(position=(24,4),paret=camera.ui)
        self.sensDecreaseP = Entity(position=(2,0),parent=camera.ui)
        self.sensIncreaseP = Entity(position=(2,0),parent=camera.ui)
        self.sensTextP = Entity(position=(2,0),parent=camera.ui)
        self.sensTitleP = Entity(position=(2.05,.1),parent=camera.ui)
        self.keybindsP = Entity(position=(2,-0.2),parent=camera.ui)

        self.UI = Entity(parent=camera.ui)

        self.TimerActive=False
        self.timer=0

        self.keyboard = Entity(model='quad',parent=camera.ui,visible=False,texture='assets/textures/menu/keyboard.png',z=-10,scale=[1.78,1])
        self.exitKeyboard = Button(visible=False,x=.85,y=.45,radius=.3,z=-11,parent=self.UI,scale=(.05,.05),text='X',text_color=color.black,color=color.red,highlight_color=color.red,highlight_scale=1.2,pressed_scale=1.07,pressed_color=color.red)
        self.exitKeyboard.on_click = self.Keyboard

        self.titleScreen = Text(font='assets/textures/fonts/MainFont.ttf',text='ChronoGate',y=.4,x=-.185)

        self.newGameBTN = Button(radius=.3, parent=self.UI,scale=(self.btnX,self.btnY),text='Retry',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.newGameBTN.on_click=self.Retry

        self.btnPosY1 = self.newGameBTN.y
        self.optionsGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Options',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.optionsGameBTN.add_script(SmoothFollow(target=self.newGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.optionsGameBTN.on_click=self.opt

        self.btnPosY2 = self.optionsGameBTN.y
        self.shopGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Credits',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0 )
        self.shopGameBTN.add_script(SmoothFollow(target=self.optionsGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.shopGameBTN.on_click=self.shop


        self.btnPosY3 = self.shopGameBTN.y
        self.quitGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Quit',color=self.btnColor,highlight_color=rgb(255,0,0,20),highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.quitGameBTN.add_script(SmoothFollow(target=self.shopGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.quitGameBTN.on_click=self.quit_

        #After button clicked stuff
        self.volume_slider = Slider(step=1,parent=self.UI,min=0, max=100, default=100, dynamic=True,position=(-24,.3),text='Master volume:',on_value_changed = self.set_volume)
        self.volume_slider.add_script(SmoothFollow(target=self.volume_sliderP,speed=6))

        self.sensDecrease = Button(text='e',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensDecrease.add_script(SmoothFollow(target=self.sensDecreaseP,speed=6))
        self.sensDecrease.on_click = self.decreaseSens
        self.sensDecrease.text_entity.use_tags=False;self.sensDecrease.text = '<'

        self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ 4 ₅ ₆ ₇ ₈')
        self.sensText.add_script(SmoothFollow(target=self.sensTextP,speed=6))
        self.sensTitle=Text(ignore=False,parent=camera.ui,scale=1.5,y=.025,x=.02,text='Sensitivity')
        self.sensTitle.add_script(SmoothFollow(target=self.sensTitleP,speed=6))

        self.sensIncrease = Button(text='e',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensIncrease.add_script(SmoothFollow(target=self.sensIncreaseP,speed=6))
        self.sensIncrease.on_click = self.increaseSens
        self.sensIncrease.text_entity.use_tags=False;self.sensIncrease.text = '>'

        self.keybinds=Button(text='Change keybinds',radius=.3,parent=self.UI,color=self.btnColor,scale=(.3,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.keybinds.on_click=self.Keyboard
        self.keybinds.add_script(SmoothFollow(target=self.keybindsP,speed=6))

        self.shopMenu = Button(radius=.3,scale=1,color=color.clear,z=3,text='<scale:2>Main credits\n\n\n<scale:1>Coding: Bailey\n\nGame design: Bailey\n\nEverything else: Bailey\n\nSmooth menu animations: @Code3D_ (yt)\n\n\n\n<scale:2>Special thanks<scale:1>\n\n\n- RangerRhino23\n\n\n\n\n<scale:.8>Why RangerRhino23? - Because I can and I did.')
        self.shopMenu.add_script(SmoothFollow(target=self.shopMenuP,speed=6))

        #Destroy all entites related to the menu
        self.EntitiesA = [self.startAudio,self.clickAudio,self.optMenuP,self.optionsGameBTN,
        self.UI,self.shopMenuP,self.titleScreen,self.newGameBTN,self.shopGameBTN,self.shopMenu,self.shopMenuP,
        self.quitGameBTN,self.volume_slider,self.volume_sliderP,self.sensDecrease,self.sensDecreaseP,self.sensIncrease,
        self.sensIncreaseP,self.sensText,self.sensTextP,self.sensTitle,self.sensTitleP,self.keyboard,self.exitKeyboard,
        self.keybindsP,self.keybinds,self.click2Audio]

        self.Entities.extend(self.EntitiesA)

    def increaseSens(self):
        global PlayerSensitvity
        if self.mouseSens < 8:
            self.mouseSens += 1
            if self.mouseSens == 2:
                self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (20,20)
            elif self.mouseSens == 3:
                self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (30,30)
            elif self.mouseSens == 4:
                self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                PlayerSensitvity = (40,40)
            elif self.mouseSens == 5:
                self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                PlayerSensitvity = (50,50)
            elif self.mouseSens == 6:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                PlayerSensitvity = (60,60)
            elif self.mouseSens == 7:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                PlayerSensitvity = (70,70)
            elif self.mouseSens == 8:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ ₇ 8'
                PlayerSensitvity = (80,80)
            self.click2Audio.play()

    def decreaseSens(self):
        global PlayerSensitvity
        if self.mouseSens > 1:
            self.mouseSens -= 1
            if self.mouseSens == 1:
                self.sensText.text = '1 ₂ ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (10,10)
            elif self.mouseSens == 2:
                self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (20,20)
            elif self.mouseSens == 3:
                self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (30,30)
            elif self.mouseSens == 4:
                self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                PlayerSensitvity = (40,40)
            elif self.mouseSens == 5:
                self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                PlayerSensitvity = (50,50)
            elif self.mouseSens == 6:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                PlayerSensitvity = (60,60)
            elif self.mouseSens == 7:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                PlayerSensitvity = (70,70)
            self.click2Audio.play()
            
    def Keyboard(self):
        self.keyboard.visible=not self.keyboard.visible
        self.exitKeyboard.visible =not self.exitKeyboard.visible
           
    def set_volume(self):
        volume = self.volume_slider.value/100
        app.sfxManagerList[0].setVolume(volume)
        
    def Retry(self):
        for e in self.Entities:
            destroy(e)
        destroy(self.parent)
        for e in scene.entities:
            print(e)
        
    
    def opt(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        if self.newGameBTN.x == 0:
            # Open options
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (0,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.24,0.09)
            self.optionsGameBTN.color = (0,0,0,60)
            self.titleScreen.text = 'Options'
            self.titleScreen.x = -.1
            self.volume_sliderP.position = (-1, 4)
            self.sensDecreaseP.position = (-.1,0)
            self.sensIncreaseP.position = (.4,0)
            self.sensTextP.position = (0.02,.02)
            self.sensTitleP.position = (0.05,.1)
            self.keybindsP.position = (.125,-0.2)

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.optionsGameBTN.color == (0,0,0,60):
            #Close options
            self.newGameBTN.x = 0
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor
            self.volume_sliderP.position = (24,4)
            self.titleScreen.text = 'chronogate'
            self.titleScreen.x = -.185
            self.sensDecreaseP.position = (2,0)
            self.sensIncreaseP.position = (2,0)
            self.sensTextP.position = (2,0)
            self.sensTitleP.position = (2.05,.1)
            self.keybindsP.position=(2,-0.2)

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.shopGameBTN.color == (0,0,0,60):
            #Switch back to options
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (0,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.24,0.09)
            self.optionsGameBTN.color = (0,0,0,60)
            self.volume_sliderP.position = (-1, 4)
            self.titleScreen.text = 'Options'
            self.titleScreen.x = -.1
            self.sensDecreaseP.position = (-.1,0)
            self.sensIncreaseP.position = (.4,0)
            self.sensTextP.position = (0.02,.02)
            self.sensTitleP.position = (0.05,.1)
            self.keybindsP.position = (.125,-0.2)
            
            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor

    def shop(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        if self.newGameBTN.x == 0:
            #Open Credits
            self.newGameBTN.x =- 0.75
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (0,0)

            self.shopGameBTN.scale = (0.24,0.09)
            self.shopGameBTN.color = (0,0,0,60)
            self.titleScreen.text = 'Credits'
            self.titleScreen.x = -.1

            self.optionsGameBTN.scale= (0.2,0.075)
            self.optionsGameBTN.color=self.btnColor
        elif self.newGameBTN.x == -0.75 and self.shopGameBTN.color == (0,0,0,60):
            #Close credits
            self.newGameBTN.x = 0
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor
            self.titleScreen.text = 'chronogate'
            self.titleScreen.x = -.185

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.optionsGameBTN.color == (0,0,0,60):
            #Switch to back credits
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (0,0)

            self.shopGameBTN.scale = (0.24,0.09)
            self.shopGameBTN.color = (0,0,0,60)
            self.volume_sliderP.position = (24, 4)
            self.titleScreen.text = 'Credits'
            self.titleScreen.x = -.1
            self.sensDecreaseP.position = (2,0)
            self.sensIncreaseP.position = (2,0)
            self.sensTextP.position = (2,0)
            self.sensTitleP.position = (2.05,.1)
            self.keybindsP.position=(2,-0.2)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor       

    def quit_(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        self.TimerActive=True
    def update(self):
        if self.TimerActive:
            self.timer+=time.dt
        if self.timer>=0.6:
            application.quit()

class MenuScreen(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Entities = []
        self.model='quad'
        self.texture='assets/textures/menu/background.jpg'
        self.scale=[16,9]

        self.startAudio = Audio('assets/audio/menu/start.ogg',autoplay=False,loop=False)
        self.clickAudio = Audio('assets/audio/menu/click.ogg',autoplay=False,loop=False)
        self.click2Audio = Audio('assets/audio/menu/click1.ogg',autoplay=False,loop=False)
        self.introAudio = Audio('assets/audio/menu/intro.ogg',autoplay=False,loop=False)

        self.TimerActive = False
        self.timer = 0
        self.canSkip = False
        self.skipTimer = 0
        self.canSkipText = Text(z=-2,visible=False,text="Hold 'e' to skip.",x=-.88,y=-.46)
        self.mouseSens = 4

        self.btnX = 0.2
        self.btnY = 0.075

        self.btnColor = rgb(0,0,0,30)
        self.btnHcolor = rgb(0,0,0,50)
        self.optMenuP = Entity(position=(2,0),parent=camera.ui)
        self.shopMenuP = Entity(position=(2,0),parent=camera.ui)
        self.volume_sliderP = Entity(position=(24,4),paret=camera.ui)
        self.sensDecreaseP = Entity(position=(2,0),parent=camera.ui)
        self.sensIncreaseP = Entity(position=(2,0),parent=camera.ui)
        self.sensTextP = Entity(position=(2,0),parent=camera.ui)
        self.sensTitleP = Entity(position=(2.05,.1),parent=camera.ui)
        self.keybindsP = Entity(position=(2,-0.2),parent=camera.ui)

        self.UI = Entity(parent=camera.ui)

        self.WormholeTravel = Entity(model='quad',parent=camera.ui,visible=False,texture='assets/textures/menu/menu.mp4',scale_y=1,scale_x=2)
        self.blackScreen = Entity(model='quad',color=color.black, scale=213,alpha=0)

        self.titleScreen = Text(font='assets/textures/fonts/MainFont.ttf',text='ChronoGate',y=.4,x=-.185)

        self.newGameBTN = Button(radius=.3, parent=self.UI,scale=(self.btnX,self.btnY),text='Start Game',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.newGameBTN.on_click=self.Startgame

        self.btnPosY1 = self.newGameBTN.y
        self.optionsGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Options',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.optionsGameBTN.add_script(SmoothFollow(target=self.newGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.optionsGameBTN.on_click=self.opt

        self.btnPosY2 = self.optionsGameBTN.y
        self.shopGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Credits',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0 )
        self.shopGameBTN.add_script(SmoothFollow(target=self.optionsGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.shopGameBTN.on_click=self.shop


        self.btnPosY3 = self.shopGameBTN.y
        self.quitGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Quit',color=self.btnColor,highlight_color=rgb(255,0,0,20),highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.quitGameBTN.add_script(SmoothFollow(target=self.shopGameBTN,speed=6,offset=[0,-1.75,0.75]))
        self.quitGameBTN.on_click=self.quit_

        #After button clicked stuff
        self.volume_slider = Slider(step=1,parent=self.UI,min=0, max=100, default=100, dynamic=True,position=(-24,.3),text='Master volume:',on_value_changed = self.set_volume)
        self.volume_slider.add_script(SmoothFollow(target=self.volume_sliderP,speed=6))

        self.sensDecrease = Button(text='e',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensDecrease.add_script(SmoothFollow(target=self.sensDecreaseP,speed=6))
        self.sensDecrease.on_click = self.decreaseSens
        self.sensDecrease.text_entity.use_tags=False;self.sensDecrease.text = '<'

        self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ 4 ₅ ₆ ₇ ₈')
        self.sensText.add_script(SmoothFollow(target=self.sensTextP,speed=6))
        self.sensTitle=Text(ignore=False,parent=camera.ui,scale=1.5,y=.025,x=.02,text='Sensitivity')
        self.sensTitle.add_script(SmoothFollow(target=self.sensTitleP,speed=6))

        self.sensIncrease = Button(text='e',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensIncrease.add_script(SmoothFollow(target=self.sensIncreaseP,speed=6))
        self.sensIncrease.on_click = self.increaseSens
        self.sensIncrease.text_entity.use_tags=False;self.sensIncrease.text = '>'

        self.keybinds=Button(text='Show key binds',radius=.3,parent=self.UI,color=self.btnColor,scale=(.3,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.keybinds.on_click=self.keybind
        self.keybinds.add_script(SmoothFollow(target=self.keybindsP,speed=6))

        self.shopMenu = Button(radius=.3,scale=1,color=color.clear,z=3,text='<scale:2>Main credits\n\n\n<scale:1>Coding: Bailey\n\nGame design: Bailey\n\nEverything else: Bailey\n\nSmooth menu animations: @Code3D_ (yt)\n\n\n\n<scale:2>Special thanks<scale:1>\n\n\n- RangerRhino23\n\n\n\n\n<scale:.8>Why RangerRhino23? - Because I can and I did.')
        self.shopMenu.add_script(SmoothFollow(target=self.shopMenuP,speed=6))

        #Destroy all entites related to the menu
        self.EntitiesA = [self.startAudio,self.clickAudio,self.optMenuP,self.optionsGameBTN,
        self.UI,self.shopMenuP,self.titleScreen,self.newGameBTN,self.shopGameBTN,self.shopMenu,self.shopMenuP,
        self.quitGameBTN,self.volume_slider,self.volume_sliderP,self.sensDecrease,self.sensDecreaseP,self.sensIncrease,
        self.sensIncreaseP,self.sensText,self.sensTextP,self.sensTitle,self.sensTitleP,self.keybinds,self.keybinds,
        self.click2Audio]

        self.Entities.extend(self.EntitiesA)

    def increaseSens(self):
        global PlayerSensitvity
        if self.mouseSens < 8:
            self.mouseSens += 1
            if self.mouseSens == 2:
                self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (20,20)
            elif self.mouseSens == 3:
                self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (30,30)
            elif self.mouseSens == 4:
                self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                PlayerSensitvity = (40,40)
            elif self.mouseSens == 5:
                self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                PlayerSensitvity = (50,50)
            elif self.mouseSens == 6:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                PlayerSensitvity = (60,60)
            elif self.mouseSens == 7:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                PlayerSensitvity = (70,70)
            elif self.mouseSens == 8:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ ₇ 8'
                PlayerSensitvity = (80,80)
            self.click2Audio.play()

    def decreaseSens(self):
        global PlayerSensitvity
        if self.mouseSens > 1:
            self.mouseSens -= 1
            if self.mouseSens == 1:
                self.sensText.text = '1 ₂ ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (10,10)
            elif self.mouseSens == 2:
                self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (20,20)
            elif self.mouseSens == 3:
                self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                PlayerSensitvity = (30,30)
            elif self.mouseSens == 4:
                self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                PlayerSensitvity = (40,40)
            elif self.mouseSens == 5:
                self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                PlayerSensitvity = (50,50)
            elif self.mouseSens == 6:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                PlayerSensitvity = (60,60)
            elif self.mouseSens == 7:
                self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                PlayerSensitvity = (70,70)
            self.click2Audio.play()

    def keybind(self):
        for e in self.Entities:
            e.enabled=False
        Keybinds(egg=self)
      
    def set_volume(self):
        volume = self.volume_slider.value/100
        app.sfxManagerList[0].setVolume(volume)

    def Startgame(self):
        for e in self.Entities:
            destroy(e)
        self.startAudio.play()
        self.WormholeTravel.visible = True
        self.s = Sequence(Wait(1),Func(self.introAudio.play))
        self.s1 = Sequence(Wait(3),Func(self.ShowSkipButton))
        self.s4 = Sequence(Wait(43),Func(self.FadeToBlack))
        self.s.start()
        self.s1.start()
        self.s4.start()


    def ShowSkipButton(self):
        self.canSkip=True
        self.canSkipText.visible=True
        self.s3=Sequence(1, Func(self.canSkipText.blink, duration=1),loop=True)
        self.s3.start()

    def FadeToBlack(self):
        self.texture = None
        self.color=color.clear
        self.WormholeTravel.fade_out(duration=1.3)
        self.blackScreen.fade_in(duration=1.3)
        destroy(self.canSkipText)
        invoke(self.startGame,delay=2)

    def startGame(self):
        global GROUND,player,playerController,enemyOne,PauseScreen
        self.blackScreen.fade_out(duration=.8)
        destroy(self.WormholeTravel)
        destroy(self)
        self.s4.pause()
        player=Player()
        playerController=FirstPersonController()
        playerController.mouse_sensitivity = PlayerSensitvity
        enemyOne = EnemyNormal(x=20)
        GROUND=Entity(model='plane',scale=1000,texture='grass',texture_scale=(32,32),collider='box')
        PauseScreen = None

    def opt(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        if self.newGameBTN.x == 0:
            # Open options
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (0,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.24,0.09)
            self.optionsGameBTN.color = (0,0,0,60)
            self.titleScreen.text = 'Options'
            self.titleScreen.x = -.1
            self.volume_sliderP.position = (-1, 4)
            self.sensDecreaseP.position = (-.1,0)
            self.sensIncreaseP.position = (.4,0)
            self.sensTextP.position = (0.02,.02)
            self.sensTitleP.position = (0.05,.1)
            self.keybindsP.position = (.125,-0.2)

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.optionsGameBTN.color == (0,0,0,60):
            #Close options
            self.newGameBTN.x = 0
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor
            self.volume_sliderP.position = (24,4)
            self.titleScreen.text = 'chronogate'
            self.titleScreen.x = -.185
            self.sensDecreaseP.position = (2,0)
            self.sensIncreaseP.position = (2,0)
            self.sensTextP.position = (2,0)
            self.sensTitleP.position = (2.05,.1)
            self.keybindsP.position=(2,-0.2)

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.shopGameBTN.color == (0,0,0,60):
            #Switch back to options
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (0,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.24,0.09)
            self.optionsGameBTN.color = (0,0,0,60)
            self.volume_sliderP.position = (-1, 4)
            self.titleScreen.text = 'Options'
            self.titleScreen.x = -.1
            self.sensDecreaseP.position = (-.1,0)
            self.sensIncreaseP.position = (.4,0)
            self.sensTextP.position = (0.02,.02)
            self.sensTitleP.position = (0.05,.1)
            self.keybindsP.position = (.125,-0.2)
            
            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor

    def shop(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        if self.newGameBTN.x == 0:
            #Open Credits
            self.newGameBTN.x =- 0.75
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (0,0)

            self.shopGameBTN.scale = (0.24,0.09)
            self.shopGameBTN.color = (0,0,0,60)
            self.titleScreen.text = 'Credits'
            self.titleScreen.x = -.1

            self.optionsGameBTN.scale= (0.2,0.075)
            self.optionsGameBTN.color=self.btnColor
        elif self.newGameBTN.x == -0.75 and self.shopGameBTN.color == (0,0,0,60):
            #Close credits
            self.newGameBTN.x = 0
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (2,0)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor
            self.titleScreen.text = 'chronogate'
            self.titleScreen.x = -.185

            self.shopGameBTN.scale = (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.optionsGameBTN.color == (0,0,0,60):
            #Switch to back credits
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (0,0)

            self.shopGameBTN.scale = (0.24,0.09)
            self.shopGameBTN.color = (0,0,0,60)
            self.volume_sliderP.position = (24, 4)
            self.titleScreen.text = 'Credits'
            self.titleScreen.x = -.1
            self.sensDecreaseP.position = (2,0)
            self.sensIncreaseP.position = (2,0)
            self.sensTextP.position = (2,0)
            self.sensTitleP.position = (2.05,.1)
            self.keybindsP.position=(2,-0.2)

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color = self.btnColor       

    def quit_(self):
        if not self.clickAudio.playing:
            self.clickAudio.play()
        self.TimerActive = True

    def update(self):
        if self.TimerActive:
            self.timer+=time.dt
        if self.timer>=0.6:
            application.quit()
        if self.canSkip:
            if held_keys['e']:
                self.skipTimer+=time.dt
                if self.skipTimer>=1.2:
                    self.canSkip=False
                    self.introAudio.stop()
                    self.FadeToBlack()
            else:
                if self.skipTimer > 0:
                    self.skipTimer-=time.dt
                elif self.skipTimer < 0:
                    self.skipTimer = 0

class DeathScreen(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entities=[]
        self.e="e"
        self.model='quad'
        self.texture='assets/textures/menu/YouDied.png'
        self.scale=[16,9]
        self.audio = Audio('assets/audio/player/death.ogg',loop=False,auto_play=True,auto_destroy=True)
        self.s = Sequence(Wait(4),Func(self.loadMenu)).start()
        self.Added=[self.audio,self.s]
        self.entities.extend(self.Added)

    def loadMenu(self):
        MenuScreenDeath(parent=self)
        for e in self.entities:
            destroy(e)
            self.model=None

class Keybinds(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.parent=camera.ui
        self.model='quad'
        self.color=color.gray
        self.scale_x=2
        self.z=-199
        self.ignore_paused=True
        with open('assets/data/controls.json') as file:
            self.data = json.load(file)

        self.key_exceptions = ['left mouse down', 'left mouse hold', 'left mouse up', 'escape', 'double click', 'right mouse down',
        'right mouse hold', 'right mouse up', '`', '` hold', '` up', "'","' up", "' hold", '#', '# up', '# hold', ']', '[', '=',
        '= up', '= hold', '-', '- up', '- hold', 'tab', 'tab up', 'tab hold', ',', ', up', ', hold', '.', '. up', '. hold', 'a up', 'a hold']

        self.execpt = ['left mouse down', 'left mouse hold', 'escape', 'double click', 'right mouse down',
        'right mouse hold', 'right mouse up']    
        self.changeW = False
        self.changeA = False
        self.changeS = False
        self.changeD = False
        self.w = self.data['W']
        self.a = self.data['A']
        self.s = self.data['S']
        self.d = self.data['D']
        self.ButtonW = Button(radius=.2,text=self.w,scale=(.15,.07),x=.4,y=.4,on_click = Func(self.ChangeLetter, 'w'),z=-200)
        self.ButtonWText = Text(text='Walk Forward',y=.4,x=-.2,z=-200)
        self.ButtonW.text_entity.use_tags=False
        self.ButtonA = Button(radius=.2,text=self.a,scale=(.15,.07),x=.4,y=.3,on_click = Func(self.ChangeLetter, 'a'),z=-200)
        self.ButtonAText = Text(text='Strafe Left',y=.3,x=-.2,z=-200)
        self.ButtonA.text_entity.use_tags=False
        self.ButtonS = Button(radius=.2,text=self.s,scale=(.15,.07),x=.4,y=.2,on_click = Func(self.ChangeLetter, 's'),z=-200)
        self.ButtonSText = Text(text='Walk Backwards',y=.2,x=-.2,z=-200)
        self.ButtonS.text_entity.use_tags=False
        self.ButtonD = Button(radius=.2,text=self.d,scale=(.15,.07),x=.4,y=.1,on_click = Func(self.ChangeLetter, 'd'),z=-200)
        self.ButtonDText = Text(text='Strafe Right',y=.1,x=-.2,z=-200)
        self.ButtonD.text_entity.use_tags=False
        self.ButtonWSeq = Sequence(Wait(.25),Func(setattr, self.ButtonW, "text", f"> {self.data['W']} <"), Wait(.25),Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">   {self.data['W']}   <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),loop=True)
        self.ButtonASeq = Sequence(Wait(.25),Func(setattr, self.ButtonA, "text", f"> {self.data['A']} <"), Wait(.25),Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">   {self.data['A']}   <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),loop=True)
        self.ButtonSSeq = Sequence(Wait(.25),Func(setattr, self.ButtonS, "text", f"> {self.data['S']} <"), Wait(.25),Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">   {self.data['S']}   <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),loop=True)
        self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)

        self.ButtonLeave = Button(radius=.2,text='Exit',scale=(.15,.07),y=-.4,on_click = self.LeaveKeybinds,z=-200)
        self.Entities=[self.ButtonLeave,self.ButtonA,self.ButtonW,self.ButtonS,self.ButtonD,self.ButtonAText,self.ButtonWText,self.ButtonSText,self.ButtonDText]

    def ChangeLetter(self, arg):
        match arg:
            case 'w':
                self.changeW = True
                self.ButtonW.text = f'>  {self.data["W"]}  <'
                self.ButtonWSeq.start()
            case 'a':
                self.changeA = True
                self.ButtonA.text = f'>  {self.data["A"]}  <'
                self.ButtonASeq.start()
            case 's':
                self.changeS = True
                self.ButtonS.text = f'>  {self.data["S"]}  <'
                self.ButtonSSeq.start()
            case 'd':
                self.changeD = True
                self.ButtonD.text = f'>  {self.data["D"]}  <'
                self.ButtonDSeq.start()
            case _:
                print("None")

    def LeaveKeybinds(self):
        for e in self.egg.Entities:
            e.enabled=True
        for e in self.Entities:
            destroy(e)
        destroy(self)

    def input(self, key):
        if self.changeW:
            if key not in self.key_exceptions and key:
                self.ButtonWSeq.kill()
                self.changeW = False
                self.ButtonW.text = key
                self.data['W'] = self.ButtonW.text
                input_handler.rebind(self.ButtonW.text, 'w')
                self.ButtonWSeq = Sequence(Wait(.25),Func(setattr, self.ButtonW, "text", f"> {self.data['W']} <"), Wait(.25),Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">   {self.data['W']}   <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),loop=True)
            elif key in self.execpt:
                self.changeW = False
                self.ButtonWSeq.kill()
                self.ButtonW.text = self.data['W']
                self.ButtonWSeq = Sequence(Wait(.25),Func(setattr, self.ButtonW, "text", f"> {self.data['W']} <"), Wait(.25),Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">   {self.data['W']}   <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),loop=True)
        if self.changeA:
            if key not in self.key_exceptions and key:
                self.ButtonASeq.kill()
                self.changeA = False
                self.ButtonA.text = key
                self.data['A'] = self.ButtonA.text
                input_handler.rebind(self.ButtonA.text, 'a')
                self.ButtonASeq = Sequence(Wait(.25),Func(setattr, self.ButtonA, "text", f"> {self.data['A']} <"), Wait(.25),Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">   {self.data['A']}   <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),loop=True)
            elif key in self.execpt:
                self.changeA = False
                self.ButtonASeq.kill()
                self.ButtonA.text = self.data['A']
                self.ButtonASeq = Sequence(Wait(.25),Func(setattr, self.ButtonA, "text", f"> {self.data['A']} <"), Wait(.25),Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">   {self.data['A']}   <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),loop=True)
        if self.changeS:
            if key not in self.key_exceptions and key:
                self.ButtonSSeq.kill()
                self.changeS = False
                self.ButtonS.text = key
                self.data['S'] = self.ButtonS.text
                input_handler.rebind(self.ButtonS.text, 's')
                self.ButtonSSeq = Sequence(Wait(.25),Func(setattr, self.ButtonS, "text", f"> {self.data['S']} <"), Wait(.25),Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">   {self.data['S']}   <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),loop=True)
            elif key in self.execpt:
                self.changeS = False
                self.ButtonSSeq.kill()
                self.ButtonS.text = self.data['S']
                self.ButtonSSeq = Sequence(Wait(.25),Func(setattr, self.ButtonS, "text", f"> {self.data['S']} <"), Wait(.25),Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">   {self.data['S']}   <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),loop=True)
        if self.changeD:
            if key not in self.key_exceptions and key:
                self.ButtonDSeq.kill()
                self.changeD = False
                self.ButtonD.text = key
                self.data['D'] = self.ButtonD.text
                input_handler.rebind(self.ButtonD.text, 'd')
                self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)
            elif key in self.execpt:
                self.changeD = False
                self.ButtonDSeq.kill()
                self.ButtonD.text = self.data['D']
                self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)
        with open('assets/data/controls.json', 'w') as file:
            json.dump(self.data, file,indent=4)

class PauseMenuScreen(Entity):
    def __init__(self, add_to_scene_entities=False, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Entities = []
        self.model='quad'
        self.parent=camera.ui
        self.color=color.black
        self.alpha=.6
        self.scale=[16,9]
        mouse.locked=False
        playerController.cursor.enabled = False
        application.pause()
                
        self.startAudio = Audio('assets/audio/menu/start.ogg',autoplay=False,loop=False)
        self.clickAudio = Audio('assets/audio/menu/click.ogg',autoplay=False,loop=False)
        self.click2Audio = Audio('assets/audio/menu/click1.ogg',autoplay=False,loop=False)
        
        self.btnColor = rgb(0,0,0,30)
        self.btnHcolor = rgb(0,0,0,50)

        self.title = Text(font='assets/textures/fonts/PauseScreen.ttf',x=-.08,y=.45,text='Paused Game')

        self.ResumeGame = Button(radius=.2,text='Resume game',scale=(.18,.07),on_click=self.Resumegame,x=-.7,y=.2,z=-1.1,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.ResumeGame.text_entity.font='assets/textures/fonts/PauseScreen.ttf'

        self.ExitGame = Button(radius=.2,text='Exit game',scale=(.18,.07),x=-.7,on_click=self.CloseGame,y=0,z=-1.1,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.ExitGame.text_entity.font='assets/textures/fonts/PauseScreen.ttf'

        #Options
        if playerController.mouse_sensitivity == Vec2(10, 10):
            self.mouseSens=1
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='1 ₂ ₃ ₄ ₅ ₆ ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(20, 20):
            self.mouseSens=2
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ 2 ₃ ₄ ₅ ₆ ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(30, 30):
            self.mouseSens=3
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ 4 ₄ ₅ ₆ ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(40, 40):
            self.mouseSens=4
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ 4 ₅ ₆ ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(50, 50):
            self.mouseSens=5
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ ₄ 5 ₆ ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(60, 60):
            self.mouseSens=6
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ ₄ ₅ 6 ₇ ₈')
        elif playerController.mouse_sensitivity == Vec2(70, 70):
            self.mouseSens=7
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ ₄ ₅ ₆ 7 ₈')
        elif playerController.mouse_sensitivity == Vec2(80, 80):
            self.mouseSens=8
            self.sensText=Text(ignore=False,parent=camera.ui,font='assets/textures/fonts/Text.ttf',scale=2,y=.025,x=.02,text='₁ ₂ ₃ ₄ ₅ ₆ ₇ 8')
                
        
        self.UI = Entity(parent=camera.ui)
        
        self.volume_slider = Slider(step=1,parent=self.UI,min=0, max=100, default=int(app.sfxManagerList[0].getVolume()*100), dynamic=True,position=(0,.3),text='Master volume:',on_value_changed = self.set_volume)
        self.volume_slider.ignore_paused=True;self.volume_slider.knob.ignore_paused=True;self.volume_slider.label.ignore_paused=True

        self.sensDecrease = Button(text='e',radius=.3,x=-.1,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.sensDecrease.on_click = self.decreaseSens
        self.sensDecrease.text_entity.use_tags=False;self.sensDecrease.text = '<'

        self.sensTitle=Text(ignore=False,parent=camera.ui,scale=1.5,y=.1,x=.04,text='Sensitivity')

        self.sensIncrease = Button(text='e',radius=.3,x=.4,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.sensIncrease.on_click = self.increaseSens
        self.sensIncrease.text_entity.use_tags=False;self.sensIncrease.text = '>'

        self.keybinds=Button(text='Show key binds',y=-.2,x=.1,radius=.3,parent=self.UI,color=self.btnColor,scale=(.3,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.keybinds.on_click=self.keybind

        self.Entities = [self.startAudio,self.clickAudio,self.UI,self.volume_slider,
        self.sensDecrease,self.sensIncrease,self.sensText,self.sensTitle,self.title,
        self.keybinds,self.keybinds,self.click2Audio,self.ExitGame,self.ResumeGame]

        for e in self.Entities:
            e.ingore_paused = True
            for x in e.children:
                x.ignore_paused=True

    def CloseGame(self):
        Background = Entity(parent=camera.ui,model='quad', color=color.gray,scale=(.8,.4),z=-10)
        AreYouSure = Text(parent=camera.ui,text='Are you sure?',x=-.05,y=.15,z=-20)
        Yes = Button(text='yes',scale_x=.2,scale_y=.1,x=-.15,on_click=Func(application.quit),color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,z=-20)
        No = Button(text='No',scale_x=.2,scale_y=.1,x=.15,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,z=-20)
        def ClosePromt():
            destroy(No)
            destroy(Yes)
            destroy(AreYouSure)
            destroy(Background)
        No.on_click=ClosePromt

    def Resumegame(self):
        global PauseScreen
        for e in self.Entities:
            destroy(e)
        destroy(self)
        PauseScreen = None
        playerController.cursor.enabled = True
        mouse.locked=True
        application.resume()

    def increaseSens(self):
        if self.mouseSens < 8:
            self.mouseSens += 1
            match self.mouseSens:
                case 2:
                    self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (20,20)
                case 3:
                    self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (30,30)
                case 4:
                    self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (40,40)
                case 5:
                    self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (50,50)
                case 6:
                    self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                    playerController.mouse_sensitivity = (60,60)
                case 7:
                    self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                    playerController.mouse_sensitivity = (70,70)
                case 8:
                    self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ ₇ 8'
                    playerController.mouse_sensitivity = (80,80)
            self.click2Audio.play()

    def decreaseSens(self):
        if self.mouseSens > 1:
            self.mouseSens -= 1
            match self.mouseSens:
                case 1:
                    self.sensText.text = '1 ₂ ₃ ₄ ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (10,10)
                case 2:
                    self.sensText.text = '₁ 2 ₃ ₄ ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (20,20)
                case 3:
                    self.sensText.text = '₁ ₂ 3 ₄ ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (30,30)
                case 4:
                    self.sensText.text = '₁ ₂ ₃ 4 ₅ ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (40,40)
                case 5:
                    self.sensText.text = '₁ ₂ ₃ ₄ 5 ₆ ₇ ₈'
                    playerController.mouse_sensitivity = (50,50)
                case 6:
                    self.sensText.text = '₁ ₂ ₃ ₄ ₅ 6 ₇ ₈'
                    playerController.mouse_sensitivity = (60,60)
                case 7:
                    self.sensText.text = '₁ ₂ ₃ ₄ ₅ ₆ 7 ₈'
                    playerController.mouse_sensitivity = (70,70)
            self.click2Audio.play()

    def keybind(self):
        for e in self.Entities:
            e.enabled=False
        Keybinds(egg=self)
      
    def set_volume(self):
        volume = self.volume_slider.value/100
        app.sfxManagerList[0].setVolume(volume)

window.title = "ChronoGate"

app=Ursina(borderless=False,vsync=60,development_mode=False,fullscreen=False)
window.entity_counter.enabled=False
window.collider_counter.enabled=False
with open("pyfiles/Scripts/Functions.py", "r") as f:
    exec(f.read())

Sky(texture='assets/textures/misc/sky.jpg')

enemyTimestopped = False
PlayerSensitvity=(40,40)
menu=MenuScreen()
PauseScreen = False
def input(key):
    global PauseScreen
    if key == 'escape':
        if PauseScreen is None:
            PauseScreen = PauseMenuScreen()
app.run()