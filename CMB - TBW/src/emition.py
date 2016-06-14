# -*- coding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons


import os
import sys
sys.path.append('core')
from binding import *
from matriz import *
from speciation import *

def convert():

	archiveflows = os.path.join('..', 'data', 'in','Flows', 'promFinal.csv');

	archivelinkprincipal = os.path.join('..', 'data', 'in', 'link', 'PRINCIPAL', 'PRINCIPALES_1.xlsx');
	archivelinksecondary = os.path.join('..', 'data', 'in', 'link', 'SECUNDARIAS','SECUNDARIAS_1.xlsx');
	archivelinktm = os.path.join('..', 'data', 'in', 'link', 'TM', 'TM_1.xlsx');

	binding(archiveflows, archivelinkprincipal, 'principal')
	#print 'binding Principal Listo'
	binding(archiveflows, archivelinktm, 'TM')
	#print 'binding Transmilenio Listo'
	Type = 'HABIL'
	bindingsecondary(archiveflows, archivelinksecondary, Type)
	Type = 'NOHAB'
	bindingsecondary(archiveflows, archivelinksecondary, Type)

	archive1 = os.path.join('..', 'data', 'in', 'link', 'SECUNDARIAS', 'secundary_HABIL_binding.csv')
	archive2 = os.path.join('..', 'data', 'in', 'link', 'SECUNDARIAS', 'secundary_NOHAB_binding.csv')
	unions(archive1, archive2)
	#print 'binding Secundarias Listo'
	
def categoryVechicle(data, noun, pollution, Typo): 

	data2 = {}
	keys = data.keys()
	categories = ['>C5','AL','AT','B','BA','BT','MB','C2G','C2P','C3-C4','C5','ESP','INT','AUT', 'TX','M', 'CC']
	
	for key in keys:
		
		if data2.get(key) is None: 
			data2[key] = {}
			data2[key]['pollutants'] = {}
			data2[key]['General'] = {}
			data2[key]['General'] = data[key]['General']

		hours = data[key]['pollutants'].keys()
		
		entryhour = data2[key]['pollutants']
		
		for hour in hours: 	
			if entryhour.get(hour) is None:
				entryhour[hour] = {'Habil': {'>C5':[],'AL':[],'AT':[],'B':[],'BA':[],'BT':[],'MB':[],'C2G':[],'C2P':[],'C3-C4':[],'C5':[],'ESP':[],'INT':[],'TX':[], 'CC':[], 'AUT':[],'M':[]}, 'NHabil': {'>C5':[],'AL':[],'AT':[],'B':[],'BA':[],'BT':[],'MB':[],'C2G':[],'C2P':[],'C3-C4':[],'C5':[],'ESP':[],'INT':[],'TX':[], 'CC':[], 'AUT':[],'M':[]}}

			Types = data[key]['pollutants'][hour].keys()
			
			vehicles = data[key]['pollutants'][hour][Typo].keys()
			
			for vehicle in vehicles: 
				index = 0
				for value in vehicle: 
					if value == '_':
						possub = index
					index += 1 

				vehicle2 = vehicle[:possub]
				for cat in categories:		
					if cat == vehicle2:
						data2[key]['pollutants'][hour][Typo][cat].append(data[key]['pollutants'][hour][Typo][vehicle][0])

	keys = data2.keys()
	for key in keys: 
		hours = data2[key]['pollutants'].keys()
		for hour in hours:
			Types = data2[key]['pollutants'][hour].keys()
			for Type in Types: 
				categories = data2[key]['pollutants'][hour][Type].keys()
				for category in categories: 
					data2[key]['pollutants'][hour][Type][category] = sum(data2[key]['pollutants'][hour][Type][category])

	writevehicle(data2, noun, pollution, Typo,  1)

