# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

from matriz import *
from wcsv import *
import json
import os
import csv


def listaCSV(direccion):
	path = os.path.join(direccion,'')

	#Lista vacia para incluir los ficheros
	lstFilesEmissions = []

	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(path) 

	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == '.csv'):
	        	lstFilesEmissions.append(nombreFichero+extension)

	return lstFilesEmissions

def binding(flows, links, noun):
	
	data = {}
	Mdata = convertXLSCSV(links)
	headData = Mdata[0,:] 
		
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
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

	Mdata = None
	MFlows = convertCSVMatriz(flows)
	headFlows = MFlows[0,:]

	index = 0
	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

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
	MFlows = None
	if noun == 'principal': 
		folder = os.path.join("..", 'data', 'in','link', 'PRINCIPAL','')
	elif noun == 'TM': 
		folder = os.path.join("..", 'data', 'in','link', 'TM','')
	#elif noun == 'HABIL' or noun == 'NOHAB': 
	#	folder = os.path.join("..", 'data', 'in', 'datalink', 'SECUNDARIAS','')
	
	writebinding(folder, data, noun)

def bindingsecondary(flows, links, typ):

	data = {}
	#print 'Start', typ
	Intermedia = 0.37
	Local = 0.22
	Activity = ['AUT_Gas', 'AUT_Gas', 'AUT_GNV', 'CC_Gas', 'CC_Dsel', 'CC_GNV', 'TX_Gas', 'TX_GNV', 'MB_Dsel', 'ESP_Gas', 'ESP_Dsel', 'ESP_GNV', 'M_Gas']
	ResidencialAct = 0.22
	NotActivity = [ 'B_Dsel', 'C2P_Dsel', 'C2P_Gas', 'C2P_GNV', 'BT_Dsel', 'AL_Dsel', 'AT_Dsel', 'BA_Dsel', 'INT_Dsel', 'INT_Gas','INT_GNV', 'C2G_Dsel', 'C2G_Gas', 'C2G_GNV', 'C3-C4_Dsel', 'C3-C4_Gas', 'C3-C4_GNV', 'c5_Dsel', 'c5_Gas', 'c5_GNV', '>c5_Dsel', '>c5_Gas', '>c5_GNV']
	ResidencialNotAct = 0

	Mdata = convertXLSCSV(links)
	headData = Mdata[0,:] 	
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
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

		for x in range(0, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	Mdata = None
	MFlows = convertCSVMatriz(flows)
	headFlows = MFlows[0,:]
	index = 0
	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = int(MFlows[y][colhour])

		FID = data.keys()

		for ID in FID:		
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				
				typo = MFlows[y][colType]
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]
				if typo == typ:
					for x in range(colhour+1, MFlows.shape[1]):
					 	headFlows = MFlows[0][x]
					 	if entryVehicle.get(headFlows) is None:
					 		entryVehicle[headFlows] = []
					 		entryVehicle[headFlows].append(MFlows[y][x])
		
	MFlows = None	
	FID = data.keys()
	for ID in FID:
		clasifi = data[ID]['link']['CLASIFI_SU'][0]
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

	folder = os.path.join('..', 'data', 'in', 'link', 'SECUNDARIAS', '')
	writeBindingSecondary(folder, data, "secundary", typ)

def bindingfinality(folderbrinding):
	
	folder2 = os.path.join('..', 'data', 'out', 'emissions', '')
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
	lstDir = os.walk(folderbrinding)
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

		matriz = None
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

		matriz = None
	csvsalida2.close()

def final(Archive):
	
	data = {}
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

	matriz = None
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
		hours = data[key]['hours'].keys()
		for hour in hours:
			csvsalida.write(',')
			csvsalida.write(str(data[key]['hours'][hour][0]))
		csvsalida.write('\n')
	csvsalida.close ()

