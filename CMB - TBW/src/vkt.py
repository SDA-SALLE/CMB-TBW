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



def vkt(matriz, noun):
	head = matriz[0,:]

	index = 0
	for value in head:
		if value == 'FID_LINK':
			colID = index
		if value == 'Largo_via' or value == 'Largo_Via':
			colLargoVia = index
		if value == 'hora':
			colhour = index
		if value == 'TX_GNV':
			colendHabil = index+1
		if value == 'NHTX_GNV':
			colendNHabil = index
		index += 1

	#print matriz[0,colendHabil:matriz.shape[1]]

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
		
		for x in range(colhour+1, colendHabil):
			name = matriz[0][x]
			if entryCatHabil.get(name) is None:
				entryCatHabil [name] = matriz[i][x]

		entryCatNHabil = entryhour[hour]['NHABIL']

		for x in range(colendHabil, matriz.shape[1]):
			name = matriz[0][x]
			if entryCatNHabil.get(name) is None:
				entryCatNHabil [name] = matriz[i][x]
		
	#print data
	keys = data.keys()
	for ID in data:
		hours = data[ID]['hour']
		for hour in hours:
			Types = hours[hour]
			for Type in Types:
				categories = Types[Type]
				for category in categories:
					operation = float(categories[category]) * float(data[ID]['large']) / 1000
					categories[category] = operation

	data['Result'] = {}

	for ID in keys:
		hours = data[ID]['hour'].keys()
		for hour in hours:
			Types = data[ID]['hour'][hour].keys()
			data['Result'][hour] ={}
			for Type in Types:
			    data['Result'][hour][Type] = {}
			    categories = data[ID]['hour'][hour][Type].keys()
			    for category in categories:
			        data['Result'][hour][Type][category] = 0

	for ID in keys:
		hours = data[ID]['hour'].keys()
		for hour in hours:
			Types = data[ID]['hour'][hour].keys()
			for Type in Types:
			    categories = data[ID]['hour'][hour][Type].keys()
			    for category in categories:
			       data['Result'][hour][Type][category] += data[ID]['hour'][hour][Type][category]

	writevkt(noun, data)

def writevkt(noun, data):
	folder = os.path.join('..', 'data', 'out', '')
	csvsalida = open (folder + noun + '_vkt.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	
	csvsalida.write('Hora')
	csvsalida.write(',')
	csvsalida.write('Tipo Dia')
	
	categoriesHabil = sorted(data['Result'][0]['HABIL'])
	#print categoriesHabil
	for category in categoriesHabil:
		csvsalida.write(',')
		csvsalida.write(category)
	csvsalida.write('\n')
	

	#for Type in ['HABIL', 'NHABIL']:
	hours = data['Result']
	for hour in hours:
		csvsalida.write(str(hour))
		csvsalida.write(',')
		csvsalida.write('HABIL')
		categories = sorted(data['Result'][hour]['HABIL'])
		for category in categories:
			csvsalida.write(',')
			csvsalida.write(str(data['Result'][hour]['HABIL'][category]))

		csvsalida.write('\n')

	for hour in hours:
		csvsalida.write(str(hour))
		csvsalida.write(',')
		csvsalida.write('NHABIL')
		categories = sorted(data['Result'][hour]['NHABIL'])
		for category in categories:
			csvsalida.write(',')
			csvsalida.write(str(data['Result'][hour]['NHABIL'][category]))

		csvsalida.write('\n')

def sum(archives1, archives2):
	data = {}
	head = archives1[0,:]
	index = 0
	for value in head:
		if value == 'Hora':
			colhour = index
		if value == 'Tipo Dia':
			colType = index
		index += 1


	for i in range(1, archives1.shape[0]):
		hour = int(archives1[i][colhour])
		Type = archives1[i][colType]
		
		if data.get(Type) is None:
			data[Type] = {}
		
		entryType = data[Type]
		
		if entryType.get(hour) is None:
			entryType[hour] = {}

		entryCategory = entryType[hour]

		for x in range(2, archives1.shape[1]):
			entryCategory[archives2[0][x]] = float(archives1[i][x]) + float(archives2[i][x])
			

	#print data

	folder = os.path.join('..', 'data', 'out', '')
	csvsalida = open (folder + 'suma_vkt.csv', 'w')

	csvsalida.write('Hora')
	csvsalida.write(',')
	csvsalida.write('Tipo Dia')
	
	categoriesHabil = sorted(data['HABIL'][0])
	
	for category in categoriesHabil:
		csvsalida.write(',')
		csvsalida.write(category)
	csvsalida.write('\n')

	Types = data.keys()
	
	for Type in Types:
		hours = data[Type].keys()
		for hour in hours:
			csvsalida.write(str(hour))
			csvsalida.write(',')
			csvsalida.write(Type)
			categories = sorted(data[Type][hour])
			for category in categories:
				csvsalida.write(',')
				csvsalida.write(str(data[Type][hour][category]))
			csvsalida.write('\n')