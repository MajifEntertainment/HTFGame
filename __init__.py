import pygame, sys, Util, tmx, glob, ugu
from pygame.locals import *
from Util import *
from tmx import *


class Game():
	def main(self, screen):
		
        # define el reloj dentro del juego
		self.clock = pygame.time.Clock()
        #contador que sabe en que mapa se encuentra el jugador
		self.map_counter = 1
		self.boss_counter = 0
		#variable que se encarga de saber si el juego esta en pausa
		self.paused = False
        # carga los datos del mapa
		self.tilemap = tmx.load("level"+str(self.map_counter)+".tmx", screen.get_size())
		# carga la imagen de fondo
		background = Util.imagen("back/fondo"+str(self.map_counter)+".png")
		# carga los joysticks
		self.joyst=False
		joystick_count = pygame.joystick.get_count()
		if joystick_count != 0:
			self.joyst=True
			pygame.joystick.Joystick(0).init()
		self.mode = False
		if ugu.dificil == 2:
			self.mode=True
		self.name=""
        # carga los datos de inicio del jugador
		self.sprites = tmx.SpriteLayer()
		start_cell = self.tilemap.layers["triggers"].find("player")[0]
		self.player = Player((start_cell.px, start_cell.py), self.sprites)
		if self.map_counter== 2 or self.map_counter==4:
			self.boss_counter+=1
			if self.map_counter == 1:
				self.name="flippy"
			if self.map_counter == 2:
				self.name="nutty"	
			start_cell_boss = self.tilemap.layers["triggers"].find("boss")[0]
			self.boss = Boss((start_cell_boss.px, start_cell_boss.py),self.name, self.sprites)
		
		self.tilemap.layers.append(self.sprites)
		
        # carga los datos de inicio de los enemigos
		self.enemies = tmx.SpriteLayer()
		for enemy in self.tilemap.layers["triggers"].find("enemy"):
			Enemy((enemy.px, enemy.py), self.enemies)
		self.tilemap.layers.append(self.enemies)
		
		# carga los items que dan puntos
		#for itemS in self.tilemap.layers["triggers"].find("itemS"):
		#	itemSmall((itemS.px, itemS.py), self.itemS)
		#self.tilemap.layers.append(self.itemS)
		
		#for itemB in self.tilemap.layers["triggers"].find("itemB"):
		#	itemBig((itemB.px, itemB.py), self.itemB)
		#self.tilemap.layers.append(self.itemB)
		              
        # ciclo infinito del juego
		while 1:
			dt = self.clock.tick(30) 
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				    return
				if pygame.joystick.Joystick(0).get_button(9):
					pause(self)
			
	        # comienza a dibujar el mapa y a los personajes
			self.tilemap.update(dt / 1000., self,screen)
			screen.blit(background, (0, 0))
			self.tilemap.draw(screen)
			# muestra el numero de vidas del jugador
			screen.blit(self.player.healthbar.image,(20,20))
			if self.map_counter== 2 or self.map_counter==4:
				screen.blit(self.boss.healthbar.image,(600,20))
			# muestra el puntaje del jugador
			text(screen, "Score" , (255, 255, 0), 400,20, 25)
			text(screen, str(self.player.points) , (255, 255, 0), 400,50, 25)
			# despliega la version del juego
			text(screen, "alpha ShanWan/scrot 0.2.1", (0, 0, 0), 700, 580, 15)  
			pygame.display.flip()
			self.player.changeY -= 3
	
	        # verifica si el jugador a llegado al final del nivel
			if self.player.finish == True and self.map_counter !=4:
				self.player.finish=False
				self.map_counter+=1
				self.tilemap = tmx.load("level"+str(self.map_counter)+".tmx", screen.get_size())
				background = Util.imagen("back/fondo"+str(self.map_counter)+".png")
				# carga los datos de inicio del jugador
				self.sprites = tmx.SpriteLayer()
				start_cell = self.tilemap.layers["triggers"].find("player")[0]
				self.player = Player((start_cell.px, start_cell.py), self.sprites)
				
				#carga los datos de inicio del boss solo si se encuentra en un mapa de jefe
				if self.map_counter== 2 or self.map_counter==4:
					self.boss_counter+=1
					if self.boss_counter == 1:
						self.name="flippy"
					if self.boss_counter == 2:
						self.name="nutty"	
					start_cell_boss = self.tilemap.layers["triggers"].find("boss")[0]
					self.boss = Boss((start_cell_boss.px, start_cell_boss.py),self.name, self.sprites)
					
				self.tilemap.layers.append(self.sprites)
				# carga los datos de inicio de los enemigos
				self.enemies = tmx.SpriteLayer()
				for enemy in self.tilemap.layers["triggers"].find("enemy"):
					Enemy((enemy.px, enemy.py), self.enemies)
	
				self.tilemap.layers.append(self.enemies)
			elif self.player.finish == True and self.map_counter ==4:
				text(screen, "YOU WIN", (0, 0, 0), (640 / 2), (180 / 2), 115)
				pygame.display.update()
				ugu.game_intro()	
			def pause(self):
				self.paused = True
				
				while self.paused:
					for event in pygame.event.get():
						if event.type == pygame.QUIT or pygame.joystick.Joystick(0).get_button(9):
							return
					if pygame.joystick.Joystick(0).get_button(8):
						ugu.game_intro()	
					#reemplzar por un fondo
					backPausa = Util.imagen("back/menux.png",False)
					screen.blit(backPausa, (0, 0))
					text(screen,"PAUSE",(0,0,0),(640 / 2), (180 / 2), 115)
					pygame.display.update()
					self.clock.tick(30)
					
