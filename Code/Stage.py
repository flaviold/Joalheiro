import configparser
from Mat import Mat
from Jewel import Jewel

class Stage:
	def __init__(self, template, jColors, wObj, clock):
		self.wObj = wObj
		self.score = 0
		self.mat = Mat(template, jColors, wObj, clock)
		self.selectedGem = None

	def click(self, x, y):
		self.selectJewel(x, y)

	def selectJewel(self, x, y):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		if((x<len(self.mat.mat[0]*jSize))and(y<len(self.mat.mat)*jSize)):
			r = 0
			c = 0
			while(r*jSize < y):
				r += 1
			while(c*jSize < x):
				c += 1
			r -= 1
			c -= 1
			if self.mat.mat[r][c].color != "X":
				if (self.selectedGem != None):
					points = 0
					if ((self.selectedGem[0] == r)and(self.selectedGem[1]) == c+1):
						points += self.mat.move((self.selectedGem[0], self.selectedGem[1]), (r, c))
					elif ((self.selectedGem[0] == r)and(self.selectedGem[1]) == c-1):
						points += self.mat.move((self.selectedGem[0], self.selectedGem[1]), (r, c))
					elif ((self.selectedGem[0] == r-1)and(self.selectedGem[1]) == c):
						points += self.mat.move((self.selectedGem[0], self.selectedGem[1]), (r, c))
					elif ((self.selectedGem[0] == r+1)and(self.selectedGem[1]) == c):
						points += self.mat.move((self.selectedGem[0], self.selectedGem[1]), (r, c))
					self.unselectJewels()
					self.selectedGem = None
					self.score += points
				else:
					self.mat.mat[r][c].selected = True
					self.selectedGem = (r, c)
			else:
				if (self.selectedGem != None):
					self.unselectJewels()
					self.selectedGem = None
		else:
			self.unselectJewels()
			self.selectedGem = None

	def unselectJewels(self):
		for r in self.mat.mat:
			for i in r:
				i.selected = False

	def draw(self, font):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		self.mat.draw()
		tObj = font.render(str(self.score), 1, (0, 0, 0))
		position = (10, len(self.mat.mat)*jSize+50)
		self.wObj.blit(tObj, position)
