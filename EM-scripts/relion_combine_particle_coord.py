#!/usr/bin/env python     

#####*************************************************************************************#####
#Despcription: This program is used to combine RELION manual pick coord into Topaz coord file.
#Copyright@JiangLab@NHLBI/NIH
#Author: Tongyi Dou
#Last Edit: 2021-11-04
#####*************************************************************************************#####

DEBUG=0

import os
import re
import pandas as pd

directory=os.getcwd()
pat_image=re.compile(r"^(\S*)_manualpick.star")
pat_coord=re.compile(r"\s(\d*)\.\d*\s(\d*)")
data=[]

for filename in os.listdir(directory):
  result_image=pat_iamge.match(filename)
  group_image=result_image.groups()
  for (l=file(filename).readlines()):
    result_coord=pat_coord.match(l)
    if(result_coord):
      group_coord=result_coord.groups()
      data.append(group_iamge[1],int(group_coord[1]),int(group_coord[2]))

df=pd.DataFrame(data,columns=['image_name','x_coord','y_coord'])
df.to_csv('Particles.txt',index=False,sep='\t')
