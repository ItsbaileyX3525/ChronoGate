from ursina import *
from ursina.prefabs.first_person_controller import *
import threading

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #General player stuff
        self.HitPoints = 100
        self.ManaPoints = 20
        
        #Head bobbing crap
        self.bobbing_amount = 0.1
        self.bobbing_speed = 0.1
        self.bobbing_timer = 0.0
        
        #Spells & stuff
        self.CurrentEquiped = 'TimeStop'
        self.SpellEquiped = Text(text='Current spell: None',x=-.87,y=-.45)
        self.Spells = ['TimeStop', ]
        self.Timestop = TimeStop()
        
        #Audios for the player
        self.normalFootSteps=Audio('assets/audio/player/footslow.ogg',autoplay=False,loop=False,volume=.5)
        self.sprintFootSteps=Audio('assets/audio/player/footfast.ogg',autoplay=False,loop=False,volume=.5)

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

    def update(self):
        if self.HitPoints <= 0:
            print("Dead")
        if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
            self.bobbing_timer += self.bobbing_speed
            vertical_offset = abs(math.sin(self.bobbing_timer)) * self.bobbing_amount
            camera.y = vertical_offset
            if not self.normalFootSteps.playing:
                self.normalFootSteps.play()
            if held_keys['shift']:
                if held_keys['w']:
                    if self.normalFootSteps.playing:
                        self.normalFootSteps.stop()
                    if not self.sprintFootSteps.playing:
                        self.sprintFootSteps.play()
                    playerController.speed=16
                    self.bobbing_speed=.2
                elif held_keys['s']:
                    if self.normalFootSteps.playing:
                        self.normalFootSteps.stop()
                    if not self.sprintFootSteps.playing:
                        self.sprintFootSteps.play()
                    playerController.speed=12
                    self.bobbing_speed=.15
            else:
                self.sprintFootSteps.stop()
                playerController.speed = 8
                self.bobbing_speed=.1
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
        self.controlsP = Entity(position=(2,-0.2),parent=camera.ui)

        self.UI = Entity(parent=camera.ui)

        self.WormholeTravel = Entity(model='quad',parent=camera.ui,visible=False,texture='assets/textures/menu/menu.mp4',scale_y=1,scale_x=2)
        self.blackScreen = Entity(model='quad',color=color.black, scale=213,alpha=0)

        self.keyboard = Entity(model='quad',parent=camera.ui,visible=False,texture='assets/textures/menu/keyboard.png',z=-10,scale=[1.78,1])
        self.exitKeyboard = Button(visible=False,x=.85,y=.45,radius=.3,z=-11,parent=self.UI,scale=(.05,.05),text='X',text_color=color.black,color=color.red,highlight_color=color.red,highlight_scale=1.2,pressed_scale=1.07,pressed_color=color.red)
        self.exitKeyboard.on_click = self.Keyboard

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

        self.controls=Button(text='Show controls',radius=.3,parent=self.UI,color=self.btnColor,scale=(.3,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.controls.on_click=self.Keyboard
        self.controls.add_script(SmoothFollow(target=self.controlsP,speed=6))

        self.shopMenu = Button(radius=.3,scale=1,color=color.clear,z=3,text='<scale:2>Main credits\n\n\n<scale:1>Coding: Bailey\n\nGame design: Bailey\n\nEverything else: Bailey\n\nSmooth menu animations: @Code3D_ (yt)\n\n\n\n<scale:2>Special thanks<scale:1>\n\n\n- RangerRhino23\n\n\n\n\n<scale:.8>Why RangerRhino23? - Because I can and I did.')
        self.shopMenu.add_script(SmoothFollow(target=self.shopMenuP,speed=6))

        #Destroy all entites related to the menu
        self.EntitiesA = [self.startAudio,self.clickAudio,self.optMenuP,self.optionsGameBTN,
        self.UI,self.shopMenuP,self.titleScreen,self.newGameBTN,self.shopGameBTN,self.shopMenu,self.shopMenuP,
        self.quitGameBTN,self.volume_slider,self.volume_sliderP,self.sensDecrease,self.sensDecreaseP,self.sensIncrease,
        self.sensIncreaseP,self.sensText,self.sensTextP,self.sensTitle,self.sensTitleP,self.keyboard,self.exitKeyboard,
        self.controlsP,self.controls]

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
        global GROUND,player,playerController,enemyOne
        self.blackScreen.fade_out(duration=.8)
        destroy(self.WormholeTravel)
        destroy(self)
        self.s4.pause()
        player=Player()
        playerController=FirstPersonController()
        playerController.mouse_sensitivity = PlayerSensitvity
        enemyOne = EnemyNormal(x=20)
        GROUND=Entity(model='plane',scale=1000,texture='grass',texture_scale=(32,32),collider='box')

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
            self.controlsP.position = (.125,-0.2)

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
            self.controlsP.position=(2,-0.2)

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
            self.controlsP.position = (.125,-0.2)
            
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
            self.controlsP.position=(2,-0.2)

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

window.title = "ChronoGate"

app=Ursina(borderless=False,vsync=60,development_mode=False,use_ingame_console=True,fullscreen=False)
window.entity_counter.enabled=False
window.collider_counter.enabled=False
with open("pyfiles/Scripts/Functions.py", "r") as f:
    exec(f.read())

Sky(texture='assets/textures/misc/sky.jpg')

enemyTimestopped = False
PlayerSensitvity=(40,40)
menu=MenuScreen()
def input(key):
    if held_keys['control'] and key=='h':
        window.console.text_field.enabled = not window.console.text_field.enabled
window.console.text_input = "Fuckyoubatman"
window.console.text_field.enabled = not window.console.text_field.enabled
app.run()