#clase de las barras de vida
class Healthbar(pygame.sprite.Sprite):
	def __init__(self,owner,lives, *groups):
		super(Healthbar, self).__init__(*groups)
		self.matImages = []
		for i in range(lives):
			self.matImages.append(Util.imagen("sprites/lifebars/barra"+owner+str(i)+".png",True) )
		self.image = self.matImages[1]
		self.rect = pygame.rect.Rect((500,500), self.image.get_size())
	def update(self,owner):
		self.image = self.matImages[owner.lives-1]
		
		
				 
# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
   def __init__(self, location, *groups):
       super(Enemy, self).__init__(*groups)
       self.image_right = Util.imagen("sprites/bombaright.png",True)
       self.image_left = pygame.transform.flip(self.image_right,True,False)
       self.image = self.image_right
       self.rect = pygame.rect.Rect(location, self.image.get_size())
       self.direction = 1;
       

   def update(self, dt, game,screen):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers["triggers"].collide(self.rect, "reverse"):
            if self.direction > 0:
                self.rect.right = cell.left
                self.image = self.image_left
            else:
                self.rect.left = cell.right
                self.image=self.image_right
            self.direction *= -1
            break
        # verifica si el jugador choca con el enemigo, le resta una vida al jugador y destruye al enemigo
        if self.rect.colliderect(game.player.rect):
			if game.player.direction == "right":
				game.player.rect.x-=800*dt
			elif game.player.direction == "left":
				game.player.rect.x+=800*dt	
			game.player.lives -= 1
			game.player.points -=50
			self.kill()
			
# Clase item pocos puntos        
class ItemSmall(pygame.sprite.Sprite):
	def __init__(self, location,*group):
		image = pygame.image.load("sprites/items/itemSmall.png")
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		
	def update(self, dt, game,screen):
		if 	self.rect.colliderect(game.player.rect):
			self.kill()
			game.player.points+=50
			
# Clase item muchos puntos        
class ItemBig(pygame.sprite.Sprite):
	def __init__(self, location,*group):
		image = pygame.image.load("sprites/items/itemBig.png")
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		
	def update(self, dt, game,screen):
		if 	self.rect.colliderect(game.player.rect):
			self.kill()
			game.player.points+=150			

