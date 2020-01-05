import pygame
import sys
import re

file = open("./RPGtest.txt")
text = ""
count_line = 0
for line in file.readlines():
	text += line
	count_line += 1
print(text)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

pygame.init()

FPS = 1
size = (width,height) = (800,600)
back_color = WHITE
tile_size = 64

def QUIT():
	pygame.quit()
	sys.exit()
class Tile:
	def __init__(self,image):
		self.Sur = pygame.image.load(image)
		self.rect = self.Sur.get_rect()
class Monster:
	def __init__(self,image,attack,defence,hp):
		self.image = pygame.image.load(image)
		self.atk = attack
		self.defen = defence
		self.hp = hp
		self.fullhp = hp
	def create(self):
		hps_x = tile_size*7/8
		hps_y = tile_size/8
		hps_fr = 2
		gap = 3
		self.hpSur = pygame.Surface((hps_x,hps_y),pygame.SRCALPHA)
		pygame.draw.rect(self.hpSur,RED,[0,0,hps_x*(self.hp/self.fullhp),hps_y],0)
		pygame.draw.rect(self.hpSur,BLACK,[0,0,hps_x,hps_y],hps_fr)
		self.Sur = pygame.Surface((tile_size,tile_size+gap+hps_y),pygame.SRCALPHA)
		self.Sur.blit(self.hpSur,((tile_size-hps_x)/2,0))
		self.Sur.blit(self.image,(0,hps_y+gap))
		self.rect = self.Sur.get_rect()
def arrange(a):
	list1 = re.split(r"\n",a)
	list2 = []
	for string in list1:
		list2.append(re.split(r"\s+",string))
	return list2

rabbit = Monster("./monster.gif",3,3,10)
#rabbit.Sur.convert()
bl = pygame.image.load("./image.gif")
#bl.Sur.convert()

blitlist = arrange(text)
print(blitlist)

windows = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			QUIT()
	rabbit.create()
	windows.fill(back_color)
	for row in range(count_line):
		x = 0
		for obj in blitlist[row]:
			windows.blit(eval(obj),(x,row*tile_size))
			x += tile_size
	pygame.display.flip()
	clock.tick(FPS)
