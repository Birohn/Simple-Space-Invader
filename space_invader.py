import os, sys, pygame
from pygame.locals import *
import directory

if not pygame.font:  print('Warning, fonts disabled')
if not pygame.mixer: print('Warning , sound disabled')


main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(name, colorkey=None):
	path= os.path.join(main_dir,'images',name)
	try:
		image = pygame.image.load(path).convert()
	except pygame.error:
		print('Cannot load {0} image'.format(name), )
		raise SystemExit()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()
	
def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	fullname = os.path.join(main_dir,'sounds',name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error:
		print('Cannot load sound: ', name)
		raise SystemExit()
	return sound
	
class Enemy(pygame.sprite.Sprite):
	
	def __init__(self,x_pos,y_pos):
		screen = pygame.display.get_surface()
		pygame.sprite.Sprite.__init__(self)
		self.x_pos = x_pos
		self.image = pygame.transform.scale(load_image('SpaceInvader.jpg',-1)[0],(40,36))
		self.rect= self.image.get_rect().move(self.x_pos,y_pos)
		self.move = 3
	def update(self):
		self._move()
		
	def _move(self):
		newpos = self.rect.move((self.move, 0))
		if self.rect.left < self.x_pos - 200 or \
			self.rect.right > self.x_pos + 200:
			self.move = -self.move
			newpos = self.rect.move((self.move, 10))
		self.rect = newpos
class Player(pygame.sprite.Sprite):
	def __init__(self):
		screen = pygame.display.get_surface()
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(load_image('player.jpg',-1)[0],(95,90))
		self.rect= self.image.get_rect(center=(screen.get_width()/2,screen.get_height()-95))
		self.move = 8
		self.has_shot = False
	def move_left(self):
		new_pos= self.rect.move(-self.move, 0)
		if new_pos.left > 0:
			self.rect = new_pos
	def move_right(self):
		new_pos= self.rect.move(self.move, 0)
		if new_pos.right < 1000:
			self.rect= new_pos
class Bullet(pygame.sprite.Sprite):
	def __init__(self,coord):
		screen = pygame.display.get_surface()
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(load_image('laser.png',-1)[0],(15,20))
		self.coord = coord
		self.rect = self.image.get_rect(center=(coord[0],coord[1]))
		self.speed = 12
		self.has_shot = False
	def update(self):
		self._move()
		
	def _move(self):
		new_pos = self.rect.move(0,-self.speed)
		if new_pos.top < 0:
			self.kill()
			self.has_shot = False
		else:
			self.rect = new_pos
			
			

def main():
	print("Game Executed")
	#Initialize Everything
	pygame.mixer.pre_init(44100, -16,2,2048)
	pygame.mixer.init()
	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	background = load_image("space.png",None)[0]
	pygame.mouse.set_visible(0)
	#Display The Background
	screen.blit(background, (0, 0))
	#Prepare Game Objects
	laser=load_sound("laser.wav")
	clock = pygame.time.Clock()
	player = Player()
	bullet = Bullet(player.rect.midtop)
	bulletsprite = pygame.sprite.RenderPlain()
	allsprites = pygame.sprite.RenderPlain((player))
	for x in range(4):
		for y in range(8):
			o = Enemy(y * 65 + 300,x*40 + 100)
			allsprites.add(o)
	
	pressed_left=pressed_right = None
	#Main Loop
	going = True
	while going:
		clock.tick(60)
			#Handle Input Events
		for event in pygame.event.get():
			if event.type == QUIT:
				going = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
			elif event.type == KEYDOWN and event.key == K_w and (bullet.has_shot == False or bullet.alive() == False):
				bullet.has_shot = True
				laser.play()
				bullet.rect =bullet.image.get_rect(center=(player.rect.midtop[0],player.rect.midtop[1]-20))
				bulletsprite.add(bullet)
				
				
			elif event.type == KEYDOWN:
				if event.key == K_a:
					pressed_left = True
				elif event.key == K_d:
					pressed_right= True
			elif event.type == KEYUP:
				if event.key == K_a:
					pressed_left = False
				elif event.key == K_d:
					pressed_right = False
			
				
		#Handle Player Sprite Movement
		if pressed_left == True:
			player.move_left()
			
		if pressed_right == True:
			player.move_right()
			
		#Handle Collision
		pygame.sprite.groupcollide(bulletsprite,allsprites,True,True)	
		allsprites.update()	
		bulletsprite.update()
		
		#Draw Everything
		
		screen.blit(background, (0, 0))
		allsprites.draw(screen)
		bulletsprite.draw(screen)
		pygame.display.flip()
		

	pygame.quit()
	
	
#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
	main()