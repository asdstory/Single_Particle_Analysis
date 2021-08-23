#!/usr/bin/env python     

#####***************************************************************************************************#####
#Despcription: This program is used to prepare the .order file for RELION subtomogram averaging.
#Author: Tongyi Dou
#How to use: "relion_prepare_orderfile.py --i run_data.star --o refined_particles_per_image.csv"
#Last Edit: 2021-08-22
#####***************************************************************************************************#####


import re
import numpy as np
from optparse import OptionParser

np.set_printoptions(threshold=np.inf)

parser = OptionParser()
parser.add_option("--i", dest="input_star", type="string", default="", help="Input .star file generated by RELION Refine3D or Class3D job [default: %default]")
parser.add_option("--o", dest="output_list", type="string", default="", help="Output .csv file with particles per image count [default: %default]")

(options, args) = parser.parse_args()

def count_particle_per_image(file_i,file_csv):
    dictionary = dict()
    pattern = r'(\d{8}_\d{8}.mrc\b)'
    for line in open(file_i, 'r'):
        line = line.rstrip()
        result = re.search(pattern, line)
        if result:
            image_name = result.group(1)
            if image_name in dictionary:
                dictionary[image_name] +=1
            else:
                dictionary.update({image_name:1})
    dictionary = sorted(dictionary[1].items(), key=lambda x:x[1], reverse=True)
    
    file_csv_handle = open(file_csv, 'w')
    for i in dictionary:
        print(dictionary.keys(i), '\t', dictionary.values(i), '\n')
        line = str(dictionary.keys(i)) + '\t' + str(dictionary.values(i)) + "\n"
        file_csv_handle.write(line)
    file_csv_handle.close()   
   
count_particle_per_image(options.input_star,options.output_list)

