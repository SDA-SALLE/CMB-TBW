#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from matriz import *
from wcsv import *
import os
import json 
import xlrd 

def listaCSV(direccion):

	path = os.path.join(direccion,'')

	lstFilesEmissions = []

	lstDir = os.walk(path)  
	datos = {}

	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def writefull(full, noun, Type): 

	if Type == 'combustion':
		folder = os.path.join('..', 'data', 'out', 'TotalEmissions', 'combustion', '')
	elif Type == 'wear': 
		folder = os.path.join('..', 'data', 'out', 'TotalEmissions', 'wear', '')

	csvsalida = open(folder + noun + "_E(TYear).csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['[ton/yr]'])

	csvsalida.write(str(full))
	csvsalida.close()


def full(archive, noun, Type):
	archiveDays = os.path.join('..', 'data', 'in', 'constants', 'DAYS.xlsx')
	Mdays = convertXLSCSV(archiveDays)
	DH = int(float(Mdays[0][1]))
	DNH = int(float(Mdays[1][1]))

	matriz = convertCSVMatriz(archive)
	head = matriz[0,:]
	index = 0
	full = 0

	for value in head:
		if value == 'UNIT': 
			colInit = index + 1
		if value == 'E24h':
			colEnd = index

		index += 1 

	for i in range(1, matriz.shape[0]):
		for x in range(colInit, colEnd):
			full += float(matriz[i][x])

	noun = noun.strip('.csv')
	index = 0
	for i in noun: 
		if i == '_':
			init = index
		index += 1

	identy = noun[init+1:]
	#print identy
	if identy == 'NHabil': 
		#print noun
		full = full * DNH / 1000000
	if identy == 'Habil': 
		full = full * DH / 1000000


	writefull(str(full), noun, Type)

def totalemission(folder):

	listEmissions = listaCSV(folder)
	#print listEmissions
	if 'combustion' in folder:
		Type = 'combustion'
	elif 'wear' in folder: 
		Type = 'wear'

	for name in listEmissions:
		archive = os.path.join(folder, name)
		full(archive, name, Type)
