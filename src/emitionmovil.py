# -*- coding: utf-8 -*-
#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons


import os
import sys
sys.path.append('core')
from brinding import *
from excelmatriz import *
from speciation import *

def convert():

	archiveflows = os.path.join('..', 'data','Flows', 'promFinal.csv');

	archivelinkprincipal = os.path.join('..', 'data', 'datalink', 'PRINCIPALES.xlsx');
	archivelinksecondary = os.path.join('..', 'data', 'datalink', 'SECUNDARIAS.xlsx');
	archivelinktm = os.path.join('..', 'data', 'datalink', 'TM.xlsx');


	brinding(archiveflows, archivelinkprincipal, 'principal')
	print 'brinding Principal Listo'
	brinding(archiveflows, archivelinktm, 'TM')
	print 'brinding Transmilenio Listo'
	brindingsecondary(archiveflows, archivelinksecondary)
	print 'brinding Secundarias Listo'

def categoryVechicle(data, noun, pollution): 

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
			
			#Habil 
			vehiclesHabil = data[key]['pollutants'][hour]['Habil'].keys()
			
			for vehicle in vehiclesHabil: 
				index = 0
				for value in vehicle: 
					if value == '_':
						possub = index
					index += 1 

				vehicle2 = vehicle[:possub]

				for cat in categories:		
					if cat == vehicle2:
						data2[key]['pollutants'][hour]['Habil'][cat].append(data[key]['pollutants'][hour]['Habil'][vehicle][0])

			#NoHabil
			vehiclesNHabil = data[key]['pollutants'][hour]['NHabil'].keys()
			for vehicle in vehiclesNHabil: 
				index = 0
				for value in vehicle: 
					if value == '_':
						possub = index
					index += 1 

				vehicle2 = vehicle[2:possub]

		 		for cat in categories: 		
		 			if cat == vehicle2:
		 				data2[key]['pollutants'][hour]['NHabil'][cat].append(data[key]['pollutants'][hour]['NHabil'][vehicle][0])


	#print data2
	keys = data2.keys()
	for key in keys: 
		hours = data2[key]['pollutants'].keys()
		for hour in hours:
			Types = data2[key]['pollutants'][hour].keys()
			for Type in Types: 
				categories = data2[key]['pollutants'][hour][Type].keys()
				for category in categories: 
					data2[key]['pollutants'][hour][Type][category] = sum(data2[key]['pollutants'][hour][Type][category])

	writevehicle(data2, noun, pollution, 1)

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
		writevehicle(data, noun, pollution, 2)

def categoryCarburant(data, noun, pollution): 
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
				entryhour[hour] = {'Habil': {'GNV': [], 'GAS': [], 'DSEL': []}, 'NHabil': {'GNV': [], 'GAS': [], 'DSEL': []}}

			vehiclesHabil = data[key]['pollutants'][hour]['Habil'].keys()

			for vehicle in vehiclesHabil: 
				if 'GNV' in vehicle: 
					data2[key]['pollutants'][hour]['Habil']['GNV'].append(data[key]['pollutants'][hour]['Habil'][vehicle][0])
				elif 'GAS' in vehicle: 
					data2[key]['pollutants'][hour]['Habil']['GAS'].append(data[key]['pollutants'][hour]['Habil'][vehicle][0])
				elif 'DSEL' in vehicle: 
					data2[key]['pollutants'][hour]['Habil']['DSEL'].append(data[key]['pollutants'][hour]['Habil'][vehicle][0])

			vehiclesNHabil = data[key]['pollutants'][hour]['NHabil'].keys()

			for vehicle in vehiclesNHabil: 
				if 'GNV' in vehicle: 
					data2[key]['pollutants'][hour]['NHabil']['GNV'].append(data[key]['pollutants'][hour]['NHabil'][vehicle][0])
				elif 'GAS' in vehicle: 
					data2[key]['pollutants'][hour]['NHabil']['GAS'].append(data[key]['pollutants'][hour]['NHabil'][vehicle][0])
				elif 'DSEL' in vehicle: 
					data2[key]['pollutants'][hour]['NHabil']['DSEL'].append(data[key]['pollutants'][hour]['NHabil'][vehicle][0])
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

	
	writecarburant(data2, noun, pollution, 1)

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
		writecarburant(data, noun, pollution, 2)

