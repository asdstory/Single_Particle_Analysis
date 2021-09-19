#!/usr/struct/bin/python
# This script will go through all the individual tomogram directories
# get the subtomo/tomo/ctfsubtomo/coords and put them in a data.star file for a  combined relion run.
# By Tanmay Bharat, MRC-LMB 05.11.2013 

import os
import sys
import commands
import numpy as np

######## INPUT ###########################

# 2D star file
#starname2D = 'subtomo_proj2d_selected.star'
starname2D = sys.argv[1]

# Output star name
#starname3D = 'particles_subtomo.star'
starname3D = sys.argv[2]

######## INPUT ###########################


######## FUNCTIONS #######################

def read_relion_header(filename):

  print 'Reading the header of the relion star file'
  ifile = open(filename, 'r')

  # first get the header
  i=-1
  XextCol=0
  YextCol=0
  ZextCol=0
  XaliCol=0
  YaliCol=0
  ZaliCol=0
  RotCol=0
  TiltCol=0
  PsiCol=0
  AlignOrNot=0
  MaxLogValCol=0
  MicNameCol=0
  ImNameCol=0
  CtfImNameCol=0

  for line in ifile:
    if line.startswith("#"):
      continue
    emptycheck = line.isspace()
    if(emptycheck):
      continue

    fields = line.split()
    if fields[0] == 'data_' or fields[0] == 'loop_':
      continue

    i= i+1
 
    firstcol = fields[0]
 
    if firstcol == '_rlnCoordinateX':
      XextCol = i
    if firstcol == '_rlnCoordinateY':
      YextCol = i
    if firstcol == '_rlnCoordinateZ':
      ZextCol = i
    if firstcol == '_rlnOriginX':
      XaliCol = i
    if firstcol == '_rlnOriginY':
      YaliCol = i
    if firstcol == '_rlnOriginZ':
      ZaliCol = i
    if firstcol == '_rlnAngleRot':
      RotCol = i
    if firstcol == '_rlnAngleTilt':
      TiltCol = i
    if firstcol == '_rlnAnglePsi':
      PsiCol = i
    if firstcol == '_rlnMaxValueProbDistribution':
      MaxLogValCol = i
    if firstcol == '_rlnImageName':
      ImNameCol = i
    if firstcol == '_rlnCtfImage':
      CtfImNameCol = i
    if firstcol == '_rlnMicrographName':
      MicNameCol = i
 
    if firstcol[0] != '_':
      break
  
    if MaxLogValCol > 0:
      AlignOrNot = 1

  #print 'XextCol,YextCol,ZextCol,XaliCol,YaliCol,ZaliCol,RotCol,TiltCol,PsiCol,AlignOrNot,MaxLogValCol,ImNameCol,CtfImNameCol,MicNameCol'
  #print XextCol,YextCol,ZextCol,XaliCol,YaliCol,ZaliCol,RotCol,TiltCol,PsiCol,AlignOrNot,MaxLogValCol
  return(XextCol,YextCol,ZextCol,XaliCol,YaliCol,ZaliCol,RotCol,TiltCol,PsiCol,AlignOrNot,MaxLogValCol,ImNameCol,CtfImNameCol,MicNameCol)
      



######## FUNCTIONS #######################



######## RUNNING THE SCRIPT #################

# First read the 2D starfile
grepline = 'grep ' + 'Tomograms ' + starname2D + '| grep -v "#" | grep -v "loop" | grep -v "data" | awk "NF"  > temp.txt'
#print grepline
os.system(grepline)

infile=open('temp.txt')
data=infile.readlines()

# Getting the column Numbers
XextCol,YextCol,ZextCol,XaliCol,YaliCol,ZaliCol,RotCol,TiltCol,PsiCol,AlignOrNot,MaxLogValCol,ImNameCol,CtfImNameCol,MicNameCol = read_relion_header(starname2D)

TomogramNames2D = []
ImageNumbers2D = []

for i in range(0, len(data)):

  pair = data[i].split()
  
  # Tomogram Name 
  TomogramName = str(pair[MicNameCol])
  TomogramNames2D.append(TomogramName)

  # Image Name and numbers
  ImageName = str(pair[ImNameCol])
  imnamesplit = ImageName.split('@')
  ImageNumber = imnamesplit[0]
  ImageNumbers2D.append(ImageNumber)

del data
os.remove('temp.txt')

# Out star header
ofile = open('output_2Dto3D.star', 'w')
ofile.write('data_' + '\n' + '\n')
ofile.write('loop_' + '\n')
ofile.write('_rlnMicrographName #1' + '\n')
ofile.write('_rlnCoordinateX #2' + '\n')
ofile.write('_rlnCoordinateY #3'+ '\n')
ofile.write('_rlnCoordinateZ #4' + '\n')
ofile.write('_rlnImageName #5' + '\n')
ofile.write('_rlnCtfImage #6' +'\n')

# Now read the 3D starfile
grepline = 'grep ' + 'Tomograms ' + starname3D + '| grep -v "#" | grep -v "loop" | grep -v "data" | awk "NF"  > temp.txt'
#print grepline
os.system(grepline)

infile=open('temp.txt')
data=infile.readlines()

# Getting the column Numbers
XextCol,YextCol,ZextCol,XaliCol,YaliCol,ZaliCol,RotCol,TiltCol,PsiCol,AlignOrNot,MaxLogValCol,ImNameCol,CtfImNameCol,MicNameCol = read_relion_header(starname3D)

for i in range(0, len(data)):

  pair = data[i].split()
 
  # X,Y,Z
  X = float(pair[XextCol])
  Y = float(pair[YextCol])
  Z = float(pair[ZextCol])

  # Image and CTF image
  ImageName = str(pair[ImNameCol])
  imnamesplit = ImageName.split('.')
  ImageNumber = imnamesplit[0][-6:]
  #print ImageNumber

  CtfImage = str(pair[CtfImNameCol])
  TomogramName = str(pair[MicNameCol])

  for m in range(0, len(ImageNumbers2D)):

    if TomogramName == TomogramNames2D[m] and ImageNumber == ImageNumbers2D[m]:
      outline = TomogramName + '\t' + str("%.2f" % X) + '\t' + str("%.2f" % Y) + '\t' + str("%.2f" % Z) + '\t' + ImageName + '\t' + CtfImage + '\n' 
      ofile.write(outline)

ofile.close()
os.remove('temp.txt')
print "Selected subtomo STAR file written out"
sys.exit()
######
