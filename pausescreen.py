from ursina import *
from ursina.prefabs.first_person_controller import *
import json

class Keybinds(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.parent=camera.ui
        self.model='quad'
        self.color=color.gray
        self.scale_x=2
        self.z=-199
        with open('assets/data/controls.json') as file:
            self.data = json.load(file)

        self.key_exceptions = ['left mouse down', 'left mouse hold', 'left mouse up', 'escape', 'double click', 'right mouse down',
        'right mouse hold', 'right mouse up', '`', '` hold', '` up', "'","' up", "' hold", '#', '# up', '# hold', ']', '[', '=',
        '= up', '= hold', '-', '- up', '- hold', 'tab', 'tab up', 'tab hold', ',', ', up', ', hold', '.', '. up', '. hold']

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

class PauseMenuScreen(Entity):
    def __init__(self, add_to_scene_entities=False, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.Entities = []
        self.model='quad'
        self.color=color.black
        self.alpha=.5
        self.scale=[16,9]
        mouse.locked=False
        playerController.cursor.enabled = False
                
        self.startAudio = Audio('assets/audio/menu/start.ogg',autoplay=False,loop=False)
        self.clickAudio = Audio('assets/audio/menu/click.ogg',autoplay=False,loop=False)
        self.click2Audio = Audio('assets/audio/menu/click1.ogg',autoplay=False,loop=False)
        
        self.btnColor = rgb(0,0,0,30)
        self.btnHcolor = rgb(0,0,0,50)

        self.title = Text(font='assets/textures/fonts/PauseScreen.ttf',x=-.08,y=.45,text='Paused Game')

        self.ResumeGame = Button(radius=.2,text='Resume game',scale=(.18,.07),on_click=self.Resumegame,x=-.7,y=.2,z=-1.1,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.ResumeGame.text_entity.font='assets/textures/fonts/PauseScreen.ttf'

        self.Options = Button(radius=.2,text='Options',scale=(.18,.07),x=-.7,on_click=self.OpenOptions,y=.05,z=-1.1,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
        self.Options.text_entity.font='assets/textures/fonts/PauseScreen.ttf'        

        self.ExitGame = Button(radius=.2,text='Exit game',scale=(.18,.07),x=-.7,on_click=self.CloseGame,y=-.1,z=-1.1,color=self.btnColor,highlight_color=self.btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=self.btnHcolor)
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
        self.keybinds,self.keybinds,self.click2Audio,self.ExitGame,self.Options,self.ResumeGame]

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

    def OpenOptions(self):
        pass

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

app=Ursina()

PauseScreen = None
playerController=FirstPersonController()
def input(key):
    global PauseScreen
    if key == 'escape':
        if PauseScreen is None:
            PauseScreen = PauseMenuScreen()

app.run()