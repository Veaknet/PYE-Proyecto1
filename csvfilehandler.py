#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Clase manejadora de operaciones de escritura y lectura 
	de archivos csv
"""

import os
import csv

class CsvFileHandler(object):
	@classmethod
	def readFile(self, strFile=None, delimiter=","):
		csvfile = open(strFile, 'rb')
		jsonfile = {}
		if strFile == None or not os.path.isfile(strFile) or not os.access(strFile, os.R_OK):
			raise Exception("%s no es un archivo valido"%(strFile))
		else:
			spamreader = csv.reader(csvfile, delimiter=delimiter)
			for row in spamreader:
				jsonfile.update({row[0]:float(row[1])})
			csvfile.close()
			return jsonfile

	@classmethod
	def writeFile():
		pass