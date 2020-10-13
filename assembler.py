import sys
import re

class Parser():
	"""docstring for ClassName"""
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
			# Caso a linha não seja coment ou whitespace, ela será adicionada em notWhiteLines
			if not (self.isWhiteLine(line) or self.isComent(line)):
				notWhiteLines.append(line)

		asm.close()
		return notWhiteLines

	def isWhiteLine(self, string):
		return string.startswith("\n")
		 

	def isComent(self, string):
		res = re.search("^//", string) == None
		return not res


# MAIN EXECUTION:
parser = Parser()
f = parser.treatAsm()
print(f)
#f = parser.getAsmFile()
#print(f.readlines())