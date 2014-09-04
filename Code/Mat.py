import pygame
import configparser
import random
from Jewel import Jewel

class Mat:
	def __init__(self, template, jewelColors, wObj, clock):
		self.wObj = wObj
		self.template = template
		self.jColors = jewelColors
		self.clock = clock
		self.mat = self.generateMat()
		
	def generateMat(self):
		result = self.template
		for r in range(len(self.template)):
			for c in range(len(self.template[r])):
				if self.template[r][c] != "X":
					color = self.jColors[random.randrange(len(self.jColors)-1)]
					if ((c >= 2)and(r >= 2)):
						while (((color == result[r][c-1].color)and(color == result[r][c-2].color))or((color == result[r-1][c].color)and(color == result[r-2][c].color))):
							color = self.jColors[random.randrange(len(self.jColors)-1)]
						result[r][c] = Jewel(color)
					elif (c >= 2):
						while ((color == result[r][c-1].color)and(color == result[r][c-2].color)):
							color = self.jColors[random.randrange(len(self.jColors)-1)]
						result[r][c] = Jewel(color)
					elif (r >= 2):
						while ((color == result[r-1][c].color)and(color == result[r-2][c].color)):
							color = self.jColors[random.randrange(len(self.jColors)-1)]
						result[r][c] = Jewel(color)
					else:
						result[r][c] = Jewel(color)
		if not(self.validateMat(result)):
			result = self.generateMat()
		return result

	def validateMat(self, mat):
		for r in range(len(mat)):
			for c in range(len(mat[r])):
				if(((c+1) < len(mat[r]))and(self.validateMove(mat, (r, c), (r, c+1)) != None)):
					return True
				elif(((c-1) >= 0)and(self.validateMove(mat, (r, c), (r, c-1)) != None)):
					return True
				elif(((r-1) >= 0)and(self.validateMove(mat, (r, c), (r-1, c)) != None)):
					return True
				elif(((r+1) < len(mat))and(self.validateMove(mat, (r, c), (r+1, c)) != None)):
					return True
		return None

	def validateMove(self, mat, gemA, gemB):
		mat[gemA[0]][gemA[1]], mat[gemB[0]][gemB[1]] = mat[gemB[0]][gemB[1]], mat[gemA[0]][gemA[1]]
		result, pRight, pLeft, pUp, pDown = self.verifyJewel(mat, gemA)
		if not result:
			result, pRight, pLeft, pUp, pDown = self.verifyJewel(mat, gemB)
			if result:
				mat[gemA[0]][gemA[1]], mat[gemB[0]][gemB[1]] = mat[gemB[0]][gemB[1]], mat[gemA[0]][gemA[1]]
				return gemB, pRight, pLeft, pUp, pDown
			else:
				mat[gemA[0]][gemA[1]], mat[gemB[0]][gemB[1]] = mat[gemB[0]][gemB[1]], mat[gemA[0]][gemA[1]]
		else:
			mat[gemA[0]][gemA[1]], mat[gemB[0]][gemB[1]] = mat[gemB[0]][gemB[1]], mat[gemA[0]][gemA[1]]
			return gemA, pRight, pLeft, pUp, pDown

		return None

	def swap(self, gemA, gemB):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		step = conf.getint('sizes', 'animation_step')
		rAuxA, cAuxA = gemA[0]*jSize, gemA[1]*jSize
		rAuxB, cAuxB = gemB[0]*jSize, gemB[1]*jSize
		rStep, cStep = (gemA[0] - gemB[0])*step, (gemA[1] - gemB[1])*step
		while ((rAuxA != gemB[0]*jSize)or(cAuxA != gemB[1]*jSize)):
			self.wObj.fill(pygame.Color(255, 255, 255))
			for r in range(len(self.mat)):
				for c in range(len(self.mat[r])):
					if ((r == gemA[0])and(c == gemA[1])):
						self.mat[r][c].draw(((cAuxA), (rAuxA)), self.wObj)
						rAuxA -= rStep
						cAuxA -= cStep
					elif ((r == gemB[0])and(c == gemB[1])):
						self.mat[r][c].draw(((cAuxB), (rAuxB)), self.wObj)
						rAuxB += rStep
						cAuxB += cStep
					else:
						self.mat[r][c].draw(((jSize*c), (jSize*r)), self.wObj)
			pygame.display.update()
			self.clock.tick(60)
		self.mat[gemA[0]][gemA[1]], self.mat[gemB[0]][gemB[1]] = self.mat[gemB[0]][gemB[1]], self.mat[gemA[0]][gemA[1]]

	def verifyJewel(self, mat, gem):
		pRight = 0
		pLeft = 0
		pUp = 0
		pDown = 0
		makePoint = False
		#--------------------Horizontal----------
		#----------Right---------------
		c = gem[1] + 1
		while ((c < len(mat[gem[0]]))and(mat[gem[0]][c].color == mat[gem[0]][gem[1]].color)):
			pRight += 1
			c += 1
		#----------Left----------------
		c = gem[1] - 1
		while ((c >= 0)and(mat[gem[0]][c].color == mat[gem[0]][gem[1]].color)):
			pLeft += 1
			c -= 1
		#------------------------------
		if (pRight + pLeft >= 2):
			makePoint = True
		else:
			pRight = 0
			pLeft = 0
		#--------------------Vertical---------------------
		#----------Up----------------
		r = gem[0] - 1
		while ((r >= 0)and(mat[r][gem[1]].color == mat[gem[0]][gem[1]].color)):
			pUp += 1
			r -= 1
		#----------Down--------------
		r = gem[0] + 1
		while ((r < len(mat))and(mat[r][gem[1]].color == mat[gem[0]][gem[1]].color)):
			pDown += 1
			r += 1
		#----------------------------
		if (pUp + pDown >= 2):
			makePoint = True
		else:
			pUp = 0
			pDown = 0
		return makePoint, pRight, pLeft, pUp, pDown


	def move(self, gemA, gemB):
		val = self.validateMove(self.mat, gemA, gemB)
		if val != None:
			self.swap(gemA, gemB)
			return self.getPoints(val[0], val[1], val[2], val[3], val[4])
		else:
			return 0


	def getPoints(self, gem, pRight, pLeft, pUp, pDown):
		self.destroy(gem, pRight, pLeft, pUp, pDown)
		#--------------------Vertical----------------------
		rAux = gem[0]+pDown
		jump = pDown+pUp+1
		self.remap(rAux, gem[1], jump)
		#--------------------Horizontal--------------------
		#--------------------Right-------------------------
		cAux = gem[1]
		while (cAux <= (gem[1] + pRight)):
			rAux = gem[0]
			jump = 1
			self.remap(rAux, cAux, jump)
			cAux += 1
		#--------------------Left--------------------------
		cAux = gem[1]
		while (cAux >= (gem[1] - pLeft)):
			rAux = gem[0]
			jump = 1
			self.remap(rAux, cAux, jump)
			cAux -= 1

		points = (pRight + pLeft + pUp + pDown + 1)*50
		ver = self.verifyMat()
		if ver != None:
			points += self.getPoints((ver[0], ver[1]), ver[2], ver[3], ver[4], ver[5])

		if not self.validateMat(self.mat):
			self.generateMat()
		return points

	def destroy(self, gem, pRight, pLeft, pUp, pDown):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		step = conf.getint('sizes', 'animation_step')
		reduction = 0
		while (reduction < jSize):
			blank = reduction/2
			self.wObj.fill(pygame.Color(255, 255, 255))
			for r in range(len(self.mat)):
				for c in range(len(self.mat[r])):
					if ((r >= (gem[0]-pUp))and(r <= (gem[0]+pDown))and(c == gem[1])):
						self.mat[r][c].drawScaled(((jSize*c + blank), (jSize*r + blank)), reduction, self.wObj)
					elif ((r == gem[0])and(c >= (gem[1]-pLeft))and(c <= (gem[1]+pRight))):
						self.mat[r][c].drawScaled(((jSize*c + blank), (jSize*r + blank)), reduction, self.wObj)
					else:
						self.mat[r][c].draw((jSize*c, jSize*r), self.wObj)
			reduction += step
			pygame.display.update()
			self.clock.tick(30)

	def remap(self, row, col, jump):
		while ((row - jump) >= 0):
			if self.mat[row-jump][col].color != "X":
				if self.mat[row][col] != "X":
					self.mat [row][col] = self.mat[row-jump][col]
					row -= 1
				else:
					row -= 1
					jump -= 1
			else:
				jump += 1
		while (row >= 0):
			if self.mat[row][col].color != "X":
				self.mat[row][col] = Jewel(self.jColors[random.randrange(len(self.jColors)-1)])
			row -= 1

	def verifyMat(self):
		for r in range(len(self.mat)):
			for c in range(len(self.mat[r])):
				result = False
				pRight = 0
				pLeft = 0
				pUp = 0
				pDown = 0
				#--------------------Horizontal----------
				#----------Right---------------
				cAux = c + 1
				while ((cAux < len(self.mat[r]))and(self.mat[r][cAux].color == self.mat[r][c].color)):
					pRight += 1
					cAux += 1
				#----------Left----------------
				cAux = c - 1
				while ((cAux >= 0)and(self.mat[r][cAux].color == self.mat[r][c].color)):
					pLeft += 1
					cAux -= 1
				#------------------------------
				if (pRight + pLeft >= 2):
					result = True
				else:
					pRight = 0
					pLeft = 0
				#--------------------Vertical---------------------
				#----------Up----------------
				rAux = r - 1
				while ((rAux >= 0)and(self.mat[rAux][c].color == self.mat[r][c].color)):
					pUp += 1
					rAux -= 1
				#----------Down--------------
				rAux = r + 1
				while ((rAux < len(self.mat))and(self.mat[rAux][c].color == self.mat[r][c].color)):
					pDown += 1
					rAux += 1
				#----------------------------
				if (pUp + pDown >= 2):
					result = True
				else:
					pUp = 0
					pDown = 0
				
				if result:
					return r, c, pRight, pLeft, pUp, pDown

		return None

	def draw(self):
		conf = configparser.ConfigParser()
		conf.read('config.ini')
		jSize = conf.getint('sizes', 'jewel_size')
		for r in range(len(self.mat)):
			for c in range(len(self.mat[r])):
				self.mat[r][c].draw(((jSize*c), (jSize*r)), self.wObj)