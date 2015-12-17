"""
Tim Hartmann 
October 2015

3x71nc7.itch.io 
www.youtube.com/tim110899

A very simple shoot'em up game made in python3 with pygame


Types:
	Projectiles:
		Projectile = 0
		Bomb = 1
	Items:
		Medikit = 0


"""
import pygame
import random
import math
import sys
import webbrowser

##COLORS
white =  (255,255,255)
black =  (0,0,0)
red =    (255,0,0)
green =  (0,255,0)
blue =   (0,0,255)
orange = (255,140,0)
lime =   (173,255,47)
cyan =   (0,255,255)
brown =  (84,66,62)
alpha =  (255,0,255)
gray =	 (100,100,100)

pygame.init()
clock = pygame.time.Clock()

scr_size = width,height = 508,700
pygame.display.set_caption("Shoot'em up!")
screen = pygame.display.set_mode(scr_size)
font = pygame.font.Font(None , 30)
font2 = pygame.font.Font(None , 60)
font3 = pygame.font.Font(None,40)
screen.set_colorkey((255,0,255))

##Game Varibales
count  = 0
playing = 0



#loading images
medikitIMG = pygame.image.load("data/health.png")
medikitIMG = pygame.transform.scale(medikitIMG,(32,32))
medikitIMG.set_colorkey(alpha)
medikitIMG = medikitIMG.convert()

raiderIMG = pygame.image.load("data/Raider.png")
raiderIMG = pygame.transform.scale(raiderIMG,(128,32))
raiderIMG.set_colorkey(alpha)
raiderIMG = raiderIMG.convert()

battleshipIMG = pygame.image.load("data/Battleship.png")
battleshipIMG = pygame.transform.scale(battleshipIMG,(320,64))
battleshipIMG.set_colorkey(alpha)
battleshipIMG = battleshipIMG.convert()

bomberIMG = pygame.image.load("data/Bomber.png")
bomberIMG = pygame.transform.scale(bomberIMG,(128,32))
bomberIMG.set_colorkey(alpha)
bomberIMG = bomberIMG.convert()

playerIMG = pygame.image.load("data/Player.png")
playerIMG = pygame.transform.scale(playerIMG,(192,64))
playerIMG.set_colorkey(alpha)
playerIMG = playerIMG.convert()

bulletIMG = pygame.image.load("data/Projectile.png")
bulletIMG = pygame.transform.scale(bulletIMG,(8,16))
bulletIMG.set_colorkey(alpha)
bulletIMG = bulletIMG.convert()

bulletPlayerIMG = pygame.image.load("data/ProjectilePlayer.png")
bulletPlayerIMG = pygame.transform.scale(bulletPlayerIMG,(8,16))
bulletPlayerIMG.set_colorkey(alpha)
bulletPlayerIMG = bulletPlayerIMG.convert()

bombIMG = pygame.image.load("data/Bomb.png")
bombIMG = pygame.transform.scale(bombIMG,(16,16))
bombIMG.set_colorkey(alpha)
bombIMG = bombIMG.convert()

class Medikit:
	def __init__(self,x):
		self.x = x
		self.y = -16
		self.health = 25
		self.vy = -3
		self.image = medikitIMG
		self.width = 32
		self.height = 32
		self.type = 0
		self.collided = False
	def update(self):
		self.y -= self.vy

class Projectile:
	def __init__(self,x,y,dmg,player):
		self.x = x
		self.y = y
		self.type = 0
		if player:
			self.vy = 6
			self.image = bulletPlayerIMG
		else:
			self.vy = -6
			self.image = bulletIMG
		self.player = player
		self.dmg = dmg
		self.collided = False
	def update(self):
		self.y -= self.vy

class Bomb:
	def __init__(self,x,y,dmg,player):
		self.x = x
		self.y = y
		self.vy = -4
		self.type = 1
		self.image = bombIMG
		self.dmg = dmg
		self.collided = False
	def update(self):
		self.y -= self.vy
		

class Player:
	def __init__(self):
		self.health = 100
		self.dmg = 10
		self.rot = 5#amount of frames waiting before next shot
		self.image = playerIMG
		self.spriteSurface = pygame.Surface((64,64))
		self.frames = 3
		self.speed = 4
		self.regen = 1
		self.count = 0
		self.score = 0
		self.x = 242
		self.y = 600
		self.width = 64
		self.height = 64
	def update(self):
		self.count+= 1
	def shoot(self):
		if self.count % self.rot == 0:
			projectiles.append(Projectile(self.x+28,self.y,self.dmg,True))
	def render(self):
		self.spriteSurface.fill(alpha)
		offset = int(self.count/3) % (self.frames)
		self.spriteSurface.blit(self.image,(-64*offset,0))
		self.spriteSurface.set_colorkey(alpha)