def calculation(archive, noun, FactorEmissions):

	FEMatriz = convertXLSCSV(FactorEmissions)
	headFE = FEMatriz[0,:]
	
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
	#print nameresh
	nameresnh = matriz[0,colFH:colFNH]
	#print nameresnh

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
				entryhour[hour]['Habil'] = {}
				entryhour[hour]['NHabil'] = {}

			
			entrycat = entryhour[hour]['Habil']
			for x in range(colIH, colFH):
				category = matriz[0][x]
				if entrycat.get(category) is None:
					entrycat[category] = []

			entrycat = entryhour[hour]['NHabil']
			for x in range(colFH, colFNH):
				category = matriz[0][x]
				if entrycat.get(category) is None:
					entrycat[category] = []

			for x in range(colIH, colFH): 
			  	category = matriz[0][x]
			  	L = float(matriz[i][colL])/1000
			   	val = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][0])), 8))
			 	uncertainty = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][1])), 8))
			   	data[FID_LINK]['pollutants'][hour]['Habil'][category].append(val)
				data[FID_LINK]['pollutants'][hour]['Habil'][category].append(uncertainty)


			for x in range(colFH, colFNH): 
			  	category = matriz[0][x]
				L = float(matriz[i][colL])/1000
				val = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][0])), 8))
			 	uncertainty = (round((((float(matriz[i][x]) * L) * pollutant[poll][category][1])), 8))
				data[FID_LINK]['pollutants'][hour]['NHabil'][category].append(val)
				data[FID_LINK]['pollutants'][hour]['NHabil'][category].append(uncertainty)

		categoryVechicle(data, noun, poll)
		categoryCarburant(data, noun, poll)
		
		FID_Link = data.keys()

		for ID in FID_Link: 
			hours = data[ID]['pollutants'].keys()
			for hour in hours:
				tipo = hours = data[ID]['pollutants'][hour].keys()
				for tip in tipo:
					categories = hours = data[ID]['pollutants'][hour][tip].keys()
					sumaval = sumauncertainy = 0
					for category in categories:
						sumaval += data[ID]['pollutants'][hour][tip][category][0]
						sumauncertainy += data[ID]['pollutants'][hour][tip][category][1]
					
					data[ID]['pollutants'][hour][tip] = []
					data[ID]['pollutants'][hour][tip].append(sumaval)
					data[ID]['pollutants'][hour][tip].append(sumauncertainy)
		if 'Brake' in FactorEmissions:
			writeemsions(data, noun, poll, 2)
		else:
			writeemsions(data, noun, poll, 1)

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
		folder = os.path.join('..', 'out', 'emissions', 'grid', 'combustion', '')
	elif 'wear' in folder:
		folder = os.path.join('..', 'out', 'emissions', 'grid', 'wear', '')
	
	wcsv(data, noun, folder)

