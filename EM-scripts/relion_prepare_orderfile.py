#!/usr/bin/env python     

#####**************************************************************************#####
#Despcription: This program is used to search and replace pattern in .star file.
#Author: Tongyi Dou
#How to use: Just "python replace.py --i run_data.star --o run_data_replace.star"
#Last Edit: 2021-07-02
#####**************************************************************************#####


import re
import numpy as np
from optparse import OptionParser

np.set_printoptions(threshold=np.inf)

parser = OptionParser()
parser.add_option("--input_tlt", dest="input_tlt", type="string", default="", help="Input .tlt file generated by IMOD [default: %default]")
parser.add_option("--input_mdoc", dest="input_mdoc", type="string", default="", help="Input .mdoc file generated by SeiralEM [default: %default]")
parser.add_option("--o", dest="output_order", type="string", default="", help="Output .order file used for RELION subtomogram averaging [default: %default]")

(options, args) = parser.parse_args()

def extract_refined_tilt_angle(file_tlt):
    file_tlt = open(file_tlt, 'r')
    refined_tilt_angle = list(file_tlt)
    return refined_tilt_angle
def extract_accumulated_dose(file_mdoc):
    accumulated_dose = []
    index = 0
    pattern = r'ExposureDose = (\d.\d{5})'
    for line in open(file_mdoc, 'r'):
        line = line.rstrip()
        result = re.search(pattern, line)
        if result and i == 0:
            accumulated_dose.append(result.group(1))
            index += 1
        elif result and i !=1:
            dose = accumulated_dose[index-1] + result.group(1)
            accumulated_dose.append(dose)
            index += 1
    return accumulated_dose
def write_order_file(file_order):
    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_order_handle = open(file_order, 'w')
    length = len(refined_tilt_angle)
    for i in range(length):
        line = refined_tilt[i] + " " + accumulated_dose[i]
        file_order_handle.write(file_i_string)
        file_order_handle.close()    
   
extract_refined_tilt_angle(options.input_tlt)
extract_accumulated_dose(options.input_mdoc)
write_order_file(options.output_order)

