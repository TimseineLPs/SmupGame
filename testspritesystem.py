import pygame

screen = pygame.display.set_mode((100,400))
clock = pygame.time.Clock()

raider = pygame.image.load("data/Raider.png")
raider.set_colorkey((255,0,255))
raider = pygame.transform.scale(raider,(256,64))
raider = raider.convert()

battleship = pygame.image.load("data/Battleship.png")
battleship.set_colorkey((255,0,255))
battleship = pygame.transform.scale(battleship,(320,64))
battleship = battleship.convert()

bomber = pygame.image.load("data/Bomber.png")
bomber.set_colorkey((255,0,255))
bomber = pygame.transform.scale(bomber,(256,64))
bomber = bomber.convert()

player = pygame.image.load("data/Player.png")
player.set_colorkey((255,0,255))
player = pygame.transform.scale(player,(192,64))
player = player.convert()

spriteSurface = pygame.Surface((64,64))
spriteSurface2 = pygame.Surface((64,64))
spriteSurface3 = pygame.Surface((64,64))
spriteSurface4 = pygame.Surface((64,64))

framecount = 0
while True:
	if framecount == 3:
		framecount = 0
	
	spriteSurface.fill((255,0,255))
	spriteSurface.blit(raider,(-64*framecount,0))
	spriteSurface.set_colorkey((255,0,255))

	spriteSurface2.fill((255,0,255))
	spriteSurface2.blit(battleship,(-64*framecount,0))
	spriteSurface2.set_colorkey((255,0,255))

	spriteSurface3.fill((255,0,255))
	spriteSurface3.blit(bomber,(-64*framecount,0))
	spriteSurface3.set_colorkey((255,0,255))

	spriteSurface4.fill((255,0,255))
	spriteSurface4.blit(player,(-64*framecount,0))
	spriteSurface4.set_colorkey((255,0,255))

	screen.fill((255,255,255))
	screen.blit(spriteSurface,(0,0))
	screen.blit(spriteSurface2,(0,64))
	screen.blit(spriteSurface3,(0,128))
	screen.blit(spriteSurface4,(0,192))

	framecount += 1
	pygame.display.flip()
	clock.tick(60)