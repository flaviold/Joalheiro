import random
from Jewel import Jewel

class Mat:
	def __init__(self, template, jewelColors):
		self.template = template
		self.jColors = jewelColors
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
					aux = mat[r][c]
					mat[r][c] = mat[r][c+1]
					mat[r][c+1] = aux
					return True
				elif(((c-1) >= 0)and(self.validateMove(mat, (r, c), (r, c-1)) != None)):
					aux = mat[r][c]
					mat[r][c] = mat[r][c-1]
					mat[r][c-1] = aux
					return True
				elif(((r-1) >= 0)and(self.validateMove(mat, (r, c), (r-1, c)) != None)):
					aux = mat[r][c]
					mat[r][c] = mat[r-1][c]
					mat[r-1][c] = aux
					return True
				elif(((r+1) < len(mat))and(self.validateMove(mat, (r, c), (r+1, c)) != None)):
					aux = mat[r][c]
					mat[r][c] = mat[r+1][c]
					mat[r+1][c] = aux
					return True
		return None

	def validateMove(self, mat, gemA, gemB):
		result = False
		pRight = 0
		pLeft = 0
		pUp = 0
		pDown = 0
		aux = mat[gemA[0]][gemA[1]]
		mat[gemA[0]][gemA[1]] = mat[gemB[0]][gemB[1]]
		mat[gemB[0]][gemB[1]] = aux
		#----------------------------------------GemA---------------
		#--------------------Horizontal----------
		#----------Right---------------
		cAux = gemA[1] + 1
		while ((cAux < len(mat[gemA[0]]))and(mat[gemA[0]][cAux].color == mat[gemA[0]][gemA[1]].color)):
			pRight += 1
			cAux += 1
		#----------Left----------------
		cAux = gemA[1] - 1
		while ((cAux >= 0)and(mat[gemA[0]][cAux].color == mat[gemA[0]][gemA[1]].color)):
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
		rAux = gemA[0] - 1
		while ((rAux >= 0)and(mat[rAux][gemA[1]].color == mat[gemA[0]][gemA[1]].color)):
			pUp += 1
			rAux -= 1
		#----------Down--------------
		rAux = gemA[0] + 1
		while ((rAux < len(mat))and(mat[rAux][gemA[1]].color == mat[gemA[0]][gemA[1]].color)):
			pDown += 1
			rAux += 1
		#----------------------------
		if (pUp + pDown >= 2):
			result = True
		else:
			pUp = 0
			pDown = 0
		
		if not result:
			#----------------------------------------GemB---------------
			#--------------------Horizontal----------
			#----------Right---------------
			cAux = gemB[1] + 1
			while ((cAux < len(mat[gemA[0]]))and(mat[gemB[0]][cAux].color == mat[gemB[0]][gemB[1]].color)):
				pRight += 1
				cAux += 1
			#----------Left----------------
			cAux = gemB[1] - 1
			while ((cAux >= 0)and(mat[gemB[0]][cAux].color == mat[gemB[0]][gemB[1]].color)):
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
			rAux = gemB[0] - 1
			while ((rAux >= 0)and(mat[rAux][gemB[1]].color == mat[gemB[0]][gemB[1]].color)):
				pUp += 1
				rAux -= 1
			#----------Down--------------
			rAux = gemB[0] + 1
			while ((rAux < len(mat))and(mat[rAux][gemB[1]].color == mat[gemB[0]][gemB[1]].color)):
				pDown += 1
				rAux += 1
			#----------------------------
			if (pUp + pDown >= 2):
				result = True
			else:
				pUp = 0
				pDown = 0

			if result:
				return gemB, pRight, pLeft, pUp, pDown
			else:
				aux = mat[gemA[0]][gemA[1]]
				mat[gemA[0]][gemA[1]] = mat[gemB[0]][gemB[1]]
				mat[gemB[0]][gemB[1]] = aux
		else:
			return gemA, pRight, pLeft, pUp, pDown

		return None


	def move(self, gemA, gemB):
		val = self.validateMove(self.mat, gemA, gemB)
		if val != None:
			return self.remap(val[0], val[1], val[2], val[3], val[4])
		else:
			return 0


	def remap(self, gem, pRight, pLeft, pUp, pDown):
		#--------------------Vertical----------------------
		rAux = gem[0]+pDown
		jump = pDown+pUp+1
		while ((rAux - jump) >= 0):
			if self.mat[rAux-jump][gem[1]].color != "X":
				if self.mat[rAux][gem[1]] != "X":
					self.mat [rAux][gem[1]] = self.mat[rAux-jump][gem[1]]
					rAux -= 1
				else:
					rAux -= 1
					jump -= 1
			else:
				jump += 1
		while (rAux >= 0):
			if self.mat[rAux][gem[1]].color != "X":
				self.mat[rAux][gem[1]] = Jewel(self.jColors[random.randrange(len(self.jColors)-1)])
			rAux -= 1
		#--------------------Horizontal--------------------
		#--------------------Right-------------------------
		cAux = gem[1]
		while (cAux <= (gem[1] + pRight)):
			rAux = gem[0]
			jump = 1
			while ((rAux - jump) >= 0):
				if self.mat[rAux-jump][cAux].color != "X":
					if self.mat[rAux][cAux] != "X":
						self.mat [rAux][cAux] = self.mat[rAux-jump][cAux]
						rAux -= 1
					else:
						rAux -= 1
						jump -= 1
				else:
					jump += 1
			while (rAux >= 0):
				if self.mat[rAux][cAux].color != "X":
					self.mat[rAux][cAux] = Jewel(self.jColors[random.randrange(len(self.jColors)-1)])
				rAux -= 1
			cAux += 1
		#--------------------Left--------------------------
		cAux = gem[1]
		while (cAux >= (gem[1] - pLeft)):
			rAux = gem[0]
			jump = 1
			while ((rAux - jump) >= 0):
				if self.mat[rAux-jump][cAux].color != "X":
					if self.mat[rAux][cAux] != "X":
						self.mat [rAux][cAux] = self.mat[rAux-jump][cAux]
						rAux -= 1
					else:
						rAux -= 1
						jump -= 1
				else:
					jump += 1
			while (rAux >= 0):
				if self.mat[rAux][cAux].color != "X":
					self.mat[rAux][cAux] = Jewel(self.jColors[random.randrange(len(self.jColors)-1)])
				rAux -= 1
			cAux -= 1

		points = (pRight + pLeft + pUp + pDown + 1)*50
		ver = self.verifyMat()
		if ver != None:
			points += self.remap((ver[0], ver[1]), ver[2], ver[3], ver[4], ver[5])

		if not self.validateMat(self.mat):
			self.generateMat()
		return points

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

	def draw(self, wObj):
		for r in range(len(self.mat)):
			for c in range(len(self.mat[r])):
				self.mat[r][c].draw(((32*c), (32*r)), wObj)