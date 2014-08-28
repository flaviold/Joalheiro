import pygame, sys
from pygame.locals import *
from Mat import Mat
from Jewel import Jewel
from Stage import Stage

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

stg = Stage(temp, colors)

size = (len(temp[0])*32+100, len(temp)*32+100)
windowObj = pygame.display.set_mode(size)
pygame.display.set_caption("Joalheiro")

font = pygame.font.SysFont(None, 48)

while True:
	windowObj.fill(pygame.Color(255, 255, 255))
	stg.draw(windowObj, font)


	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			x, y = event.pos
			stg.click(x, y)

	pygame.display.update()