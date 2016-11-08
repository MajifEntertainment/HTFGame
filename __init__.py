import pygame, sys, Util, tmx, glob
from pygame.locals import *
from Util import *
from tmx import *


class Game():
	def main(self, screen):
        # define el reloj dentro del juego
        
		clock = pygame.time.Clock()
        # carga la imagen de fondo
		background = Util.imagen("fondoJungla.png")
		self.map_counter = 1
        # carga los datos del mapa
		self.tilemap = tmx.load("level"+str(self.map_counter)+".tmx", screen.get_size())

		# carga los joysticks
		self.joyst=False
		joystick_count = pygame.joystick.get_count()
		if joystick_count != 0:
			self.joyst=True
			pygame.joystick.Joystick(0).init()
            
		
		
        # carga los datos de inicio del jugador
		self.sprites = tmx.SpriteLayer()
		start_cell = self.tilemap.layers["triggers"].find("player")[0]
		self.player = Player((start_cell.px, start_cell.py), self.sprites)
		self.tilemap.layers.append(self.sprites)
		
        # carga los datos de inicio de los enemigos
		self.enemies = tmx.SpriteLayer()
		for enemy in self.tilemap.layers["triggers"].find("enemy"):
			Enemy((enemy.px, enemy.py), self.enemies)

		self.tilemap.layers.append(self.enemies)
        
        
        # ciclo infinito del juego
		while 1:
			dt = clock.tick(30) 
			 # verifica si el juego es quitado
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
				    return
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return
			
            # comienza a dibujar el mapa y a los personajes
			self.tilemap.update(dt / 1000., self,screen)
			screen.blit(background, (0, 0))
			self.tilemap.draw(screen)
            # muestra el numero de vidas del jugador
			text(screen, "Lives: " + str(self.player.lifes), (255, 255, 0), 50, 20, 25)
			# despliega la version del juego
			text(screen, "alpha petunia 0.0.11", (0, 0, 0), 700, 580, 15)  
			pygame.display.flip()

			self.player.changeY -= 3

            # verifica si el jugador a llegado al final del nivel
			if self.player.finish == True:
				self.player.finish=False
				self.map_counter+=1
				self.tilemap = tmx.load("level"+str(self.map_counter)+".tmx", screen.get_size())
				 # carga los datos de inicio del jugador
				self.sprites = tmx.SpriteLayer()
				start_cell = self.tilemap.layers["triggers"].find("player")[0]
				self.player = Player((start_cell.px, start_cell.py), self.sprites)
				self.tilemap.layers.append(self.sprites)
				
				# carga los datos de inicio de los enemigos
				self.enemies = tmx.SpriteLayer()
				for enemy in self.tilemap.layers["triggers"].find("enemy"):
					Enemy((enemy.px, enemy.py), self.enemies)

				self.tilemap.layers.append(self.enemies)
				
            # verifica si el jugador a perdido todas sus vidas
			if self.player.lifes == 0:
				text(screen, "YOU DIED", (0, 0, 0), (640 / 2), (180 / 2), 115)
				pygame.display.update()
				clock.tick(60)
				return
				
# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
   image = pygame.image.load("enemy.png")
   def __init__(self, location, *groups):
       super(Enemy, self).__init__(*groups)
       self.rect = pygame.rect.Rect(location, self.image.get_size())
       self.direction = 1;

   def update(self, dt, game,screen):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers["triggers"].collide(self.rect, "reverse"):
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break
        # verifica si el jugador choca con el enemigo, le resta una vida al jugador y destruye al enemigo
        if self.rect.colliderect(game.player.rect):

            game.player.lifes -= 1
            self.kill()
         

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
        # carga las imagenes que corresponden al personaje jugador
		
		
		self.player_current = 0
		self.right_images=[]
		self.right_images.append(Util.imagen('sprites/petunia_right.000.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.001.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.002.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.003.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.004.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.005.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.006.png',True) )
		self.left_images = []
		self.left_images.append(Util.imagen('sprites/petunia_left.000.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.001.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.002.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.003.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.004.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.005.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.006.png',True) )
		self.image = self.right_images[self.player_current]
		
		self.rect = pygame.rect.Rect(location, self.image.get_size())
        # variable que sabe si el personaje esta tocando el suelo
		self.resting = False

        # contiene el delta y (la variente de y en el tiempo, para efectos del salto)
		self.dy = 0
		self.lifes = 3
		self.direction = "right"
		self.finish = False
		self.changeY = self.rect.y + 90
		self.wallJump = False
		self.walking = False
		self.walking_steps = 5

    def update(self, dt, game,screen):
		
		last = self.rect.copy()
        # verifica si se presiona alguna tecla
		
		if game.joyst == True:
		
			# mueve al personaje a la izquierda
			if pygame.joystick.Joystick(0).get_hat(0) == (-1, 0): 
				self.walking=True
				self.rect.x -= 300 * dt
				self.direction = "left"
				
			# mueve al personaje a la derecha
			if pygame.joystick.Joystick(0).get_hat(0) == (1, 0):
				self.walking=True
				self.rect.x += 300 * dt
				self.direction = "right"     
			if pygame.joystick.Joystick(0).get_hat(0) == (0, 0):
				self.walking = False
			# hace que el personaje salte
			if (self.resting and pygame.joystick.Joystick(0).get_button(0)) or (self.wallJump and pygame.joystick.Joystick(0).get_button(0)):
				self.walking = False
				if self.direction == "right":
					self.image = self.right_images[1]
				elif self.direction == "left":
					self.image = self.left_images[1]
				self.dy = -500

			self.dy = min(400, self.dy + 40)
			self.rect.y += self.dy * dt
			new = self.rect
			self.resting = False
			
		elif game.joyst==False:
			key = pygame.key.get_pressed() 
			# mueve al personaje a la izquierda
			if key[pygame.K_LEFT]:
				self.walking=True
				self.rect.x -= 300 * dt
				self.direction = "left"
				
			# mueve al personaje a la derecha
			if key[pygame.K_RIGHT]:
				self.walking=True
				self.rect.x += 300 * dt
				self.direction = "right"     
			if (pygame.KEYUP and pygame.K_RIGHT) or (pygame.KEYUP and pygame.K_LEFT):
				self.walking = False
			# hace que el personaje salte
			if (self.resting and key[pygame.K_SPACE]) or (self.wallJump and key[pygame.K_SPACE]):
			
				self.walking = False
				if self.direction == "right":
					self.image = self.right_images[1]
				elif self.direction == "left":
					self.image = self.left_images[1]
				self.dy = -500

			self.dy = min(400, self.dy + 40)
			self.rect.y += self.dy * dt
			new = self.rect
			self.resting = False
		
        # verifica si el personaje esta o no chocando con los objetos bloqueadores(suelo, parades, etc.)
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				self.resting = True

			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				new.left = cell.right

				self.resting = True
			if "t" in blockers and last.bottom <= cell.top and new.bottom > cell.top:
				self.resting = True
				new.bottom = cell.top
				self.dy = 0
			if "b" in blockers and last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.dy = 0
				
		if self.walking == True:
			if self.direction == "right":
				
				if self.walking_steps > 0:
					
					self.player_current = (self.player_current + 1) % len(self.right_images)
					self.image = self.right_images[ self.player_current ]
					self.walking_steps -= 1
				else:
					self.walking = False
					self.walking_steps=5		
						
			elif self.direction == "left":
				
				if self.walking_steps > 0:
					self.player_current = (self.player_current + 1) % len(self.left_images)
					self.image = self.left_images[ self.player_current ]
					self.walking_steps -= 1
				else:
					self.walking = False	
					self.walking_steps=5	
        # hace que la camara siga al personaje
		#game.tilemap.set_focus(new.x, self.changeY)
		game.tilemap.set_focus(new.x, new.y)
		#if self.rect.y > self.changeY + 300:

			#self.lifes = 0
        
        # verifica si el personaje toca al trigger de salida
		for cell in game.tilemap.layers["triggers"].collide(new, "exit"):
			self.finish = True
        # verifica si el personaje activa el trigger de muerte
		for cell in game.tilemap.layers["triggers"].collide(new, "death"):
			self.lifes = 0