class Raider:#light, fast enemy
	def __init__(self,x,direction):
		self.health = 10
		self.rot = 10
		self.dmg = 0.75
		self.image = raiderIMG
		self.spriteSurface = pygame.Surface((32,32))
		self.speed = 5
		self.count = 0
		self.frames = 4
		self.width = 32
		self.height = 32
		self.x = x
		self.y = -16
		self.direction = direction#'left' or 'right' 

	def update(self):
		self.count += 1
		if self.count % self.rot == 0:
			projectiles.append(Projectile(self.x+8,self.y+16,self.dmg,False))
		if self.direction == 'left':
			self.x -= self.speed/2
		else:
			self.x += self.speed/2
		self.y += self.speed/3
		if self.x <= 0:
			self.direction = 'right'
		elif self.x >= width-32:
			self.direction = 'left'
	def render(self):
		self.spriteSurface.fill(alpha)
		offset = self.count % (self.frames-1)
		self.spriteSurface.blit(self.image,(-32*offset,0))
		self.spriteSurface.set_colorkey(alpha)

class Bomber:#medium enemy
	def __init__(self,x,direction):
		self.health = 25
		self.rot = 40
		self.dmg = 10
		self.image = bomberIMG
		self.spriteSurface = pygame.Surface((32,32))
		self.speed = 2
		self.count = 0
		self.frames = 4
		self.width = 32
		self.height = 32
		self.x = x
		self.y = -16
		self.direction = direction#'left' or 'right'
	def update(self):
		self.count += 1
		if self.count % self.rot == 0:
			projectiles.append(Bomb(self.x+8,self.y+16,self.dmg,False))
		if self.direction == 'left':
			self.x -= self.speed/2
		else:
			self.x += self.speed/2
		self.y += self.speed/3
		if self.x <= 0:
			self.direction = 'right'
		elif self.x >= width-32:
			self.direction = 'left'
	def render(self):
		self.spriteSurface.fill(alpha)
		offset = self.count % (self.frames-1)
		self.spriteSurface.blit(self.image,(-32*offset,0))
		self.spriteSurface.set_colorkey(alpha)

class Battleship:#heavy, slow enemy
	def __init__(self,x,direction):
		self.health = 50
		self.rotProj = 10
		self.rotBmb = 40
		self.dmgProj = 2
		self.dmgBmb = 15
		self.image = battleshipIMG
		self.spriteSurface = pygame.Surface((64,64))
		self.speed = 1
		self.count = 0
		self.frames = 4
		self.width = 64
		self.height = 64
		self.x = x
		self.y = -32
		self.direction = direction#'left' or 'right'
	def update(self):
		self.count += 1
		if self.count % self.rotProj == 0:
			projectiles.append(Projectile(self.x+16,self.y+32,self.dmgProj,False))
		if self.count % self.rotBmb == 0:
			projectiles.append(Bomb(self.x+16,self.y+32,self.dmgBmb,False))
		if self.direction == 'left':
			self.x -= self.speed
		else:
			self.x += self.speed
		self.y += self.speed/3
		if self.x <= 0:
			self.direction = 'right'
		elif self.x >= width-64:
			self.direction = 'left'
	def render(self):
		self.spriteSurface.fill(alpha)
		offset = self.count % (self.frames-1)
		self.spriteSurface.blit(self.image,(-64*offset,0))
		self.spriteSurface.set_colorkey(alpha)

