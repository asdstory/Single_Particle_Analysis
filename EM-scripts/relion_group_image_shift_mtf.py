#!/usr/bin/env python     

#####**************************************************************************#####
#Despcription: This program is used to introduce optic group into movies.star file.
#Copyright@JiangLab@NHLBI/NIH
#Author: Jiansen Jiang & Tongyi Dou
#Last Edit: 2021-07-02
#####**************************************************************************#####

DEBUG=0

import os
import re
import time
import numpy as np
import matplotlib 
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import cluster
from datetime import datetime
from optparse import OptionParser

np.set_printoptions(threshold=np.inf)

parser = OptionParser()
parser.add_option("--clusters", dest="n_clusters", type="int", default=16, help="Number of image shift clusters [default: %default]")
parser.add_option("--image_shift_data", dest="image_shift_data_file", type="string", default="", help="Image shift data file (SQL query from Leginon database) [default: %default]")
parser.add_option("--input_star", dest="input_star", type="string", default="", help="Input movies.star file generated by RELION Import job [default: %default]")
parser.add_option("--output_star", dest="output_star", type="string", default="", help="Output movies.star file [default: %default]")
parser.add_option("--output_plot", dest="output_plot", type="string", default="image_shift.pdf", help="Output pdf file [default: %default]")

(options, args) = parser.parse_args()


def read_image_shift(fn):
    try:
        l = file(fn).readlines()
    except:
        print "Can't read image shift data file " + fn + "."
        exit(1)

    if len(l) < 2:
        print "There are no data in the image shift file"
        exit(1)

    # Assuming the columns are separated by Tab. Fix this if other sparators are used.
    # Typical header: 'unix_timestamp  timestamp       name    filename        image_shift_x   image_shift_y'
    header = l[0].strip().split('\t')
    image_shift_data = []
    for i in range(1, len(l)):
        d = l[i].strip().split('\t')
        t = {}
        for j in range(len(header)):
            if header[j] == 'unix_timestamp':
                t[header[j]] = int(d[j])
#                t['adjusted_timestamp'] = int(d[j])
            elif header[j][:11] == 'image_shift': t[header[j]] = float(d[j]) * 1000000.
            else: t[header[j]] = d[j]
        if t['filename'][-2:] == 'en':
            t['grid'] = "_".join(t['filename'].split('_')[:-6])
            image_shift_data.append(t)
    image_shift_data.sort(key = lambda x : x['unix_timestamp'])
    return image_shift_data

def read_image_list(fn):
    try:
        l = file(fn).readlines()
    except:
        print "Can't read image list file " + fn + "."
        exit(1)
    image_list = []
    for i in range(len(l)):
        pat = re.compile(r"(\w.+|-.+|\/.+)(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{2}).([a-z].+)")
        #"20151201_15090200"
        result = pat.match(l[i])
        if result:
            tmp = result.groups()
            timestamp = int(time.mktime((int(tmp[1]), int(tmp[2]), int(tmp[3]),  int(tmp[4]), int(tmp[5]), int(tmp[6]), 0, 0, -1)))
            image_list.append({'unix_timestamp' : timestamp, 'filename' : os.path.basename(l[i].strip()).split('.')[0], 'grid' : "", 'image_shift_x' : 0., 'image_shift_y' : 0., 'time_error' : 0, 'class' : 0})
    image_list.sort(key = lambda x : x['unix_timestamp'])
    return image_list

def read_image_full_name(fn):
    try:
        l = file(fn).readlines()
    except:
        print "Can't read image list file " + fn + "."
        exit(1)
    tmp = []
    for i in range(len(l)):
        pat = re.compile(r"(\w.+|-.+|\/.+)(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})(\d{2}).([a-z]+)")
        #"20151201_15090200"
        result = pat.match(l[i])
        if result:
            tmp = result.groups()
            print "Image full name with address is like:" + str(tmp) + "\n"
            break
    return tmp

def read_optical_parameter(fn):
    try:
        l = file(fn).readlines()
    except:
        print "Can't read image list file " + fn + "."
        exit(1)
    tmp = []
    for i in range(len(l)):
        #pat = re.compile(r"(\w+)\s+(\d*\.?\d*)\s+(\d*\.?\d*)\s+(\d*\.?\d*)\s+(\d*\.?\d*)")
        pat = re.compile(r"(\w+)\s+(\d*\.?\d*)\s+((?:[A-Z]:|\\|(?:\.{1,2}[\/\\])+)[\w+\\\s_\(\)\/]+(?:\.\w+)*)\s+(\d*\.?\d*)\s+(\d*\.?\d*)\s+(\d*\.?\d*)\s+(\d*\.?\d*)")
        #"opticsGroup1            1     0.850000   300.000000     2.700000     0.100000"
        #"opticsGroup1            1 ../Database/MTF_curves/mtf_k3_CDS_300kv_from_gatan.star     0.415000   300.000000     2.700000     0.100000"
        result = pat.match(l[i])
        if result:
            tmp = result.groups()
            print "Input optical parameters are:" + str(tmp) + "\n"
            break
    return tmp

