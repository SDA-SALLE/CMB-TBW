# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons


#from emitionmovil import *
import os
import sys
sys.path.append('core')
from emitionmovil import *
from PMC import *
from clear import *

folderout = os.path.join ('..', 'out' ,'')
clear(folderout)

print 'empieza proceso'
convert()
FactorEmissions = os.path.join('..', 'data', 'FEmition', 'FactoresEmision.xlsx')
FactoresEmissionBrake = os.path.join('..', 'data', 'FEmition', 'FEBrake.xlsx')


principal = os.path.join('..', 'data', 'datalink', 'principalbrinding.csv')
calculation(principal, 'Principal', FactorEmissions, 'Habil')
calculation(principal, 'Principal', FactorEmissions, 'NHabil')
calculation(principal, 'Principal', FactoresEmissionBrake, 'Habil')
calculation(principal, 'Principal', FactoresEmissionBrake, 'NHabil')
print 'Calculo para Principales Habil y No Habil Listos'

TM = os.path.join('..', 'data', 'datalink', 'TMbrinding.csv')
calculation(TM, 'TM', FactorEmissions, 'Habil')
calculation(TM, 'TM', FactorEmissions, 'NHabil')
calculation(TM, 'TM', FactoresEmissionBrake, 'Habil')
calculation(TM, 'TM', FactoresEmissionBrake, 'NHabil')
print 'Calculo para Transmilenio Habil y No Habil Listos'


secundarias = os.path.join('..', 'data', 'datalink', 'secundarybrinding.csv')
calculation(secundarias, 'Secundary', FactorEmissions, 'Habil')
calculation(secundarias, 'Secundary', FactorEmissions, 'NHabil')
calculation(secundarias, 'Secundary', FactoresEmissionBrake, 'Habil')
calculation(secundarias, 'Secundary', FactoresEmissionBrake, 'NHabil')
print 'Calculo para Secundarias Habil y No Habil Listos'

folderdeparture = os.path.join('..', 'out', 'departure', '', '')
listFilesDeparture = list(folderdeparture)	

for File in listFilesDeparture:
	#index = 0
	#for letter in File:
		#if letter == '_':
			#possub1 = index
			#break
		#index += 1

	#index = 0
	#for letter in File:
		#if letter == '_':
			#possub2 = index
		#index += 1

	#noun = File[:possub1]
	#pollution = File[possub1+1:possub2]
	#Typo = File[possub2+1:-4]

	#archive = folderdeparture + File
	#data = createdata(archive, Typo)

	#categoryVechicle(data, noun, pollution, Typo)
	#categoryCarburant(data, noun, pollution, Typo)


foldercombustion = os.path.join('..', 'out', 'emissions', 'link', 'combustion', '')
listFilesEmissions = list(foldercombustion)

for File in listFilesEmissions:
	#finality(foldercombustion, File)

folderwear = os.path.join('..', 'out', 'emissions', 'link', 'wear', '')
listFilesEmissions = list(folderwear)

for File in listFilesEmissions:
	#finality(folderwear, File)

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
	#archive = foldercombustion + combustion
	##print archive
	#final(archive)

folderwearTIRE = os.path.join('..', 'out', 'speciation', 'brinding', 'wear', 'TIRE', '')
archiveswearTIRE = list(folderwearTIRE)

for wear in archiveswearTIRE:
	#archive = folderwearTIRE + wear
	#final(archive)

folderwearBRAKE = os.path.join('..', 'out', 'speciation', 'brinding', 'wear', 'BRAKE', '')
archiveswearBRAKE = list(folderwearBRAKE)

for wear in archiveswearBRAKE:
	#archive = folderwearBRAKE + wear
	#final(archive)

print 'brinding speciation OK'
print '*------------------------------------*'
print 'Archivo NoHabil Listo'
print 'End'

categoryVechiclegrid()
categoryCarburantgrid()

print 'Star PMC'
folderconbustion = os.path.join('..','out','emissions', 'grid', 'combustion', '')
pmc(folderconbustion)
folderout = os.path.join('..', 'out','emissions', 'grid', 'PMC', 'Combustion', '')
testingpmc(folderout)
brindingpmc(folderout)
listapmc = list(folderout)
for archive in listapmc:
	#archive = folderout + archive
	#final(archive)

folderwear = os.path.join('..','out','emissions', 'grid', 'wear', '')
pmc(folderwear)
folderout = os.path.join('..', 'out','emissions', 'grid', 'PMC', 'Wear', '')
testingpmc(folderout)
brindingpmc(folderout)
listapmc = list(folderout)
for archive in listapmc:
	#archive = folderout + archive
	#final(archive)
print 'END PMC'