#clase del jefe
class Boss(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
        # carga las imagenes que corresponden al jefe
		
		
		self.player_current = 0
		self.right_images=[]
		self.right_images.append(Util.imagen('sprites/petunia_right.000.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.001.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.002.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.003.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.004.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.005.png',True) )
		self.right_images.append(Util.imagen('sprites/petunia_right.006.png',True) )
		self.left_images = []
		self.left_images.append(Util.imagen('sprites/petunia_left.000.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.001.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.002.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.003.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.004.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.005.png',True) )
		self.left_images.append(Util.imagen('sprites/petunia_left.006.png',True) )
		self.image = self.right_images[self.player_current]
		
		self.rect = pygame.rect.Rect(location, self.image.get_size())
        # variable que sabe si el personaje esta tocando el suelo
		self.resting = False
        # contiene el delta y (la variente de y en el tiempo, para efectos del salto)
		self.dy = 0
		self.lifes = 3
		self.direction = "right"
		self.finish = False
		self.changeY = self.rect.y + 90
		self.wallJump = False
		self.walking = False
		self.walking_steps = 5

    def update(self, dt, game, my_joystick,screen):
		
		last = self.rect.copy()
        # verifica si se presiona alguna tecla
		#key = pygame.key.get_pressed() 
        # mueve al personaje a la izquierda
		if my_joystick.get_hat(0) == (-1, 0):  # key[pygame.K_LEFT]:
			self.walking=True
			self.rect.x -= 300 * dt
			#self.image = self.left_image
			self.direction = "left"
			
        # mueve al personaje a la derecha
		if my_joystick.get_hat(0) == (1, 0):  # key[pygame.K_RIGHT]:
			self.walking=True
			self.rect.x += 300 * dt
			#self.image = self.right_image
			self.direction = "right"     
		if my_joystick.get_hat(0) == (0, 0):
			self.walking = False
        # hace que el personaje salte
		# if (self.resting and key[pygame.K_SPACE]) or (self.wallJump and key[pygame.K_SPACE]):
		if (self.resting and my_joystick.get_button(0)) or (self.wallJump and pygame.joystick.Joystick(0).get_button(0)):
			self.walking = False
			if self.direction == "right":
				self.image = self.right_images[1]
			elif self.direction == "left":
				self.image = self.left_images[1]
			self.dy = -500

		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt
		new = self.rect
		self.resting = False
		
        # verifica si el personaje esta o no chocando con los objetos bloqueadores(suelo, parades, etc.)
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				self.resting = True

			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				new.left = cell.right

				self.resting = True
			if "t" in blockers and last.bottom <= cell.top and new.bottom > cell.top:
				self.resting = True
				new.bottom = cell.top
				self.dy = 0
			if "b" in blockers and last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.dy = 0
				
		if self.walking == True:
			if self.direction == "right":
		       # here you need to check some counter 
		        # if it is time for next step to walk slower
		        # but don't use 'time.sleep()'
				print("right")
				if self.walking_steps > 0:
					
					self.player_current = (self.player_current + 1) % len(self.right_images)
					self.image = self.right_images[ self.player_current ]
					self.walking_steps -= 1
				else:
					self.walking = False
					self.walking_steps=5		
						
			elif self.direction == "left":
				print("left")
				if self.walking_steps > 0:
					self.player_current = (self.player_current + 1) % len(self.left_images)
					self.image = self.left_images[ self.player_current ]
					self.walking_steps -= 1
				else:
					self.walking = False	
					self.walking_steps=5	

def musica():
    pygame.mixer.music.load("musica/Happy tree friends 8-bit remix.mp3")  # sound file has to be in same folder/directory as
    # the file you are writing the music loading code into
    #pygame.mixer.music.play(-1, 0.0)
    return

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Tree Friends")
    musica()
    Game().main(screen)
