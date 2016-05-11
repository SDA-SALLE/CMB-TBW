#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from excelmatriz import *
from wcsv import *
import json
import os
import csv


def listaCSV(direccion):
   	#Variable para la ruta al directorio
	path = os.path.join(direccion,'')
	#print direccion

	#Lista vacia para incluir los ficheros
	lstFilesEmissions = []

	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
	datos = {}

	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def brinding(flows, links, noun):
	
	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)

	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))

		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = int(MFlows[y][colhour])

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	folder = os.path.join("..", 'data', 'datalink', '')
	writebinding(folder, data, noun)

def brindingsecondary(flows, links):

	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)
	
	Intermedia = 0.37
	Local = 0.22
	Activity = ['L', 'AUT_Gas', 'AUT_Gas', 'AUT_GNV', 'CC_Gas', 'CC_Dsel', 'CC_GNV', 'TX_Gas', 'TX_GNV', 'C', 'MB_Dsel', 'ESP', 'ESP_Gas', 'ESP_Dsel', 'ESP_GNV', 'M', 'M_Gas']
	ResidencialAct = 0.22
	NotActivity = [ 'B', 'B_Dsel', 'C2P', 'C2P_Dsel', 'C2P_Gas', 'C2P_GNV', 'BT', 'BT_Dsel', 'AL', 'AL_Dsel', 'AT', 'AT_Dsel', 'BA', 'BA_Dsel', 'INT', 'INT_Dsel', 'INT_Gas','INT_GNV', 'C2G', 'C2G_Dsel', 'C2G_Gas', 'C2G_GNV', 'C3-C4', 'C3-C4_Dsel', 'C3-C4_Gas', 'C3-C4_GNV', 'C5', 'c5_Dsel', 'c5_Gas', 'c5_GNV', '>C5', '>c5_Dsel', '>c5_Gas', '>c5_GNV']
	ResidencialNotAct = 0


	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))
		#print 'Trabajando con el Link #', FID
		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = int(MFlows[y][colhour])

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	FID = data.keys()
	
	for ID in FID:
		clasifi = data[ID]['link']['CLASIFI_SU'][0]
		print 'Trabajando con Link #', ID
		types = data[ID]['flows'].keys()
		for typ in types:
			hour = data[ID]['flows'][typ].keys()
			for hr in hour:
				namevehicle = sorted(data[ID]['flows'][typ][hr].keys())
				
				if clasifi == 'Local':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Local

				if clasifi == 'Intermedia':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Intermedia 

				if clasifi == 'Residencial':

					for Vehicle in Activity: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialAct

					for Vehicle in NotActivity:
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialNotAct


	folder = os.path.join("..", "data", "datalink", '')
	writebinding(folder, data, "secundary")

def brindingfinality(folderbrinding):
	
	folder2 = os.path.join('..', 'out', 'emissions', '')
	if 'wear' in folderbrinding:
		csvsalida1 = open (folder2 + 'emissionsHabilWear.csv', 'w')
		csvsalida2 = open (folder2 + 'emissionsNoHabilWear.csv', 'w')
	elif 'combustion' in folderbrinding:
		csvsalida1 = open (folder2 + 'emissionsHabilConbustion.csv', 'w')
		csvsalida2 = open (folder2 + 'emissionsNoHabilConbustion.csv', 'w')


	salida1 = csv.writer(csvsalida1, delimiter=',')
	salida2 = csv.writer(csvsalida2, delimiter=',')

	listHabil = []
	listNHabil = []
	
	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(folderbrinding)   #os.walk()Lista directorios y ficheros
	datos = {}
	lstFilesEmissions = []
	
	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == ".csv"):
	        	lstFilesEmissions.append(nombreFichero+extension)
	
	#Clasificacion Archivos
	for name in lstFilesEmissions: 
		index = 0
		for l in name:
			if "_" == l:
				possub = index

			index += 1 
		
		if  "_Habil" in name:
			listHabil.append(name)
		elif "_NHabil" in name:
			listNHabil.append(name)

	cont = 0
	for name in listHabil:
		archive = folderbrinding + name 
		matriz = convertCSVMatriz(archive)
		if cont == 0:
			salida1.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])			
			cont += 1

		for i in range(1, matriz.shape[0]):
			cod = matriz[i][0] + matriz[i][1]
			salida1.writerow(matriz[i,:])

	csvsalida1.close()

	cont = 0
	for name in listNHabil:
		archive = folderbrinding + name 
		matriz = convertCSVMatriz(archive)

		if cont == 0:
			salida2.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])			
			cont += 1

		for i in range(1, matriz.shape[0]):
			salida2.writerow(matriz[i,:])

	csvsalida2.close()