# Clase item de vida       
class ItemHeal(pygame.sprite.Sprite):
	def __init__(self, location,*group):
		image = pygame.image.load("sprites/items/itemHeal.png")
		self.rect = pygame.rect.Rect(location, self.image.get_size())
		
	def update(self, dt, game,screen):
		if 	self.rect.colliderect(game.player.rect) and game.player.lives<3:
			self.kill()
			game.player.points+=10
			game.player.lives+=1

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
		super(Player, self).__init__(*groups)
        # carga las imagenes que corresponden al personaje jugador	
		self.player_current = 0
		self.right_images=[]
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.000.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.001.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.002.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.003.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.004.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.005.png',True) )
		self.right_images.append(Util.imagen('sprites/cuddles/cuddles_right.006.png',True) )
		self.left_images = []
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.000.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.001.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.002.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.003.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.004.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.005.png',True) )
		self.left_images.append(Util.imagen('sprites/cuddles/cuddles_left.006.png',True) )
		self.image = self.right_images[self.player_current]
		self.blood=[]
		self.blood.append(Util.imagen('sprites/death/blood0.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood1.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood2.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood3.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood4.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood5.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood6.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood7.png',True) )
		self.blood.append(Util.imagen('sprites/death/blood8.png',True) )
		self.name = "cuddles"
		self.points =0
		self.rect = pygame.rect.Rect(location, self.image.get_size())
        # variable que sabe si el personaje esta tocando el suelo
		self.resting = False

        # contiene el delta y (la variente de y en el tiempo, para efectos del salto)
		self.dy = 0
		self.lives = 3
		self.direction = "right"
		self.finish = False
		self.changeY = self.rect.y + 60
		self.walking = False
		self.walking_steps = 5
		self.jumpSound = pygame.mixer.Sound("sounds/jump.wav")
		self.cooldown = 0;
		self.healthbar = Healthbar(self.name,self.lives)

    def update(self, dt, game,screen):
		self.healthbar.update(self)
		last = self.rect.copy()		
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
		if self.resting and pygame.joystick.Joystick(0).get_button(2):
			self.walking = False
			self.resting = False	
			if self.direction == "right":
				self.image = self.right_images[1]
			elif self.direction == "left":
				self.image = self.left_images[1]
			self.dy = -650
			self.jumpSound.play()
				
		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt
		new = self.rect
		self.resting = False
		# hace que el personaje dispare	
		if pygame.joystick.Joystick(0).get_button(1) and not self.cooldown:
			if self.direction == "right":
				Bullet(self.rect.midright, 1, game.sprites)
			else:
				Bullet(self.rect.midleft, -1, game.sprites)
			self.cooldown = 1
		self.cooldown = max(0, self.cooldown -dt)
		
        # verifica si el personaje esta o no chocando con los objetos bloqueadores(suelo, parades, etc.)
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				

			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				new.left = cell.right

				
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
		
		if self.lives == 0:
			
			for i in range(8):
				self.image = self.blood[i]
				game.clock.tick(8)
					
			text(screen, "YOU DIED", (0, 0, 0), (640 / 2), (180 / 2), 115)
			pygame.display.update()
			ugu.game_intro()	
			
				
        # hace que la camara siga al personaje o suba, dependiendo del tipo de nivel
		game.tilemap.set_focus(new.x, new.y)
		if game.mode:
			if game.map_counter%2==0:
				game.tilemap.set_focus(new.x, new.y)
			else:
				game.tilemap.set_focus(new.x, self.changeY)
				if self.rect.y > self.changeY + 300:
					self.lives = 0
        # verifica si el personaje toca al trigger de salida
		for cell in game.tilemap.layers["triggers"].collide(new, "exit"):
			self.finish = True
			
        # verifica si el personaje activa el trigger de muerte
		for cell in game.tilemap.layers["triggers"].collide(new, "death"):
			self.lives = 0
		if self.points < 0:
				self.points =0
