import pygame

class Jewel:
	def __init__(self, color):
		self.color = color
		self.sprite, self.selSprite = self.getSprite(color)
		self.selected = False

	def getSprite(self, color):
		if color != "X":
			return pygame.image.load("sprites/gem_"+color+".png"), pygame.image.load("sprites/gem_"+color+"_selected.png")
		else:
			return None, None

	def draw(self, position, wObj):
		if self.color != "X":
			if self.selected:
				wObj.blit(self.selSprite, position)
			else:
				wObj.blit(self.sprite, position)