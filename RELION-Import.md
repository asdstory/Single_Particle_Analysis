# Function and Application:
#This step is to import the data for processing, either raw image or processed ones, e.g. particles picked by Gautomatch.

# Algorithm and Principle:
#What is the mrc file?

https://www.ccpem.ac.uk/mrc_format/mrc2014.php

# Materials and Methods:



## Start Relion on Biowulf

#Import mrc files after motioncorr (the *sum_DW.mrc file)

Input file: *_sum_DW.mrc
Node type: 2D micrographs/tomograms

#Import particles picked by GAutomatch

Input file: *_automatch.star
Node type: 2D/3D particle coordinates

# Results and Interpretation:
#You can view the imported data by view/Display?