def final(Archive):
	
	data = {}

	#print Archive
	matriz = convertCSVMatriz(Archive)
	head = matriz[0,:]
	index = 0
	
	for value in head: 
		if value == 'ROW': 
			colROW = index
		if value == 'COL': 
			colCOL = index
		if value == 'LAT': 
			colLAT = index
		if value == 'LON':
			colLON = index
		if value == 'POLNAME':
			colPollname = index
		if value == 'UNIT':
			colUnit = index
		index += 1


	for i in range(1, matriz.shape[0]):
		keys = matriz[i][colROW] + matriz[i][colCOL] + matriz[i][colPollname]
		
		if data.get(keys) is None: 
			data[keys] = {}
			data[keys]['hours'] = {}
			data[keys]['GENERAL'] = {'ROW': [], 'COL': [], 'LAT': [], 'LON': [], 'POLNAME': [], 'UNIT':[]}

		
		for hour in range(0, 25):
			data[keys]['hours'][hour] = []

	
	for i in range(1, matriz.shape[0]):
		keys = matriz[i][colROW] + matriz[i][colCOL] + matriz[i][colPollname]
		if data[keys]['GENERAL']['ROW'] == []:
			data[keys]['GENERAL']['ROW'].append(matriz[i][colROW])
			data[keys]['GENERAL']['COL'].append(matriz[i][colCOL])
			data[keys]['GENERAL']['LAT'].append(matriz[i][colLAT])
			data[keys]['GENERAL']['LON'].append(matriz[i][colLON])
			data[keys]['GENERAL']['POLNAME'].append(matriz[i][colPollname])
			data[keys]['GENERAL']['UNIT'].append(matriz[i][colUnit])

		hour = 0
		for x in range(6, matriz.shape[1]):
			data[keys]['hours'][hour].append(matriz[i][x])
			hour += 1

	keys = data.keys()
	for key in keys: 
		hours = data[key]['hours'].keys()
		for hour in hours:
			if hour == 'GENERAL': 
				pass
			else:
				suma = eval('+'.join(data[key]['hours'][hour]))
				data[key]['hours'][hour] = []
				data[key]['hours'][hour].append(suma)

	
	csvsalida = open(Archive, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	salida.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])
	names = data.keys()

	for key in names: 
		csvsalida.write(data[key]['GENERAL']['ROW'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['COL'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['LAT'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['LON'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['POLNAME'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['UNIT'][0])
		csvsalida.write(',')
		hours = data[key]['hours'].keys()
		for hour in hours:
			csvsalida.write(str(data[key]['hours'][hour][0]))
			csvsalida.write(',')
		csvsalida.write('\n')

	csvsalida.close ()

def brindingspeciation(folder, noun): 
	print folder
	listaspeciation = listaCSV(folder)

	if noun == 'combustion':
		listVOC = ['PAR', 'OLE', 'TOL', 'XYL', 'FORM', 'ALD2', 'ETH', 'ISOP', 'MEOH', 'ETHA', 'IOLE', 'ALDX', 'TERP', 'UNR', 'UNK']
		listGAS = ['CO', 'CO2', 'SO2']
		listsepared = ['CH4', 'BEN', 'PM10', 'PM2.5']
		archivesSpeciesHabil = []
		achivesSpeciesNHabil = []
		archivesVOCHabil = []
		archivesVOCNHabil = []
		archivesGASHabil = []
		archivesGASNHabil = []
		archivesSeparedHabil = []
		archivesSeparedNHabil = []
		
		for value in listaspeciation: 
			index = 0
			for pos in value: 
				if pos == '_':
					end = index
					break
				index += 1
			
			pollutant =  value[:end]

			if pollutant[0] == 'P': 
				if pollutant != 'PAR' and pollutant != 'PM10' and pollutant != 'PM2.5':
					if '_Habil' in value:
						archivesSpeciesHabil.append(value)
					if '_NHabil' in value:
						achivesSpeciesNHabil.append(value)	


			for VOC in listVOC: 
				if VOC == pollutant: 
					#print VOC, pollutant
					if '_NHabil' in value:
						archivesVOCNHabil.append(value)
					if '_Habil' in value:
						archivesVOCHabil.append(value)


		 	for GAS in listGAS:
		 		if GAS == pollutant: 
		 			#print GAS, pollutant
		 			if '_NHabil' in value:
		 				archivesGASNHabil.append(value)
		 			if '_Habil' in value:
		 				archivesGASHabil.append(value)


		 	for separed in listsepared: 
		 		if separed == pollutant: 
		 			if '_Habil' in value:
		 				archivesSeparedHabil.append(value)
		 			if '_NHabil' in value:
		 				archivesSeparedNHabil.append(value)


		listCH4 = []
		listBEN = []
		listPM10 = []
		listPM25 = []	
		for data in archivesSeparedHabil:
			if 'CH4' in data:
				listCH4.append(data)
			if 'BEN' in data:
				listBEN.append(data)
			if 'PM10' in data:
				listPM10.append(data)
			if 'PM2.5' in data:
				listPM25.append(data)


		writebrindingspeciation(listCH4, noun, 'CH4_Habil' , folder)	
		writebrindingspeciation(listBEN, noun, 'BEN_Habil' , folder)	
		writebrindingspeciation(listPM10, noun, 'PM10_Habil' , folder)	
		writebrindingspeciation(listPM25, noun, 'PM25_Habil' , folder)	

		listCH4 = []
		listBEN = []
		listPM10 = []
		listPM25 = []
		for data in archivesSeparedNHabil:
			if 'CH4' in data:
				listCH4.append(data)
			if 'BEN' in data:
				listBEN.append(data)
			if 'PM10' in data:
				listPM10.append(data)
			if 'PM2.5' in data:
				listPM25.append(data)

		writebrindingspeciation(listCH4, noun, 'CH4_NHabil' , folder)	
		writebrindingspeciation(listBEN, noun, 'BEN_NHabil' , folder)	
		writebrindingspeciation(listPM10, noun, 'PM10_NHabil' , folder)	
		writebrindingspeciation(listPM25, noun, 'PM25_NHabil' , folder)	
		

		writebrindingspeciation(archivesSpeciesHabil, noun, 'species_PM25_Habil', folder)
		writebrindingspeciation(achivesSpeciesNHabil, noun, 'species_PM25_NHabil', folder)
		
		writebrindingspeciation(archivesVOCHabil, noun, 'species_VOC_Habil', folder)			
		writebrindingspeciation(archivesVOCNHabil, noun, 'species_VOC_NHabil', folder)			

		writebrindingspeciation(archivesGASHabil, noun, 'CO2_CO_SO2_Habil', folder)	
		writebrindingspeciation(archivesGASNHabil, noun, 'CO2_CO_SO2_NHabil', folder)	

	if noun == 'wear':
		archivesSpeciesHabilTire = []
		archivesSpeciesHabilBrake = []
		achivesSpeciesNHabilTire = []
		achivesSpeciesNHabilBrake = []

		for value in listaspeciation: 
			index = 0
			for pos in value: 
				if pos == '_':
					end = index
					break
				index += 1
			
			pollutant =  value[:end]

			if pollutant[0] == 'P': 
				if '_Habil' in value and 'TIRE' in value:
					archivesSpeciesHabilTire.append(value)
				if '_Habil' in value and 'BRAKE' in value:
					archivesSpeciesHabilBrake.append(value)
				if '_NHabil' in value and 'TIRE' in value:
					achivesSpeciesNHabilTire.append(value)	
				if '_NHabil' in value and 'BRAKE' in value:
					achivesSpeciesNHabilBrake.append(value)	
			else: 
				print 'Not Found'

		folderBrake = os.path.join(folder, 'BRAKE', '')
		folderTire = os.path.join(folder, 'TIRE', '')

		writebrindingspeciation(archivesSpeciesHabilBrake, noun, 'species_PM25_Habil_BRAKE', folder)
		writebrindingspeciation(archivesSpeciesHabilTire, noun, 'species_PM25_Habil_TIRE', folder)
		
		writebrindingspeciation(achivesSpeciesNHabilBrake, noun, 'species_PM25_NHabil_BRAKE', folder)
		writebrindingspeciation(achivesSpeciesNHabilTire, noun, 'species_PM25_NHabil_TIRE', folder)

def writebrindingspeciation(listout, noun, identy, folder): 
	
	if noun == 'combustion':
		foldersave = os.path.join('..', 'out','speciation', 'brinding', 'combustion', '')
	elif noun == 'wear':
		if 'BRAKE' in identy:
			foldersave = os.path.join('..', 'out','speciation', 'brinding', 'wear', 'BRAKE', '')
		elif 'TIRE' in identy: 
			foldersave = os.path.join('..', 'out','speciation', 'brinding', 'wear', 'TIRE', '')


	csvsalida = open(foldersave + identy + '_SPC_Full.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['ROW', 'COL', 'LAT', 'LON', 'POLNAME', 'UNIT', 'E00h', 'E01h', 'E02h', 'E03h', 'E04h', 'E05h', 'E06h' ,'E07h', 'E08h', 'E09h', 'E10h', 'E11h', 'E12h', 'E13h', 'E14h', 'E15h', 'E16h', 'E17h', 'E18h', 'E19h', 'E20h', 'E21h', 'E22h', 'E23h', 'E24h'])
	
	folder = os.path.join(folder, '')
	
	for archiv in listout: 
		archive = folder + archiv
		matriz = convertCSVMatriz (archive)
		for i in range(1, matriz.shape[0]):
			salida.writerow(matriz[i,:])