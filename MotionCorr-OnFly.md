#Login to Titan computer:
#Just ssh and use your Biowulf password.

ssh -X dout2@micefdata1.niddk.nih.gov

#Go to your data folder (the folder you want to put the image data to)

#if there is an existing "config.txt" file, backup it and then delete it (do it on micefdata1 on K2 computer)

#run Screen command in this folder

screen

# In the screen window, run following shell script:

/home/jianglab/local/align_frames/run_on_micefdata1.sh

#do following to exit screen (detach from screen)

ctrl+a+d

#If you want to attach the screen (get back to the screen), type

screen -r

#If you have multiple screen and want to switch, try

ctr+a+n or ctr+a+p

#List all the screens you have

screen -ls


##Rerence 1 : How to use screen on linux

https://hostpresto.com/community/tutorials/how-to-use-screen-on-linux/

##Reference 2

#Email from Jiansen

Hi Bertram,
 
I have updated my scripts and installed them for all users on micefdata1. Could you please put the attached shell script to a folder that is in the default search path of all users, such as '/usr/local/bin', and make it executable.
 
Huaibin, after that script is installed, users just need to run "unattended_motioncor2.sh" to start the motioncor2 script. Ask users not to run the old copy of scripts that they installed in their folders as those are already obsolete. Also ask users not to use their previous config.txt files as some options have been changed.
 
This is new and simplified protocol:
1. login to micefdata1.niddk.nih.gov
2. go to the data folder (before copying data to the folder)
3. if there is an existing "config.txt" file, backup it and then delete it (do it on micefdata1 on K2 computer)
4. run "unattended_motioncor2.sh"; a new "config.txt" file will be created automatically
5. edit "config.txt" file by uncommenting the appropriate section near the end of file (do it on micefdata1 on K2 computer) 
6. start to transfer K2 movie files to the folder
7. terminate the script when image acquisition is done

Best regards,
Jiansen

# run_on_micefdata1.sh

#!/bin/bash
umask 022

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/jianglab/local/anaconda2/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/jianglab/local/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/home/jianglab/local/anaconda2/etc/profile.d/conda.sh"
    else
        export PATH="/home/jianglab/local/anaconda2/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
conda activate

/home/jianglab/local/align_frames/unattended_frame_align.py --gpu_nodes localhost:0,localhost:1 --config_template config_default_micef_krios.txt ./

# /home/jianglab/local/align_frames/unattended_frame_align.py

#!/usr/bin/env python

from ConfigParser import SafeConfigParser
from optparse import OptionParser
import re
import time
import threading
import random
import signal
import os
#from sys import argv
from os.path import isfile, isdir, join, getctime, exists, basename, dirname, abspath, realpath, getsize
from subprocess import call
from shlex import split
import json
from string import Template

DEBUG=False

parser = OptionParser()
parser.add_option("--incoming_folder", dest="incoming_folder", type="string", default="", help="Additional incoming folder for new frames [default: %default]")
parser.add_option("--scan_subfolder", dest="scan_subfolder", action="store_true", help="Process the subfolders where there is a config file [default: %default]")
parser.add_option("--gpu_nodes", dest="gpu_nodes", type="string", default="", help="Available GPUs. Format host1:gpu-id1,host1:gpu-id2,... e.g. localhost:0,localhost:1,... [default: %default]")
parser.add_option("--config_template", dest="config_template", type="string", default="", help="Template of config file [default: %default]")

(options, args) = parser.parse_args()

# Settings for this program. Change them accordingly if the computational enviroment is changed.
#frame_folder = '/datadisk/frames1/unattended_frame_alignment'
frame_folder = '.'

if len(args) > 0: frame_folder = args[0]

# specify graphics cards in the second input parameter:
# localhost:0,localhost:1,...
gpu_nodes = []
if len(args) > 1:
    for node in args[1].split(','):
        h = node.split(':')
        gpu_nodes.append([str(h[0]), int(h[1])])
elif options.gpu_nodes != '':
    for node in options.gpu_nodes.split(','):
        h = node.split(':')
        gpu_nodes.append([str(h[0]), int(h[1])])
else:
    # Each graphics card is defined.
    # [[ "server_name", gpu_id], ... ]
    gpu_nodes = [ \
                [ 'localhost', 0], \
                [ 'localhost', 1], \
                [ 'localhost', 2], \
                [ 'localhost', 3], \
                ]