def bindingspeciation(folder, noun): 
	#print folder
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

					if '_NHabil' in value:
						archivesVOCNHabil.append(value)
					if '_Habil' in value:
						archivesVOCHabil.append(value)


		 	for GAS in listGAS:
		 		if GAS == pollutant: 
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


		writebindingspeciation(listCH4, noun, 'CH4_Habil' , folder)	
		writebindingspeciation(listBEN, noun, 'BEN_Habil' , folder)	
		writebindingspeciation(listPM10, noun, 'PM10_Habil' , folder)	
		writebindingspeciation(listPM25, noun, 'PM25_Habil' , folder)	

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

		writebindingspeciation(listCH4, noun, 'CH4_NHabil' , folder)	
		writebindingspeciation(listBEN, noun, 'BEN_NHabil' , folder)	
		writebindingspeciation(listPM10, noun, 'PM10_NHabil' , folder)	
		writebindingspeciation(listPM25, noun, 'PM25_NHabil' , folder)	
		

		writebindingspeciation(archivesSpeciesHabil, noun, 'species_PM25_Habil', folder)
		writebindingspeciation(achivesSpeciesNHabil, noun, 'species_PM25_NHabil', folder)
		
		writebindingspeciation(archivesVOCHabil, noun, 'species_VOC_Habil', folder)			
		writebindingspeciation(archivesVOCNHabil, noun, 'species_VOC_NHabil', folder)			

		writebindingspeciation(archivesGASHabil, noun, 'CO2_CO_SO2_Habil', folder)	
		writebindingspeciation(archivesGASNHabil, noun, 'CO2_CO_SO2_NHabil', folder)	

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

		writebindingspeciation(archivesSpeciesHabilBrake, noun, 'species_PM25_Habil_BRAKE', folder)
		writebindingspeciation(archivesSpeciesHabilTire, noun, 'species_PM25_Habil_TIRE', folder)
		
		writebindingspeciation(achivesSpeciesNHabilBrake, noun, 'species_PM25_NHabil_BRAKE', folder)
		writebindingspeciation(achivesSpeciesNHabilTire, noun, 'species_PM25_NHabil_TIRE', folder)

def writebindingspeciation(listout, noun, identy, folder): 
	
	if noun == 'combustion':
		foldersave = os.path.join('..', 'data', 'out','speciation', 'binding', 'combustion', '')
	elif noun == 'wear':
		if 'BRAKE' in identy:
			foldersave = os.path.join('..', 'data', 'out','speciation', 'binding', 'wear', 'BRAKE', '')
		elif 'TIRE' in identy: 
			foldersave = os.path.join('..', 'data', 'out','speciation', 'binding', 'wear', 'TIRE', '')


	csvsalida = open(foldersave + identy + '_SPC_Full.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['ROW', 'COL', 'LAT', 'LON', 'POLNAME', 'UNIT', 'E00h', 'E01h', 'E02h', 'E03h', 'E04h', 'E05h', 'E06h' ,'E07h', 'E08h', 'E09h', 'E10h', 'E11h', 'E12h', 'E13h', 'E14h', 'E15h', 'E16h', 'E17h', 'E18h', 'E19h', 'E20h', 'E21h', 'E22h', 'E23h', 'E24h'])
	
	folder = os.path.join(folder, '')
	
	for archiv in listout: 
		archive = folder + archiv
		matriz = convertCSVMatriz (archive)
		for i in range(1, matriz.shape[0]):
			salida.writerow(matriz[i,:])

		matriz = None

def unions(archive1, archive2): 
	#print archive1
	Marchive1 = convertCSVMatriz(archive1)
	Marchive2 = convertCSVMatriz(archive2)
	
	name = Marchive1[0,:]
	index = 0
	for value in name: 
		if value == 'hora': 
			colIF = index+1
		index += 1
	name2 = Marchive2[0,colIF:]
	newname = []
	for noun in name: 
		newname.append(noun)

	for noun in name2: 
		newname.append(noun)

	name = None
	name2 = None

	folder = os.path.join('..', 'data', 'in','link', 'SECUNDARIAS', '')
	
	csvsalida = open(folder + 'secundaryBinding.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	salida.writerow(newname)
	
	for i in range(1, Marchive1.shape[0]):
		for x in range(0, Marchive1.shape[1]):
			if x == 0: 
				csvsalida.write(Marchive1[i][x])
			else: 
				csvsalida.write(',')
				csvsalida.write(Marchive1[i][x])
			
		
		for x in range(colIF, Marchive2.shape[1]):
				csvsalida.write(',')
				csvsalida.write(Marchive2[i][x])
					

		csvsalida.write('\n')

	Marchive1 = None
	Marchive2 = None