#clase del jefe
class Boss(pygame.sprite.Sprite):
    def __init__(self, location,name, *groups):
		super(Boss, self).__init__(*groups)
        # carga las imagenes que corresponden al jefe
		
		
		self.boss_current = 0
		self.right_images=[]
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.000.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.001.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.002.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.003.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.004.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.005.png',True) )
		self.right_images.append(Util.imagen('sprites/'+name+'/'+name+'_right.006.png',True) )
		self.left_images = []
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.000.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.001.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.002.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.003.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.004.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.005.png',True) )
		self.left_images.append(Util.imagen('sprites/'+name+'/'+name+'_left.006.png',True) )
		self.image = self.right_images[self.boss_current]
		self.name=name
		self.rect = pygame.rect.Rect(location, self.image.get_size())
        # variable que sabe si el personaje esta tocando el suelo
		self.resting = False
        # contiene el delta y (la variente de y en el tiempo, para efectos del salto)
		self.dy = 0
		self.lives = 10
		self.direction = 1
		self.finish = False
		self.changeY = self.rect.y + 90
		self.walking = False
		self.walking_steps = 5
		self.estate = 0
		self.cooldown = 0
		self.proyectilDer = 'sprites/'+name+'ProDer.png'
		self.proyectilIzq = 'sprites/'+name+'ProIzq.png'
		self.healthbar = Healthbar(self.name,self.lives)
		
    def update(self, dt, game,screen):
		self.healthbar.update(self)
		last = self.rect.copy()
		if self.estate == 0:
			self.rect.x += self.direction * 100 * dt
			for cell in game.tilemap.layers["triggers"].collide(self.rect, "reverse"):
				if self.direction > 0:
					self.rect.right = cell.left
				else:
					self.rect.left = cell.right
				self.direction *= -1
				break
			if game.player.rect.y < self.rect.y+20:	
				if game.player.rect.x <self.rect.x and game.player.rect.x > self.rect.x-500:
					self.estate = 1
				if game.player.rect.x >self.rect.x and game.player.rect.x < self.rect.x+500:
					self.estate = 1
		if self.estate == 1:
			if game.player.rect.y < self.rect.y+20:
					
				if game.player.rect.x <self.rect.x and game.player.rect.x > self.rect.x-500:
					self.rect.x += -100 * dt
					if not self.cooldown:
						BulletBoss(self.rect.midleft, -1,self.proyectilIzq, game.sprites)
						self.cooldown = 3
					self.cooldown = max(0, self.cooldown - dt)
					self.walking=True
					self.direction = -1
				elif game.player.rect.x >self.rect.x and game.player.rect.x < self.rect.x+500:
					self.rect.x += 100 * dt 
					if not self.cooldown:
						BulletBoss(self.rect.midright, 1,self.proyectilDer, game.sprites)
						self.cooldown = 3
					self.cooldown = max(0, self.cooldown - dt)
					self.walking = True
					self.direction = 1
			if game.player.rect.y > self.rect.y+20:	
				self.estate =0
				
		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt
		new = self.rect
		self.resting = False
		
		if self.lives ==0:
			
			self.kill()
			game.player.finish = True
		
        # verifica si el personaje esta o no chocando con los objetos bloqueadores(suelo, parades, etc.)
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				new.right = cell.left
				self.resting = True
				self.direction *= -1
				
			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				new.left = cell.right
				self.resting = True
				self.direction *= -1
				
			if "t" in blockers and last.bottom <= cell.top and new.bottom > cell.top:
				self.resting = True
				new.bottom = cell.top
				self.dy = 0
			if "b" in blockers and last.top >= cell.bottom and new.top < cell.bottom:
				new.top = cell.bottom
				self.dy = 0
				
		if self.walking == True:
			if self.direction == 1:
		      
				
				if self.walking_steps > 0:
					
					self.boss_current = (self.boss_current + 1) % len(self.right_images)
					self.image = self.right_images[ self.boss_current ]
					self.walking_steps -= 1
				else:
					self.walking = False
					self.walking_steps=5		
						
			elif self.direction == -1:
				
				if self.walking_steps > 0:
					self.boss_current = (self.boss_current + 1) % len(self.left_images)
					self.image = self.left_images[ self.boss_current ]
					self.walking_steps -= 1
				else:
					self.walking = False	
					self.walking_steps=5
		if ugu.dificil ==2:			
			if self.rect.colliderect(game.player.rect):
				if game.player.direction == "right":
					game.player.rect.x-=800*dt
				elif game.player.direction == "left":
					game.player.rect.x+=800*dt	
					game.player.lives -= 1

					
class Bullet(pygame.sprite.Sprite):
  
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        
        self.image = pygame.image.load('sprites/pelota.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.lifespan = 1

    def update(self, dt, game,screen):
		last = self.rect.copy()
		self.lifespan -= dt
		if self.lifespan < 0:
			self.kill()
			return
		self.rect.x += self.direction * 400 * dt
			
		new = self.rect
		# verifica si el proyectil choca o no con alguna pared
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				self.kill()
			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				self.kill()
			
		if pygame.sprite.spritecollide(self, game.enemies, True):
			self.kill()
			game.player.points+=50
		if game.map_counter%2==0:
			if self.rect.colliderect(game.boss.rect):
				self.kill()
				game.boss.lives-=1	
				
class BulletBoss(pygame.sprite.Sprite):
  
    def __init__(self, location, direction,proyectil, *groups):
        super(BulletBoss, self).__init__(*groups)
        self.image = Util.imagen(proyectil,True)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = direction
        self.lifespan = 1

    def update(self, dt, game,screen):
		last = self.rect.copy()
		self.lifespan -= dt
		if self.lifespan < 0:
			self.kill()
			return
		self.rect.x += self.direction * 400 * dt
			
		new = self.rect
		# verifica si el proyectil choca o no con alguna pared
		for cell in game.tilemap.layers["triggers"].collide(new, "blockers"):
			blockers = cell["blockers"]
			if "l" in blockers and last.right <= cell.left and new.right > cell.left:
				self.kill()
			if "r" in blockers and last.left >= cell.right and new.left < cell.right:
				self.kill()
			
		if self.rect.colliderect(game.player.rect):
			self.kill()
			game.player.lives-=1

#if __name__ == '__main__':
def inicio():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Happy Tree Friends: Cuddles's Nightmares")
    Util.musica()
    Game().main(screen)
