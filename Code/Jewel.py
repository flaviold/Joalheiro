import configparser
import pygame

class Jewel:
	def __init__(self, color):
		self.color = color
		self.sprite, self.selSprite = self.getSprite(color)
		self.selected = False

	def getSprite(self, color):
		if color != "X":
			conf = configparser.ConfigParser()
			conf.read('config.ini')
			path = conf.get('paths', 'sprites')
			return pygame.image.load(path+"gem_"+color+".png"), pygame.image.load(path+"gem_"+color+"_selected.png")
		else:
			return None, None

	def drawScaled(self, position, reduct, wObj):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		scaledSprite = pygame.transform.scale(self.sprite, (jSize-reduct, jSize-reduct))
		wObj.blit(scaledSprite, position)


	def draw(self, position, wObj):
		if self.color != "X":
			if self.selected:
				wObj.blit(self.selSprite, position)
			else:
				wObj.blit(self.sprite, position)