def categoryVechiclegrid():
	folder = os.path.join('..', 'out', 'category', 'link', '')
	archiveslink = list(folder)

	for archive in archiveslink: 
		noun = archive
		data = {}
		archive = folder + archive
		
		matriz = convertCSVMatriz(archive)
		head = matriz[0,:]
		index = 0
		for value in head: 
			if value =='FID_Grilla':
				colFIDGrid = index
			if value == 'COL':
				colCOL = index
			if value == 'ROW': 
				colROW = index
			if value == 'LAT': 
				colLAT = index
			if value == 'LON': 
				colLON = index
			if value == 'Category':
				colCat = index
			if value == 'Type':
				colType = index
			if value == 'POLNAME': 
				colPOLNAME = index
			index += 1

		for i in range(1, matriz.shape[0]):
			key = int(matriz[i][colFIDGrid])
			category = matriz[i][colCat]
			Type = matriz[i][colType]

			if data.get(key) is None: 
				data[key] = {'General': {'COL': [], 'ROW': [], 'LAT': [], 'LON': [], 'POLNAME': []}, 'Type': {}}

			if data[key]['General']['COL'] == []:
				data[key]['General']['COL'].append(matriz[i][colCOL])
				data[key]['General']['ROW'].append(matriz[i][colROW])
				data[key]['General']['LAT'].append(matriz[i][colLAT])
				data[key]['General']['LON'].append(matriz[i][colLON])
				data[key]['General']['POLNAME'].append(matriz[i][colPOLNAME])


			entryType = data[key]['Type']

			if entryType.get(Type) is None:
				entryType[Type] = {} 

			entrycategory = entryType[Type]

			if entrycategory.get(category) is None:
				entrycategory[category] = {}

			for hour in range(0, 24):
				if entrycategory[category].get(hour) is None:
					entrycategory[category][hour] = []

			hour = 0
			for x in range(colCat+1, matriz.shape[1]):
				

				entrycategory[category][hour].append(float(matriz[i][x]))
				hour += 1 
		
		keys = data.keys()
		for key in keys: 
			Types = data[key]['Type'].keys()
			for Type in Types: 
				categories = data[key]['Type'][Type].keys()
				for category in categories:
					hours = data[key]['Type'][Type][category].keys()
					for hour in hours: 
						data[key]['Type'][Type][category][hour] = sum(data[key]['Type'][Type][category][hour])

		
		pollution = 0
		writevehicle(data, noun, pollution, None, 2)

def categoryCarburant(data, noun, pollution, Typo): 
	data2 = {}
	keys = data.keys()
	for key in keys: 

		if data2.get(key) is None: 
			data2[key] = {}
			data2[key]['pollutants'] = {}
			data2[key]['General'] = {}
			data2[key]['General'] = data[key]['General']

		hours = data[key]['pollutants'].keys()
		
		for hour in hours: 
			entryhour = data2[key]['pollutants']
			
			if entryhour.get(hour) is None:
				entryhour[hour] = {Typo: {'GNV': [], 'GAS': [], 'DSEL': []}, 'NHabil': {'GNV': [], 'GAS': [], 'DSEL': []}}

			vehicles = data[key]['pollutants'][hour][Typo].keys()

			for vehicle in vehicles: 
				if 'GNV' in vehicle: 
					data2[key]['pollutants'][hour][Typo]['GNV'].append(data[key]['pollutants'][hour][Typo][vehicle][0])
				elif 'GAS' in vehicle: 
					data2[key]['pollutants'][hour][Typo]['GAS'].append(data[key]['pollutants'][hour][Typo][vehicle][0])
				elif 'DSEL' in vehicle: 
					data2[key]['pollutants'][hour][Typo]['DSEL'].append(data[key]['pollutants'][hour][Typo][vehicle][0])

	data = {}
	keys = data2.keys()
	for key in keys: 
		hours = data2[key]['pollutants'].keys()
		for hour in hours:
			Types = data2[key]['pollutants'][hour].keys()
			for Type in Types:
				carburants = data2[key]['pollutants'][hour][Type].keys()
				for carburant in carburants:
					data2[key]['pollutants'][hour][Type][carburant] = sum(data2[key]['pollutants'][hour][Type][carburant])

	
	writecarburant(data2, noun, pollution, Typo, 1)

