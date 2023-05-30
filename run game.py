from ursina import *
from ursina.prefabs.first_person_controller import *

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.HitPoints = 100
        self.CurrentEquiped = 'TimeStop'
        self.ManaPoints = 20
        self.SpellEquiped = Text(text='Current spell: None',x=-.87,y=-.45)
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
    
    def update(self):
        if self.HitPoints <= 0:
            print("Dead")
        if held_keys['shift']:
            if held_keys['w']:
                playerController.speed = 16
            if held_keys['s']:
                playerController.speed = 12
        else:
            playerController.speed = 8
        self.SpellEquiped.text = f'Current spell: {self.CurrentEquiped}'

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
                self.pauseTime()
                print(f"Remaining mana: {player.ManaPoints}")
            elif not EnoughMana:
                print("Not enough mana")
                pass

    def pauseTime(self):
        global enemyTimestopped
        enemyTimestopped = True
    
    def resumeTime(self):
        global enemyTimestopped
        enemyTimestopped = False
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
                print("In range to attack")
        else:
            if not self.touchingBorder and not enemyTimestopped:
                self.position += self.forward * time.dt

class MenuScreen(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Entities = []
        
        self.startAudio = Audio('assets/audio/menu/start.ogg',autoplay=False,loop=False)
        self.clickAudio = Audio('assets/audio/menu/click.ogg',autoplay=False,loop=False)
        self.introAudio = Audio('assets/audio/menu/intro.ogg',autoplay=False,loop=False)
        self.oldSpiceAudio = Audio('assets/audio/menu/oldspice.mp3',autoplay=False,loop=False,volume=.5)
        
        self.TimerActive = False
        self.timer = 0
        self.canSkip = False
        self.skipTimer = 0
        self.canSkipText = Text(z=-2,visible=False,text="Hold 'e' to skip.",x=-.88,y=-.46)
        
        self.btnX = 0.2
        self.btnY = 0.075

        self.btnColor = rgb(0,0,0,30)
        self.btnHcolor = rgb(0,0,0,50)
        self.optMenuP = Entity(position=(2,0),parent=camera.ui)
        self.shopMenuP = Entity(position=(2,0),parent=camera.ui)
        self.volume_sliderP = Entity(position=(24,4),paret=camera.ui)
        self.sensDecreaseP = Entity(position=(0,0),parent=camera.ui)
        self.sensIncreaseP = Entity(position=(2,2),parent=camera.ui)

        self.UI = Entity(parent=camera.ui)
        
        self.WormholeTravel = Entity(model='quad',parent=camera.ui,visible=False,texture='assets/textures/menu/menu.mp4',scale_y=1,scale_x=2)
        self.blackScreen = Entity(model='quad',color=color.black, scale=213,alpha=0)
        
        self.titleScreen = Text(font='assets/textures/fonts/MainFont.ttf',text='ChronoGate',y=.4,x=-.185)

        self.newGameBTN = Button(radius=.3, parent=self.UI,scale=(self.btnX,self.btnY),text='Start Game',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.newGameBTN.on_click=self.Startgame

        self.btnPosY1 = self.newGameBTN.y
        self.optionsGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Options',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.optionsGameBTN.add_script(SmoothFollow(target=self.newGameBTN,speed=6,offset=[0,-1.55,0.75]))
        self.optionsGameBTN.on_click=self.opt

        self.btnPosY2 = self.optionsGameBTN.y
        self.shopGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Credits',color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0 )
        self.shopGameBTN.add_script(SmoothFollow(target=self.optionsGameBTN,speed=6,offset=[0,-1.55,0.75]))
        self.shopGameBTN.on_click=self.shop


        self.btnPosY3 = self.shopGameBTN.y
        self.quitGameBTN = Button(radius=.3,parent=self.UI,scale=(self.btnX,self.btnY),text='Quit',color=self.btnColor,highlight_color=rgb(255,0,0,20),highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y=0 )
        self.quitGameBTN.add_script(SmoothFollow(target=self.shopGameBTN,speed=6,offset=[0,-1.55,0.75]))
        self.quitGameBTN.on_click=self.quit_

        #After button clicked stuff
        self.volume_slider = Slider(parent=self.UI,min=0, max=100, default=100, dynamic=True,position=(-24,.3),text='Master volume:',on_value_changed = self.set_volume)
        self.volume_slider.add_script(SmoothFollow(target=self.volume_sliderP,speed=6))
        
        self.sensDecrease = Button(text='<',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensDecrease.add_script(SmoothFollow(target=self.sensDecreaseP,speed=6))
        
        self.sensIncrease = Button(text='>',radius=.3,parent=self.UI,color=self.btnColor,scale=(.05,.05),highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor,y= 0)
        self.sensIncrease.add_script(SmoothFollow(target=self.sensIncreaseP,speed=6))
        
        self.shopMenu = Button(radius=.3,scale=1,color=color.clear,z=3,text='Coding: Bailey\n\nGame design: Bailey\n\nEverything else: Bailey\n\nMenu: @Code3D_ (yt)')
        self.shopMenu.add_script(SmoothFollow(target=self.shopMenuP,speed=6))

        #Destroy all entites related to the menu
        self.EntitiesA = [self.startAudio,self.clickAudio,self.optMenuP,self.optionsGameBTN,
        self.UI,self.shopMenuP,self.titleScreen,self.newGameBTN,self.shopGameBTN,self.shopMenu,self.shopMenuP,
        self.quitGameBTN,self.volume_slider,self.volume_sliderP]
        
        self.Entities.extend(self.EntitiesA)

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
        self.WormholeTravel.fade_out(duration=1.3)
        self.blackScreen.fade_in(duration=1.3)
        destroy(self.canSkipText)
        invoke(self.startGame,delay=2)

    def startGame(self):
        global GROUND,player,playerController,enemyOne
        self.blackScreen.fade_out(duration=.8)
        destroy(self.WormholeTravel)
        self.s4.pause()
        player=Player()
        playerController=FirstPersonController()
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

            self.shopGameBTN.scale= (0.2,0.075)
            self.shopGameBTN.color = self.btnColor
        elif self.newGameBTN.x == -0.75 and self.optionsGameBTN.color == (0,0,0,60):
            #Switch to back credits
            self.newGameBTN.x = -0.75
            self.optMenuP.position = (2,0)
            self.shopMenuP.position = (0,0)

            self.shopGameBTN.scale = (0.24,0.09)
            self.shopGameBTN.color =(0,0,0,60)
            self.volume_sliderP.position = (24, 4)
            self.titleScreen.text = 'Credits'
            self.titleScreen.x = -.1

            self.optionsGameBTN.scale = (0.2,0.075)
            self.optionsGameBTN.color  =self.btnColor       


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
                self.skipTimer=0
            

window.title = "ChronoGate"
app=Ursina(borderless=False,vsync=60)
with open("pyfiles/Scripts/Functions.py", "r") as f:
    exec(f.read())

enemyTimestopped = False
menu=MenuScreen()
app.run()