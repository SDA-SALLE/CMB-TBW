#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python

#from emitionmovil import *
import os
import sys
sys.path.append('core')
from emitionmovil import *
from PMC import *
from clear import *

folderout = os.path.join ('..', 'out' ,'')
clear(folderout)

init()
categoryVechiclegrid()
categoryCarburantgrid()

print 'Star PMC'
folderconbustion = os.path.join('..','out','emissions', 'grid', 'combustion', '')
pmc(folderconbustion)
folderout = os.path.join('..', 'out','emissions', 'grid', 'PMC', 'Combustion', '')
testingpmc(folderout)
brindingpmc(folderout)

folderwear = os.path.join('..','out','emissions', 'grid', 'wear', '')
pmc(folderwear)
folderout = os.path.join('..', 'out','emissions', 'grid', 'PMC', 'Wear', '')
testingpmc(folderout)
brindingpmc(folderout)
print 'END PMC'