# Example - Processing CBFSMMHC_20191105TF20,the truncated version of filament from Tao Zhen, totally 273 images

# Step01 - Import images (motion corrected by MotionCorr2)

Input files: 2019-11-05-TYD-CBFSMMHC-tr-corrected-averages/*_sum_DW.mrc

Node type: 2D micrographs/tomograms(*.mrc)

# Step02 - CTF estimation

#I/O

Spherical aberration (mm): 1.2 #this dataset was collected on TF20, Building 8, under low mag (29kx)

Voltage (kV): 200

Amplitude contrast: 0.1

Magnified pixel size (Angstrom): 1.26

Amount of astigmastism (A): 100

#Searches

Use as default

#CTFFIND-4.1

Use CTFFIND-4.1? Yes

# Step03 - Particle Picking Manually

#In RELION Manual picking, Display

Pick star-end coordinates helices? Yes

# Step04 - ?

Input files: 2019-11-23-TYD-PnuC_3NR-corrected-averages/*_automatch.star

Node type: 2D/3D particle coordinates (*.box, *_pick.star)

#You can view the auto-picking results directly after import particles, by display "coords_suffix_automatch.star".
#However, to view the particles, you have to set Manual picking parameters first:


#Optimization

Change diameters for GAutomach autopicking, and check on raw images if particles we want are picked.
For this case, try 70, 80, 90, 100. 

# Step05 - Extract Particles

#Extract

Particle box size (pix): 200


# Step06 - 2D classificaiton

# CTF

Do CTF-correction? Yes
Ignore CTFs until first peak? Yes

# Optimization

Number of classes: 100

Mask diameter (A): 160

#2D classification results showed good alignment.

# Further optimization - 1 Optimize the box size and Mask diameter
#I changed the Mask diameter to 170, redo the Particle extraction and 2D classification, see if this will make 2D alignment results much better.

#Try 1: 
Particle box size (pix): 1200
Mask diameter (A): 170

#Results: 
1. Particles aligned much better than before, best class has 6% distribution.

#Try 2: 
Particle box size (pix): 170
Mask diameter (A): 150


# Further optimization - 2 Select good particles/classes from last 2D classification, and redo 2D classification.


# Further optimization - 3 Select some templates from last 2D classification, and do template-based particle picking again, using RELION-Autopick.