def categoryCarburantgrid():
	folder = os.path.join('..', 'out', 'carburant', 'link', '')
	archiveslink = list(folder)

	for archive in archiveslink: 
		noun = archive
		data = {}
		archive = folder + archive
		
		matriz = convertCSVMatriz(archive)
		head = matriz[0,:]
		index = 0
		for value in head: 
			if value =='FID_Grilla':
				colFIDGrid = index
			if value == 'COL':
				colCOL = index
			if value == 'ROW': 
				colROW = index
			if value == 'LAT': 
				colLAT = index
			if value == 'LON': 
				colLON = index
			if value == 'Category':
				colCat = index
			if value == 'Type':
				colType = index
			if value == 'POLNAME': 
				colPOLNAME = index
			index += 1

		for i in range(1, matriz.shape[0]):
			key = int(matriz[i][colFIDGrid])
			category = matriz[i][colCat]
			Type = matriz[i][colType]

			if data.get(key) is None: 
				data[key] = {'General': {'COL': [], 'ROW': [], 'LAT': [], 'LON': [], 'POLNAME': []}, 'Type': {}}

			if data[key]['General']['COL'] == []:
				data[key]['General']['COL'].append(matriz[i][colCOL])
				data[key]['General']['ROW'].append(matriz[i][colROW])
				data[key]['General']['LAT'].append(matriz[i][colLAT])
				data[key]['General']['LON'].append(matriz[i][colLON])
				data[key]['General']['POLNAME'].append(matriz[i][colPOLNAME])


			entryType = data[key]['Type']

			if entryType.get(Type) is None:
				entryType[Type] = {} 

			entrycategory = entryType[Type]

			if entrycategory.get(category) is None:
				entrycategory[category] = {}


			for hour in range(0, 24):
				if entrycategory[category].get(hour) is None:
					entrycategory[category][hour] = []

			hour = 0
			for x in range(colCat+1, matriz.shape[1]):
				

				entrycategory[category][hour].append(float(matriz[i][x]))
				hour += 1 
		
		keys = data.keys()
		for key in keys: 
			Types = data[key]['Type'].keys()
			for Type in Types: 
				categories = data[key]['Type'][Type].keys()
				for category in categories:
					hours = data[key]['Type'][Type][category].keys()
					for hour in hours: 
						data[key]['Type'][Type][category][hour] = sum(data[key]['Type'][Type][category][hour])

		
		pollution = 0
		writecarburant(data, noun, pollution, None,  2)