def list(folder):
	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(folder)   #os.walk()Lista directorios y ficheros
	datos = {}
	lstFilesEmissions = []
	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def init():
	print 'empieza proceso'
	convert()
	FactorEmissions = os.path.join('..', 'data', 'FEmition', 'FactoresEmision.xlsx')
	FactoresEmissionBrake = os.path.join('..', 'data', 'FEmition', 'FEBrake.xlsx')

	
	principal = os.path.join('..', 'data', 'datalink', 'principalbrinding.csv')
	calculation(principal, 'Principal', FactorEmissions)
	calculation(principal, 'Principal', FactoresEmissionBrake)
	print 'Calculo para Principales Habil y No Habil Listos'
	
	TM = os.path.join('..', 'data', 'datalink', 'TMbrinding.csv')
	calculation(TM, 'TM', FactorEmissions)
	calculation(TM, 'TM', FactoresEmissionBrake)
	print 'Calculo para Transmilenio Habil y No Habil Listos'
	
	secundarias = os.path.join('..', 'data', 'datalink', 'secundarybrinding.csv')
	calculation(secundarias, 'Secundary', FactorEmissions)
	calculation(secundarias, 'Secundary', FactoresEmissionBrake)
	print 'Calculo para Secundarias Habil y No Habil Listos'

	foldercombustion = os.path.join('..', 'out', 'emissions', 'link', 'combustion', '')
	listFilesEmissions = list(foldercombustion)

	for File in listFilesEmissions:
		finality(foldercombustion, File)

	folderwear = os.path.join('..', 'out', 'emissions', 'link', 'wear', '')
	listFilesEmissions = list(folderwear)

	for File in listFilesEmissions:
		finality(folderwear, File)
	
	gridCombustion = os.path.join('..', 'out', 'emissions', 'grid', 'combustion', '')
	brindingfinality(gridCombustion)

	gridWear = os.path.join('..', 'out', 'emissions', 'grid', 'wear', '')
	brindingfinality(gridWear)

	ArchiveHabilWear = os.path.join('..', 'out', 'emissions', 'emissionsHabilWear.csv')
	ArchiveHabilConbustion = os.path.join('..', 'out', 'emissions', 'emissionsHabilConbustion.csv')
	final(ArchiveHabilWear)
	final(ArchiveHabilConbustion)
	
	ArchiveNHabilWear = os.path.join('..', 'out', 'emissions', 'emissionsNoHabilWear.csv')
	ArchiveNHabilConbustion = os.path.join('..', 'out', 'emissions', 'emissionsNoHabilConbustion.csv')
	final(ArchiveNHabilWear)
	final(ArchiveNHabilConbustion)

	print 'speciation PM2.5 BRAKE'
	archivespeciation = os.path.join('..', 'data', 'speciation', 'BRAKE_SCP_PROF_PM25.xlsx')
	folderwear = os.path.join('..', 'out', 'emissions', 'grid', 'wear', '')
	speciationwear(archivespeciation, folderwear)
	print 'Testing'
	testing('PM2.5 BRAKE')

	print 'speciation PM2.5 TIRE'
	archivespeciation = os.path.join('..', 'data', 'speciation', 'TIRE_SCP_PROF_PM25.xlsx')
	folderwear = os.path.join('..', 'out', 'emissions', 'grid', 'wear', '')
	speciationwear(archivespeciation, folderwear)
	print 'Testing'
	testing('PM2.5 TIRE')

	foldercombustion = os.path.join('..', 'out', 'emissions', 'grid', 'combustion', '')
	speciationcombustion(foldercombustion)

	#brinding speciation in folder /out/speciation/brinding
	print 'Start brinding speciation'
	foldercombustion = os.path.join('..', 'out', 'speciation', 'combustion', '')
	brindingspeciation(foldercombustion, 'combustion')	

	folderwear = os.path.join('..', 'out', 'speciation', 'wear', '')
	brindingspeciation(folderwear, 'wear')	

	foldercombustion = os.path.join('..', 'out', 'speciation', 'brinding', 'combustion', '')
	archivescombustion = list(foldercombustion)

	for combustion in archivescombustion:
		archive = foldercombustion + combustion
		#print archive
		final(archive)

	folderwearTIRE = os.path.join('..', 'out', 'speciation', 'brinding', 'wear', 'TIRE', '')
	archiveswearTIRE = list(folderwearTIRE)

	for wear in archiveswearTIRE:
		archive = folderwearTIRE + wear
		final(archive)

	folderwearBRAKE = os.path.join('..', 'out', 'speciation', 'brinding', 'wear', 'BRAKE', '')
	archiveswearBRAKE = list(folderwearBRAKE)

	for wear in archiveswearBRAKE:
		archive = folderwearBRAKE + wear
		final(archive)

	print 'brinding speciation OK'
	print '*------------------------------------*'
	print 'Archivo NoHabil Listo'
	print 'End'
