# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons


#from emitionmovil import *
import os
import sys
sys.path.append('core')
from emition import *
from matriz import *
from PMC import *
from clear import *



def vkt(matriz):
	head = matriz[0,:]

	index = 0
	for value in head: 
		if value == 'FID_LINK':
			colID = index
		if value == 'Shape_Leng': 
			colLargoVia = index
		if value == 'hora': 
			colhour = index
		if value == 'C5_GAS':
			colendHabil = index
		if value == 'NHC5_GAS':
			colendNhabil = index
		index += 1

	data = {}
	for i in range(1, matriz.shape[0]):
		ID = int(float(matriz[i][colID]))
		large = float(matriz[i][colLargoVia])
		hour = int(float(matriz[i][colhour]))


		if data.get(ID) is None: 
			data[ID] = {'hour': {}, 'large': large}

		entryhour = data[ID]['hour']
		if entryhour.get(hour) is None:
			entryhour[hour] = {'HABIL': {}, 'NHABIL': {}}

		entryCatHabil = entryhour[hour]['HABIL']

		for x in range(hour+1, colendHabil):
			name = matriz[0][x]
			if entryCatHabil.get(name) is None:
				entryCatHabil [name] = matriz[i][x]

		entryCatNHabil = entryhour[hour]['NHABIL']

		for x in range(colendHabil + 1, colendNHabil):
			name = matriz[0][x]
			if entryCatNHabil.get(name) is None:
				entryCatNHabil [name] = matriz[i][x]
		
	#print data
	keys = data.keys()
	for ID in keys:
		hours = data[ID]['hour'].keys()
		for hour in hours:
			Types = data[ID]['hour'][hour].keys()
			for Type in Types:
				categories = data[ID]['hour'][hour][Type].keys()
				for category in categories:
					operation = data[ID]['hour'][hour][Type][category] * data[ID]['large']
					data[ID]['hour'][hour][Type][category] = operation

	data['Result'] = {}
	for ID in keys:
		hours = data[ID]['hour'].keys()
		for hour in hours:
			data['Result'][hour] = {}
			Types = data[ID]['hour'][hour].keys()
			for Type in Types:
				data['Result'][hour][Type] = {}
				categories = data[ID]['hour'][hour][Type].keys()
				for category in categories:
					data['Result'][hour][Type][category] += data[ID]['hour'][hour][Type][category]
					

	print data['Result']

archivePrincipal = os.path.join('..', 'data', 'in','Link', 'PRINCIPALES', 'principalbinding.csv')
Mprincipales = convertCSVMatriz(archivePrincipal)


archiveSecundarias = os.path.join('..', 'data', 'in','Link', 'SECUNDARIAS', 'secundaryBinding.csv')
MSecundarias = convertCSVMatriz(archiveSecundarias)
vkt(MSecundarias)
