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
	#print csvsalida
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['[ton/yr]'])

	csvsalida.write(str(full))
	csvsalida.close()


def full(archive, noun, Type):
	archiveDays = os.path.join('..', 'data', 'in', 'constants', 'DAYS.xlsx')
	
	Mdays = convertXLSCSV(archiveDays)
	DH = int(float(Mdays[0][1]))
	DNH = int(float(Mdays[1][1]))

	archivePrincipal = archive
	matrizHabilPrincipal = convertCSVMatriz(archivePrincipal)
	archivePrincipal = archive.replace('Habil', 'NHabil')
	matrizNHabilPrincipal = convertCSVMatriz(archivePrincipal)

	archiveSecundary = archive.replace('Principal', 'Secundary')
	#print archiveSecundary
	matrizHabilSecundary = convertCSVMatriz(archiveSecundary)
	archiveSecundary = archive.replace('Habil', 'NHabil')
	matrizNHabilSecundary = convertCSVMatriz(archiveSecundary)

	head = matrizHabilPrincipal[0,:]
	
	index = 0
	full = 0
	fullHabilPrincipal = 0
	fullNHabilPrincipal = 0
	fullHabilSecundary = 0
	fullNHabilSecundary = 0

	for value in head:
		if value == 'UNIT': 
			colInit = index + 1
		if value == 'E24h':
			colEnd = index
		index += 1 

	for i in range(1, matrizHabilPrincipal.shape[0]):
		for x in range(colInit, colEnd):
			fullHabilPrincipal += float(matrizHabilPrincipal[i][x])

	for i in range(1, matrizNHabilPrincipal.shape[0]):
		for x in range(colInit, colEnd):
			fullNHabilPrincipal += float(matrizNHabilPrincipal[i][x])


	for i in range(1, matrizHabilSecundary.shape[0]):
		for x in range(colInit, colEnd):
			fullHabilSecundary += float(matrizHabilSecundary[i][x])

	for i in range(1, matrizNHabilSecundary.shape[0]):
		for x in range(colInit, colEnd):
			fullNHabilSecundary += float(matrizNHabilSecundary[i][x])

	noun = noun.strip('.csv')
	noun = noun.strip('_Habil')
	noun = noun.replace('Principal', 'Emission')

	index = 0
	
	fullHabilPrincipal = fullHabilPrincipal * DH / 1000000
	fullNHabilPrincipal = fullNHabilPrincipal * DNH / 1000000

	fullHabilSecundary = fullHabilSecundary * DH / 1000000
	fullNHabilSecundary = fullNHabilSecundary * DNH / 1000000

	
	full = fullHabilPrincipal + fullNHabilPrincipal + fullHabilSecundary + fullNHabilSecundary 
	#print fullHabil, '+' ,fullNHabil, '=', full
	writefull(str(full), noun, Type)

def totalemission(folder):

	listEmissions = listaCSV(folder)
	#print listEmissions
	if 'combustion' in folder:
		Type = 'combustion'
	elif 'wear' in folder: 
		Type = 'wear'

	for name in listEmissions:
		if '_Habil' in name and 'Principal' in name: 
			#print 'Paso'
			archive = os.path.join(folder, name)
			full(archive, name, Type)