def calculation(archive, noun, FactorEmissions, Typo):

	FEMatriz = convertXLSCSV(FactorEmissions)
	headFE = FEMatriz[0,:]
	
	#print 'calculation', noun, '-', Typo
	matriz = convertCSVMatriz(archive)
	head = matriz[0,:]

	index = 0
	name = []
	mat = []

	for value in head:
	    if value == 'Largo_via' or value == 'Largo_Via':
	        colL = index
	    if value == 'FID_Grilla':
	    	colGrilla = index
	    if value == 'hora':
	        colIH = index +1
	    if value == 'NH>C5_DSEL':
	        colFH = index
	    if value == 'NHC5_GAS':
	        colFNH = index + 1
	    if value == 'FID_LINK' or value == 'FID_Link':
	    	colID = index
	    if value == 'COL':
	        colCOL = index
	    if value == 'ROW':
	        colROW = index
	    if value == 'LAT' or value == 'LAT_1':
	        colLAT = index
	    if value == 'LON' or value == 'LON_1':
	        colLON = index
	    index += 1

	nameresh = matriz[0,colIH:colFH]
	nameresnh = matriz[0,colFH:colFNH]

	data = {}
	pollutant = {}
	
	index = 0
	for value in headFE:
		if value == 'Pollutant':
			colNamePollutant = index
		index += 1 

	for i in range(1, FEMatriz.shape[0]):
		polution = FEMatriz[i][0]
		if polution != '':
			if polution != 'Pollutant':
				if pollutant.get(polution) is None:
					pollutant[polution] = {}
				entrycategory = pollutant[polution]
		
				for value in nameresh:
					if entrycategory.get(value) is None:
						entrycategory[value] = []

				for value in nameresnh:
					if entrycategory.get(value) is None:
						entrycategory[value] = []

	for x in range(0, FEMatriz.shape[1]):
	 	category = FEMatriz[0][x]
	 	if category != 'Pollutant':
	  		if category != '':
	 			for i in range(2, FEMatriz.shape[0]):
	 	 			contaminante = FEMatriz[i][0]
	 	 			pollutant[contaminante][category].append(round(float(FEMatriz[i][x]),8))
	 	 			pollutant[contaminante]['NH'+category].append(round(float(FEMatriz[i][x]),8))
	  				pollutant[contaminante][category].append(round(float(FEMatriz[i][x+1]),8))
	  				pollutant[contaminante]['NH'+category].append(round(float(FEMatriz[i][x+1]),8))
	
	pollutants = pollutant.keys()	
	
	for poll in pollutants:
		data = {}
		
		for i in range(1,matriz.shape[0]):
		 	FID_LINK = int(float(matriz[i][colID]))
		 	hour = int(matriz[i][colIH-1])

			if data.get(FID_LINK) is None:
				data[FID_LINK] = {}
				data[FID_LINK]['General'] = {'FID_Grilla':[], 'COL':[], 'ROW':[], 'LAT': [], 'LON': []} 
				data[FID_LINK]['pollutants'] = {}

			if data[FID_LINK]['General']['FID_Grilla'] == []:
				data[FID_LINK]['General']['FID_Grilla'].append(int(float(matriz[i][colGrilla])))
				data[FID_LINK]['General']['COL'].append(int(float(matriz[i][colCOL])))
				data[FID_LINK]['General']['ROW'].append(int(float(matriz[i][colROW])))
				data[FID_LINK]['General']['LAT'].append(float(matriz[i][colLAT]))
				data[FID_LINK]['General']['LON'].append(float(matriz[i][colLON]))

			
			entryhour = data[FID_LINK]['pollutants']
			if entryhour.get(hour) is None: 
				entryhour[hour] = {}
				entryhour[hour][Typo] = {}

			
			entrycat = entryhour[hour][Typo]

			if Typo == 'Habil':
				for x in range(colIH, colFH):
					category = matriz[0][x]
					if entrycat.get(category) is None:
						entrycat[category] = []

				for x in range(colIH, colFH): 
				  	category = matriz[0][x]
				  	L = float(matriz[i][colL])/1000
				   	val = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][0])), 8))
				 	uncertainty = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][1])), 8))
				   	data[FID_LINK]['pollutants'][hour][Typo][category].append(val)
					data[FID_LINK]['pollutants'][hour][Typo][category].append(uncertainty)

			elif Typo == 'NHabil':
				for x in range(colFH, colFNH):
					category = matriz[0][x]
					if entrycat.get(category) is None:
						entrycat[category] = []

				for x in range(colFH, colFNH): 
				  	category = matriz[0][x]
					L = float(matriz[i][colL])/1000
					val = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][0])), 8))
				 	uncertainty = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][1])), 8))
					data[FID_LINK]['pollutants'][hour][Typo][category].append(val)
					data[FID_LINK]['pollutants'][hour][Typo][category].append(uncertainty)

		writedeparture(data, noun, poll, Typo)

		FID_Link = data.keys()

		for ID in FID_Link: 
			hours = data[ID]['pollutants'].keys()
			for hour in hours:
				categories = hours = data[ID]['pollutants'][hour][Typo].keys()
				sumaval = sumauncertainy = 0
				for category in categories:
					sumaval += data[ID]['pollutants'][hour][Typo][category][0]
					sumauncertainy += data[ID]['pollutants'][hour][Typo][category][1]
				
				data[ID]['pollutants'][hour][Typo] = []
				data[ID]['pollutants'][hour][Typo].append(sumaval)
				data[ID]['pollutants'][hour][Typo].append(sumauncertainy)
		

		if 'Brake' in FactorEmissions:
			writeemsions(data, noun, poll, Typo, 2)
		else:
			writeemsions(data, noun, poll, Typo, 1)

	matriz = None
	FEMatriz = None