def correlate_timestamp(ts1, ts2):
    if ts1[0] > ts2[0]: d_start = ts1[0]
    else: d_start = ts2[0]
    if ts1[-1] < ts2[-1]: d_end = ts1[-1]
    else: d_end = ts2[-1]
    d_start -= 10
    d_end += 10
    if (d_end - d_start) % 2 == 1: d_end += 1

    if d_end < d_start: return -99999

    d1 = np.zeros(d_end - d_start)
    d2 = np.zeros(d_end - d_start)

    for i in ts1:
        # Fill with a small distribution
        k = i - d_start
        if k > 2 and k < len(d1) - 2:
            d1[k-2] = 0.1
            d1[k-1] = 0.5
            d1[k] = 1.0
            d1[k+1] = 0.5
            d1[k+2] = 0.1
    for i in ts2:
        # Fill with a small distribution
        k = i - d_start
        if k > 5 and k < len(d2) - 5:
            d2[k-5] = 0.1
            d2[k-4] = 0.3
            d2[k-3] = 0.6
            d2[k-2] = 0.8
            d2[k-1] = 0.9
            d2[k] = 1.0
            d2[k+1] = 0.9
            d2[k+2] = 0.8
            d2[k+3] = 0.6
            d2[k+4] = 0.3
            d2[k+5] = 0.1

#    print "Length of time", len(d1), len(d2)
    cc = np.correlate(d1, d2, "same")
    pp = np.argmax(cc)
    return(len(d1) / 2 - pp)

def find_image_shift(imgs, shifts):
# Look up correct image shift values
    shifts_map = []
    p = 0
    for i in imgs:
        t = i['unix_timestamp']
        while p + 1 < len(shifts):
            e0 = abs(t - shifts[p]['unix_timestamp'])
            e1 = abs(t - shifts[p + 1]['unix_timestamp'])
            if e0 < e1:
                break
            p += 1
        t_err = t - shifts[p]['unix_timestamp']
        im = i.copy()
        im['image_shift_x'] = shifts[p]['image_shift_x']
        im['image_shift_y'] = shifts[p]['image_shift_y']
        im['time_error'] = abs(shifts[p]['unix_timestamp'] - t)
        im['grid'] = shifts[p]['grid']
        shifts_map.append(im)
    return shifts_map

def get_grid_list(shifts):
    t = []
    for i in shifts:
        if (i['grid'] not in t) and (len(i['grid']) > 0): t.append(i['grid'])
    return t

def filter_by_grid(shifts, grid):
    t = []
    for i in shifts:
        if i['grid'] == grid: t.append(i)
    return t

def slice_by_unix_timestamp(shifts, start, end):
    p0 = 0
    p1 = len(shifts) - 1
    for i in range(len(shifts)):
        p0 = i
        if shifts[i]['unix_timestamp'] > start:
            break
    for i in range(len(shifts) - 1, -1, -1):
        p1 = i
        if shifts[i]['unix_timestamp'] < end:
            break
    return  shifts[p0:p1]

def get_adjusted_image_shift_timestamp(imgs, shifts):
    grids = get_grid_list(shifts)

    t = []
    for i in grids:
#        print "Align images in grid: %s" % (i)
        shifts_grid = filter_by_grid(shifts, i)
        img_list = slice_by_unix_timestamp(imgs, shifts_grid[0]['unix_timestamp'] - 3600, shifts_grid[-1]['unix_timestamp'] + 3600)
        if len(img_list) > 0:
            ts1 = [x['unix_timestamp'] for x in img_list]
            ts2 = [x['unix_timestamp'] for x in shifts_grid]
            dt = correlate_timestamp(ts1, ts2)
            print "Grid %s. %d images. Time difference between saved images and Leginon records: %d seconds." % (i, len(img_list), dt)
            if dt > -99999:
                for j in shifts_grid:
                    a = j.copy()
                    a['unix_timestamp'] -= dt
                    t.append(a)
    t.sort(key = lambda x : x['unix_timestamp'])
    return t

print "Read image shift data ... ",
image_shift_data = read_image_shift(options.image_shift_data_file)
print "Done. %i images were read." % (len(image_shift_data))
print "First image was recorded at:\t %s" % (datetime.fromtimestamp(image_shift_data[0]['unix_timestamp']))
print "Last image was recorded at:\t %s" % (datetime.fromtimestamp(image_shift_data[-1]['unix_timestamp']))

