
import configparser
import pygame, sys
from pygame.locals import *
from Mat import Mat
from Jewel import Jewel
from Stage import Stage

conf = configparser.ConfigParser()
conf.read('config.ini')

JEWELSIZE = conf.getint('sizes', 'jewel_size')

pygame.init()
fpsClock = pygame.time.Clock()

temp = [["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"],
		["O", "O", "O", "O", "O", "O"]]

colors = ["blue", "green", "orange", "purple", "red", "yellow"]

size = (len(temp[0])*JEWELSIZE+100, len(temp)*JEWELSIZE+100)
windowObj = pygame.display.set_mode(size)
pygame.display.set_caption("Joalheiro")

stg = Stage(temp, colors, windowObj, fpsClock)

font = pygame.font.SysFont(None, 48)

while True:
	windowObj.fill(pygame.Color(255, 255, 255))
	stg.draw(font)


	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			x, y = event.pos
			stg.click(x, y)

	pygame.display.update()
	fpsClock.tick(30)