def finality(folder, noun):

	hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	archive = folder + noun
	matriz = convertCSVMatriz(archive)

	head = matriz[0]
	index = 0
	data = {}
	houra = ['Hora 0', 'Hora 1', 'Hora 2', 'Hora 3', 'Hora 4', 'Hora 5', 'Hora 6', 'Hora 7', 'Hora 8', 'Hora 9', 'Hora 10', 'Hora 11', 'Hora 12', 'Hora 13', 'Hora 14', 'Hora 15', 'Hora 16', 'Hora 17', 'Hora 18', 'Hora 19', 'Hora 20', 'Hora 21', 'Hora 22', 'Hora 23']
	posHour = []

	for value in head:
		if value == 'FID_Grilla':
			colID = index
		if value == 'COL':
			colCOL = index
		if value == 'ROW':
			colROW = index
		if value == 'LAT':
			colLAT = index
		if value == 'LON':
			colLON = index
		if value == 'Contaminante':
			colCont = index
		for h in houra:
			if value == h:
				posHour.append(index)
		index += 1 

	for i in range(1, matriz.shape[0]):
		FID_Grilla = matriz[i][colID]
		pollutant = matriz[i][colCont]
		
		if data.get(FID_Grilla) is None: 
			data[FID_Grilla] = {}
			data[FID_Grilla]['General'] = {'COL':[], 'ROW':[], 'LAT': [], 'LON': []}
			data[FID_Grilla]['pollutants'] = {}

		if data[FID_Grilla]['General']['COL'] == []:
			data[FID_Grilla]['General']['COL'].append(matriz[i][colCOL])
			data[FID_Grilla]['General']['ROW'].append(matriz[i][colROW])
			data[FID_Grilla]['General']['LAT'].append(matriz[i][colLAT])
			data[FID_Grilla]['General']['LON'].append(matriz[i][colLON])

		entrypollution = data[FID_Grilla]['pollutants'] 
		
		if entrypollution.get(pollutant) is None:
			entrypollution[pollutant] = {}

		entryhour = entrypollution[pollutant]
		for hour in hours:
			if entryhour.get(hour) is None:
				entryhour[hour] = []

			data[FID_Grilla]['pollutants'][pollutant][hour].append(matriz[i][posHour[int(hour)]])


	ID_Grilla = data.keys()
	for ID in ID_Grilla: 
		pollutants = data[ID]['pollutants'].keys()
		for pollutant in pollutants:
			hours = pollutants = data[ID]['pollutants'][pollutant].keys()
			for hour in hours:
				suma = eval('+'.join(data[ID]['pollutants'][pollutant][hour]))
				data[ID]['pollutants'][pollutant][hour] = []
				data[ID]['pollutants'][pollutant][hour].append(suma)
	
	if 'combustion' in folder: 
		folder = os.path.join('..', 'data','out', 'emissions', 'grid', 'combustion', '')
	elif 'wear' in folder:
		folder = os.path.join('..', 'data','out', 'emissions', 'grid', 'wear', '')
	
	wcsv(data, noun, folder)

def list(folder):
	lstDir = os.walk(folder)
	lstFilesEmissions = []
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def createdata(archive, Typo): 
	data = {}
	matriz = convertCSVMatriz(archive)

	head = matriz[0,:]
	index = 0
	for value in head:
		if value == 'FID_LINK':
			colLink = index
		if value == 'FID_Grilla':
			colGrilla = index
		if value == 'COL': 
			colCOL = index
		if value == 'ROW': 
			colROW = index
		if value == 'LAT':
			colLAT = index
		if value == 'LON':
			colLON = index
		if value == 'hora':
			colHour = index
		index += 1
		
	for i in range(1, matriz.shape[0]):
		key = matriz[i][colLink]
		hour = int(matriz[i][colHour])
		if data.get(key) is None: 
			data[key] = {'General': {'LAT': [], 'LON': [], 'COL': [], 'ROW': [], 'FID_Grilla': []}, 'pollutants': {}}

		entryhour = data[key]['pollutants']
		if entryhour.get(hour) is None: 
			entryhour[hour] = {Typo: {}}


		if data[key]['General']['LAT'] == []:
			data[key]['General']['LAT'].append(matriz[i][colLAT])
			data[key]['General']['LON'].append(matriz[i][colLON])
			data[key]['General']['ROW'].append(matriz[i][colROW])
			data[key]['General']['COL'].append(matriz[i][colCOL])
			data[key]['General']['FID_Grilla'].append(matriz[i][colGrilla])


		entrycategory = entryhour[hour][Typo]
		for x in range(colHour+1, matriz.shape[1]):
			name = head[x]
			if entrycategory.get(name) is None: 
				entrycategory[name] = []
				entrycategory[name].append(float(matriz[i][x]))

	return data
