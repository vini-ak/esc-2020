import sys
import re

class Parser():
	"""Decodificador das unidades"""
	def __init__(self):
		self.__asm = open(sys.argv[1], 'r')


	def getAsmFile(self):
		return self.__asm


	def treatAsm(self):
		''' 
		Essa função é responsável por fazer o 
		tratamento da string e remover os coments 
		e whitespaces
		'''

		asm = self.getAsmFile()

		# Linhas sem espaços e brancos ou comentarios
		notWhiteLines = []


		# Verificando todas as linhas do arquivo, uma a uma
		for line in asm.readlines():
			# Caso a linha não seja comment ou whitespace, ela será adicionada em notWhiteLines
			if not (self.isWhiteLine(line) or self.isComent(line)):
				line = line.replace(" ", "")	# Removendo os espaços em branco
				commentPos = line.find("//")	# Verificando se a instrução possui comentarios
				if commentPos:
					line = line[:commentPos]	# Removendo os comentarios
				notWhiteLines.append(line)		# Salvando a instrução depois de ser tratada.

		asm.close()
		return notWhiteLines


	def isWhiteLine(self, string):
		''' Verifica se a linha é um espaço em branco '''
		return string.startswith("\n")
		 

	def isComent(self, string):
		''' Verifica se a linha é um comentário '''
		res = re.search("^//", string) == None
		return not res

	def isAInstruction(self, string):
		''' Verifica se a linha se trata de uma A-Instruction'''
		res = re.search("^@", string) == None 
		return not res

	def isCInstruction(self, string):
		return (not self.isAInstruction(string)) and (not string.startswith("(") and not string.endswith(")")) and (not "//" in string)


class AInstruction(object):
	"""docstring for  A-Instruction"""
	def __init__(self, value):
		self.__value = value

	def getValue(self):
		return bin(int(self.__value))

	def getA(self):
		a = str(self.getValue())[2:]
		return "0"*(16-len(a)) + a


class CInstruction(object):
	"""docstring for CInstruction"""
	def __init__(self, value):
		self.__value = value 

	def getValue(self):
		return self.__value

	def dest(self, d):
		dest = {"M": "001", "D": "010", "MD" : "011", "A" : "100", "AM" : "101", "AD" : "110", "AMD" : "111"}
		return dest[d]

	def jump(self, j):
		jump = {"JGT" : "001", "JEQ" : "010", "JGE" : "011", "JLT" : "100", "JNE" : "101", "JLE" : "110", "JMP" : "111"}
		return jump[j]

	def comp(self, c):
		# comp que contém A
		a0 = {"0" : "101010", "1" : "111111", "-1" : "111010", "D" : "001100", "A" : "110000", "!D" : "001101", "!A" : "110001", "-D" : "001111",\
		"-A" : "110011", "D+1" : "011111" , "A+1":"110111", "D-1":"001110", "A-1" : "110010", "D+A":"000010", "A+D" : "000010" ,"D-A":"010011", "A-D":"000111", "D&A":"000000", "A&D": "000000","D|A":"010101", "A|D" : "010101" }

		# comp que contém M
		a1 = {"M" : "110000", "!M" : "110001", "-M" : "110011", "M+1" : "110111", "M-1" : "110010", "D+M" : "000010", "M+D" : "000010","D-M" : "010011", "M-D" : "000111", "D&M" : "000000", "M&D" : "000000","D|M" : "010101", "M|D":"010101"}
		

		if c.find("M") != -1:
			return "1" + a1[c]
		else:
			return "0" + a0[c]


	def getC(self, string):
		
		# DEST e JUMP são opcionais
		dest = "000"
		jump = "000"

		if string.find("=") == -1 and string.find(";") == -1:
			comp = self.comp(string)


		else:
			if string.find("=") != -1:
				split1 = string.split("=")
				dest = self.dest(split1[0])
				comp = self.comp(split1[1])

			if string.find(";") != -1:
				split2 = string.split(";")
				comp = self.comp(split2[0])
				jump = self.jump(split2[1])

		return "111" + comp + dest + jump

		



# MAIN EXECUTION:
parser = Parser()
f = parser.treatAsm()

fileR = open(sys.argv[2], "w")

for line in f:
	if parser.isAInstruction(line):
		a = AInstruction(line[1:])
		line = a.getA()

	elif parser.isCInstruction(line):
		c = CInstruction(line)
		line = c.getC(line)

	# Escrevendo as linhas resultantes
	fileR.write(line+"\n")

fileR.close()
#print(f)
#f = parser.getAsmFile()
#print(f.readlines())