game = 1
enemies = []
projectiles = []
items = []
def play():

	Spieler = Player()
	s = open("savefile.data","rt")
	hs = s.readlines()
	hs = int(hs[1])
	while True:

		screen.fill(brown)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return 0
		##User Input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			Spieler.x += Spieler.speed
		if keys[pygame.K_LEFT]:
			Spieler.x -= Spieler.speed
		if keys[pygame.K_UP]:
			Spieler.y -= Spieler.speed
		if keys[pygame.K_DOWN]:
			Spieler.y += Spieler.speed
		if keys[pygame.K_SPACE]:
			Spieler.shoot()

		##Spawning
		if 2 == random.randint(1,30*int(1+(Spieler.count/300))):
			items.append(Medikit(random.randint(0,width-32)))
		if 2 == random.randint(1,120):
			enemies.append(Raider(random.randint(0,width-32),'left'))
		if 2 == random.randint(1,240):
			enemies.append(Bomber(random.randint(0,width-32),'right'))
		if 2 == random.randint(1,560):
			enemies.append(Battleship(random.randint(0,width-32),'left'))

		if 2 == random.randint(1,120):
			enemies.append(Raider(random.randint(0,width-32),'right'))
		if 2 == random.randint(1,240):
			enemies.append(Bomber(random.randint(0,width-32),'left'))
		if 2 == random.randint(1,560):
			enemies.append(Battleship(random.randint(0,width-32),'right'))

		##Move Everything and shoot and stuff
		for i in items:
			i.update()
		for e in enemies:
			e.update()
		Spieler.update()

		##Check for Collision and remove props
		#->Projectile Collisions
		for p in projectiles:
			if p.type == 0:
				if p.player:
					for e in enemies:
						if p.x+8 > e.x and p.x < e.x+e.width and p.y+16 > e.y and p.y < e.y+e.height:
							p.collided = True
							e.health -= p.dmg
				else:#check fuer spieler
					if p.x+8 > Spieler.x and p.x < Spieler.x+Spieler.width and p.y+16 > Spieler.y and p.y < Spieler.y+Spieler.height:
						p.collided = True
						Spieler.health -= p.dmg
			if p.type == 1:#kann nur den Spieler treffen
				if p.x+16 > Spieler.x+12 and p.x < Spieler.x+Spieler.width-12 and p.y+16 > Spieler.y and p.y < Spieler.y+Spieler.height:
					p.collided = True
					Spieler.health -= p.dmg

		for i in items:#item collision
			if i.type == 0:
				if i.x+i.width > Spieler.x and i.x < Spieler.x+Spieler.width and i.y+i.height > Spieler.y and i.y < Spieler.y+Spieler.height:
					i.collided = True
					Spieler.health += i.health



		for i in reversed(range(len(items))):
			if items[i].y > height+32:
				del items[i]
			elif items[i].collided:
				del items[i]
		for e in reversed(range(len(enemies))):
			if enemies[e].y > height+32:
				del enemies[e]
			elif enemies[e].health <= 0:
				del enemies[e]
				Spieler.score += 1

		for p in reversed(range(len(projectiles))):
			if projectiles[p].y > height+16:
				del projectiles[p]
			elif projectiles[p].y < -16:
				del projectiles[p]
			elif projectiles[p].collided:
				del projectiles[p]

		##Check Player health
		if Spieler.health <= 0:
			s = open("savefile.data","wt")

			if Spieler.score > hs:
				s.write(str(Spieler.score)+"\n")
				s.write(str(Spieler.score))	
			else:
				s.write(str(Spieler.score)+"\n")
				s.write(str(hs))
			s.close()	
			return 0

		##Rendering
		#->Background Clouds

		#->Items
		for i in items:	
			screen.blit(i.image,(i.x,i.y))

		#->Projectiles
		for p in projectiles:
			p.update()
			screen.blit(p.image,(p.x,p.y))

		#->Player and enemies
		for e in enemies:
			e.render()
			screen.blit(e.spriteSurface,(e.x,e.y))
		Spieler.render()
		screen.blit(Spieler.spriteSurface,(Spieler.x,Spieler.y))

		#->UI
		pygame.draw.rect(screen, gray , (0,0,110,20),0)
		pygame.draw.rect(screen, gray , (388,0,120,20),0)
		scoreText = font.render("Score:"+str(Spieler.score),True,white)
		healthText = font.render("Health:"+str(int(Spieler.health)),True,red)
		screen.blit(healthText,(0,0))
		screen.blit(scoreText,(388,0))
		clock.tick(60)
		pygame.display.flip()


def homescreen():
	select = 0
	s = open("savefile.data","rt")
	scores = s.readlines()
	sc = int(scores[0])
	hs = int(scores[1])
	while True:
		screen.fill((114,106,91))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					select += 1
				elif event.key == pygame.K_UP:
					select -= 1
				elif event.key == pygame.K_RETURN:
					#select 0 = play
					#select 1 = website
					#select 2 = exit
					if select % 3 == 0:
						enemies = []
						projectiles = []
						items = []

						return 0
						

					elif select % 3 == 1:
						webbrowser.open_new("http://3x71nc7.itch.io")
					elif select % 3 == 2:
						exit()

		h1 = font2.render("Shoot'em up!",True,(181,179,139))
		h2 = font3.render("by Tim Hartmann",True,(127,126,99))
		if select % 3 == 0:
			t1 = font.render("play",True,(17,38,33))
			t2 = font.render("website",True,(82,22,25))
			t3 = font.render("exit",True,(82,22,25))			
		elif select % 3 == 1:
			t1 = font.render("play",True,(82,22,25))
			t2 = font.render("website",True,(17,38,33))
			t3 = font.render("exit",True,(82,22,25))
		else:
			t1 = font.render("play",True,(82,22,25))
			t2 = font.render("website",True,(82,22,25))
			t3 = font.render("exit",True,(17,38,33))

		t4 = font.render("Last Score:"+str(sc),True,(33,38,61))
		t5 = font.render("High Score:"+str(hs),True,(33,38,61))
		screen.blit(h1,(150,100))
		screen.blit(h2,(150,150))

		screen.blit(t1,(100,300))
		screen.blit(t2,(100,350))
		screen.blit(t3,(100,400))
		screen.blit(t4,(100,250))
		screen.blit(t5,(100,225))

		pygame.display.flip()
while True:
	homescreen()
	play()