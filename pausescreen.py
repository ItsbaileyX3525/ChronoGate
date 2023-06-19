from ursina import *

class Keybinds(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.parent=camera.ui
        self.model='quad'
        self.color=color.gray
        self.scale_x=2
        self.z=-1
        with open('assets/data/controls.json') as file:
            self.data = json.load(file)
            
        self.key_exceptions = ['left mouse down', 'left mouse hold', 'left mouse up', 'escape', 'double click', 'right mouse down',
        'right mouse hold', 'right mouse up']    
        
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
        self.ButtonW = Button(radius=.2,text=self.w,scale=(.15,.07),x=.4,y=.4,on_click = Func(self.ChangeLetter, 'w'),z=-1.1)
        self.ButtonWText = Text(text='Walk Forward',y=.4,x=-.2,z=-1.1)
        self.ButtonW.text_entity.use_tags=False
        self.ButtonA = Button(radius=.2,text=self.a,scale=(.15,.07),x=.4,y=.3,on_click = Func(self.ChangeLetter, 'a'),z=-1.1)
        self.ButtonAText = Text(text='Strafe Left',y=.3,x=-.2,z=-1.1)
        self.ButtonA.text_entity.use_tags=False
        self.ButtonS = Button(radius=.2,text=self.s,scale=(.15,.07),x=.4,y=.2,on_click = Func(self.ChangeLetter, 's'),z=-1.1)
        self.ButtonSText = Text(text='Walk Backwards',y=.2,x=-.2,z=-1.1)
        self.ButtonS.text_entity.use_tags=False
        self.ButtonD = Button(radius=.2,text=self.d,scale=(.15,.07),x=.4,y=.1,on_click = Func(self.ChangeLetter, 'd'),z=-1.1)
        self.ButtonDText = Text(text='Strafe Right',y=.1,x=-.2,z=-1.1)
        self.ButtonD.text_entity.use_tags=False
        self.ButtonWSeq = Sequence(Wait(.25),Func(setattr, self.ButtonW, "text", f"> {self.data['W']} <"), Wait(.25),Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">   {self.data['W']}   <"),Wait(.25), Func(setattr, self.ButtonW, "text", f">  {self.data['W']}  <"),loop=True)
        self.ButtonASeq = Sequence(Wait(.25),Func(setattr, self.ButtonA, "text", f"> {self.data['A']} <"), Wait(.25),Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">   {self.data['A']}   <"),Wait(.25), Func(setattr, self.ButtonA, "text", f">  {self.data['A']}  <"),loop=True)
        self.ButtonSSeq = Sequence(Wait(.25),Func(setattr, self.ButtonS, "text", f"> {self.data['S']} <"), Wait(.25),Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">   {self.data['S']}   <"),Wait(.25), Func(setattr, self.ButtonS, "text", f">  {self.data['S']}  <"),loop=True)
        self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)
        
        self.ButtonLeave = Button(radius=.2,text='Exit',scale=(.15,.07),y=-.4,on_click = self.LeaveKeybinds,z=-1.1)
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
                self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)
            elif key in self.execpt:
                self.changeD = False
                self.ButtonDSeq.kill()
                self.ButtonD.text = self.data['D']
                self.ButtonDSeq = Sequence(Wait(.25),Func(setattr, self.ButtonD, "text", f"> {self.data['D']} <"), Wait(.25),Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">   {self.data['D']}   <"),Wait(.25), Func(setattr, self.ButtonD, "text", f">  {self.data['D']}  <"),loop=True)
        with open('assets/data/controls.json', 'w') as file:
            json.dump(self.data, file,indent=4)

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

    def input(self,key):
        global PauseScreen
        if key=='escape' and PauseScreen is not None:
            PauseScreen=None
            for e in self.Entities:
                destroy(e)
            destroy(self)
app=Ursina()

PauseScreen = None

def input(key):
    global PauseScreen
    if key == 'escape':
        if PauseScreen is None:
            PauseScreen = MenuScreen()

app.run()