print "Read image list ... ",
image_list = read_image_list(options.input_star)
print "Done. %i images were read." % (len(image_list))
print "First image was recorded at:\t %s" % (datetime.fromtimestamp(image_list[0]['unix_timestamp']))
print "Last image was recorded at:\t %s" % (datetime.fromtimestamp(image_list[-1]['unix_timestamp']))

image_shift_adjusted_time = get_adjusted_image_shift_timestamp(image_list, image_shift_data)
image_list = find_image_shift(image_list, image_shift_adjusted_time)
time_errors = np.array([i['time_error'] for i in image_list])
print "%d images were matched. Time error (seconds): mean %f std %f" % (len(time_errors), time_errors.mean(), time_errors.std())


if DEBUG:
    for i in range(len(image_list)):
        print "Timestamp: %s\tGrid: %s\tTime error: %d\tImage shift x: %f\ty: %f" % (image_list[i]['unix_timestamp'], image_list[i]['grid'], image_list[i]['time_error'], image_list[i]['image_shift_x'], image_list[i]['image_shift_y'])

grids = get_grid_list(image_list)
cn = 0
for g in grids:
    imgs = filter_by_grid(image_list, g)
    xyd = np.array([[i['image_shift_x'], i['image_shift_y']] for i in imgs])
    clustering = cluster.KMeans(n_clusters=options.n_clusters).fit(xyd)
    cls = clustering.labels_
    for i in range(len(imgs)):
        imgs[i]['class'] = cls[i] + cn
    cn = cn + max(cls) + 1
    print "Grid \'%s\': %d images, %d classes" % (g, len(imgs), max(cls) + 1)

    plt.figure()
    xyd = np.array([[i['image_shift_x'], i['image_shift_y'], i['class']] for i in imgs])
    r1 = [min(xyd[:, 0]), min(xyd[:, 1]), max(xyd[:, 0]), max(xyd[:, 1])]
    plt.xlim(min(r1), max(r1))
    plt.ylim(min(r1), max(r1))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.scatter(xyd[:, 0], xyd[:, 1], c=xyd[:, 2], s=4)
    #plt.show()
    plt.draw()
    plt.savefig(options.output_plot[:-4] + g + '.pdf', format='pdf')


print "Total images: %d, Beam tilt classes: %d" % (len(image_list), cn)

plt.figure
xyd = np.array([[i['image_shift_x'], i['image_shift_y'], i['class']] for i in image_list])
r1 = [min(xyd[:, 0]), min(xyd[:, 1]), max(xyd[:, 0]), max(xyd[:, 1])]
plt.xlim(min(r1), max(r1))
plt.ylim(min(r1), max(r1))
plt.gca().set_aspect('equal', adjustable='box')
plt.scatter(xyd[:, 0], xyd[:, 1], c=xyd[:, 2], s=4)
#plt.show()
plt.draw()
plt.savefig(options.output_plot, format='pdf')

shift_class_dict = {}
for i in image_list:
    shift_class_dict[i['filename']] = i['class']
#print shift_class_dict
"""
shift_class_dict = {
  "20210127_17415700": "1",
  "20210127_17422501": "2",
  "20210127_17423902": "3",
  "20210127_17425303": "4",
  "20210127_17430704": "5"
}
"""
#d = open("dictionary.txt","w")
#d.write(shift_class_dict)
#d.close()

f = open(options.output_star,"w")
f.write("\n")
f.write("# version 30001"+"\n")
f.write("\n")
f.write("data_optics"+"\n")
f.write("\n")
f.write("loop_"+"\n")
f.write("_rlnOpticsGroupName #1"+"\n")
f.write("_rlnOpticsGroup #2"+"\n")
f.write("_rlnMtfFileName #3"+"\n")
f.write("_rlnMicrographOriginalPixelSize #4"+"\n")
f.write("_rlnVoltage #5"+"\n")
f.write("_rlnSphericalAberration #6"+"\n")
f.write("_rlnAmplitudeContrast #7"+"\n")

Optical_parameter = read_optical_parameter((options.input_star))

for i in range(cn):
    line = "opticsGroup" + str(i+1) + "            " + str(i+1) +"     "+str(Optical_parameter[2])+"   "+str(Optical_parameter[3])+"     "+str(Optical_parameter[4])+"     "+str(Optical_parameter[5])+"     "+str(Optical_parameter[6])+"\n"
    f.write(line)
f.write("\n")
f.write("\n")
f.write("# version 30001"+"\n")
f.write("data_movies"+"\n")
f.write("loop_"+"\n")
f.write("_rlnMicrographMovieName #1"+"\n")
f.write("_rlnOpticsGroup #2"+"\n")

Image_name = read_image_full_name((options.input_star))

for x in sorted(shift_class_dict.keys()):
    line = str(Image_name[0])+str(x)+"."+str(Image_name[8])+"            "+str(shift_class_dict[x]+1)+"\n"
    f.write(line)
f.close()
