from ursina import *
app = Ursina()
#window.fullscreen=True
window.color=rgb(166, 150, 108)

btnX= 0.2
btnY = 0.075

btnColor= rgb(0,0,0,30)
btnHcolor= rgb(0,0,0,50)



def opt():
	newGameBTN.x=-0.75
	optMenuP.position=(0,0)
	shopMenuP.position=(2,0)

	optionsGameBTN.scale= (0.24,0.09)
	optionsGameBTN.color=(0,0,0,60)

	shopGameBTN.scale= (0.2,0.075)
	shopGameBTN.color=btnColor


def shop():
	newGameBTN.x=-0.75
	optMenuP.position=(2,0)
	shopMenuP.position=(0,0)

	shopGameBTN.scale= (0.24,0.09)
	shopGameBTN.color=(0,0,0,60)

	optionsGameBTN.scale= (0.2,0.075)
	optionsGameBTN.color=btnColor


def quit_():
	newGameBTN.x=0
	optMenuP.position=(2,0)
	shopMenuP.position=(2,0)

	optionsGameBTN.scale= (0.2,0.075)
	optionsGameBTN.color=btnColor

	shopGameBTN.scale= (0.2,0.075)
	shopGameBTN.color=btnColor



optMenuP= Entity(position=(2,0),parent=camera.ui)
shopMenuP= Entity(position=(2,0),parent=camera.ui)

UI = Entity(parent=camera.ui)


newGameBTN = Button(parent=UI,scale=(btnX,btnY),text='New Game',color=btnColor,highlight_color=btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=btnHcolor)


btnPosY1= newGameBTN.y
optionsGameBTN = Button(parent=UI,scale=(btnX,btnY),text='Options',color=btnColor,highlight_color=btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=btnHcolor,
			   y=0 )
optionsGameBTN.add_script(SmoothFollow(target=newGameBTN,speed=6,offset=[0,-1.55,0.75]))
optionsGameBTN.on_click=opt


btnPosY2= optionsGameBTN.y
shopGameBTN = Button(parent=UI,scale=(btnX,btnY),text='Shop',color=btnColor,highlight_color=btnHcolor,highlight_scale=1.2,pressed_scale=1.07,pressed_color=btnHcolor,
			   y= 0 )
shopGameBTN.add_script(SmoothFollow(target=optionsGameBTN,speed=6,offset=[0,-1.55,0.75]))
shopGameBTN.on_click=shop


btnPosY3= shopGameBTN.y
quitGameBTN = Button(parent=UI,scale=(btnX,btnY),text='Quit',color=btnColor,highlight_color=rgb(255,0,0,20),highlight_scale=1.2,pressed_scale=1.07,pressed_color=btnHcolor,
			   y=0 )
quitGameBTN.add_script(SmoothFollow(target=shopGameBTN,speed=6,offset=[0,-1.55,0.75]))
quitGameBTN.on_click=quit_



optMenu= Button(scale=1,z=3,text='Options',color=btnColor,highlight_color=btnColor)
optMenu.add_script(SmoothFollow(target=optMenuP,speed=6))

shopMenu= Button(scale=1,z=3,text='Shop',color=btnColor,highlight_color=btnColor)
shopMenu.add_script(SmoothFollow(target=shopMenuP,speed=6))


app.run()