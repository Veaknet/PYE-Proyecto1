#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################
## SimPy Implementation       ##
## FARM Desease Implemetation ##
## v.1.0.0                    ##
################################

# Librerias necesarias de sistema
from time import *
from random import *

# Librerias propietarias de la implementacion
from csvfilehandler import *
from simulation import *

seed(time())

# Metodo principal de ejecucion
def main():
	# Leyendo archivo de entrada
	fileData = CsvFileHandler.readFile('entrada.csv')

	# Realizar la simulacion Cant_Corr veces
	#for i in xrange(int(fileData['Cant_Corr'])):
	for i in xrange(int(1)):
		print '==== ==== ==== (Corrida %d) ==== ==== ====' % (i+1)
		simulate(fileData)

if __name__ == '__main__':
	main()
