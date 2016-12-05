import pygame
import time
import random
import __init__
import Util

pygame.init()
pygame.joystick.Joystick(0).init()
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Happy Tree Friends')

#icon = pygame.image.load("apple.png")
#pygame.display.set_icon(icon)

white = (255,255,255)
black = (0,0,0)


red = (180,0,0)
light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

green = (34,177,76)
light_green = (0,255,0)

dificil = 1
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("happytreefriends.ttf", 25)
medfont = pygame.font.SysFont("happytreefriends.ttf",50)
largefont = pygame.font.SysFont("happytreefriends.ttf", 80)



def score(score):

    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])


def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)


def button(text, x, y, width, height, inactive_color, active_color,posicion,seleccionado,dificil, action = None): 
	click = pygame.mouse.get_pressed()
	if posicion ==seleccionado:
		pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
		if (pygame.joystick.Joystick(0).get_button(2) or click[0]) and action != None:
			if action == "quit":
				pygame.quit()
				quit()
			if action == "dif":
				dificil+=1;
				if dificil > 2:
					dificil = 1

			if action == "play":
				__init__.inicio()
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))
	text_to_button(text,black,x,y,width,height)
	return dificil

#def button(text, x, y, width, height, inactive_color, active_color,posicion,seleccionado, action = None):
    #cur = pygame.mouse.get_pos()
    #click = pygame.mouse.get_pressed()
    
    
    ##print(click)
    #if (x + width > cur[0] > x and y + height > cur[1] > y) or (posicion ==seleccionado):
        #pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        #if (click[0] == 1 or pygame.joystick.Joystick(0).get_button(1)) and action != None:
            #if action == "quit":
                #pygame.quit()
                #quit()

            #if action == "controls":
                #pass

            #if action == "play":
                ##gameLoop()
                #__init__.inicio()

    #else:
        #pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    #text_to_button(text,black,x,y,width,height)


#def pause():

	#paused = True
	#gameDisplay.fill((255,255,255))
	#message_to_screen("Pausa",black,-100,size="large")
	#message_to_screen("presiona C para continuar jugando o Q para salir",black,25)
    ##pygame.display.update()
	#while paused:
		#for event in pygame.event.get():
			#if event.type == pygame.QUIT:
				#pygame.quit()
				#quit()
                ##fdsf
			#if pygame.joystick.Joystick(0).get_button(9):
                ##if event.type == pygame.KEYDOWN:
                 ##   if event.key == pygame.K_c:
				#paused = False
                  ##  elif event.key == pygame.K_q:
                   ##     pygame.quit()
                    ##    quit()
			#if pygame.joystick.Joystick(0).get_button(8):
				#game_intro()
			

		#pygame.display.update()
		#clock.tick(5)


def game_intro():
	global dificil
	intro = True
	total_opciones = 3
	seleccionado=0
	#dificil=1
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:		
				if event.key == pygame.K_c:
					intro = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()
			if pygame.joystick.Joystick(0).get_hat(0) == (1, 0) and seleccionado < total_opciones-1:
				seleccionado+=1
			if pygame.joystick.Joystick(0).get_hat(0) == (-1, 0)and seleccionado > 0:
				seleccionado-=1		
					
					
			
		background = Util.imagen("back/menux.png",False)
		gameDisplay.blit(background, (0, 0))
        #gameDisplay.blit(fondo,(0,0))
		message_to_screen("Cuddles's Nightmares",green,-100,size="large")
		message_to_screen("Ayudemos a nuestro querido",black,-30)
		message_to_screen("cuddles a sobrevir a sus ",black,10)
		message_to_screen("desquisiados amigos",black,50)
        #message_to_screen("Press C to play, P to pause or Q to quit",black,180)
		
		button("Jugar", 150,500,100,50, green, light_green,seleccionado,0,dificil, action="play")
		dificil=button("Modo", 350,500,100,50, yellow, light_yellow,seleccionado,1,dificil, action="dif")
		button("Salir", 550,500,100,50, red, light_red,seleccionado,2,dificil, action ="quit")
		if dificil ==1:
			message_to_screen("Modo: Facil",black,180)
		if dificil == 2:
			message_to_screen("Modo: Dificil",black,180)


		pygame.display.update()

		clock.tick(30)

game_intro()


