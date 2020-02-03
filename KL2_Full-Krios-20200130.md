# Example - Processing KL2_Fulllength-20200130Krios data,the fulllength version of filament from Tao Zhen, totally 7910 images

# Step01 - Import 

## Movies/mics

Import raw movies/micrographs? Yes

Raw input files: Micrographs/*.tif

Are these multi-frame movies? Yes

Optics group name: opticsGroup1

MTF of the detector: ../Gain-reference/mtf_k2_300kv_FL2.star

Pixel size (Angstrom): 1.058

Voltage (kV): 300

Spherical aberration (mm): 2.7

Amplitude contrast: 0.1

Beamtilt in X (mrad): 0

Beamtilt in Y (mrad): 0

## Other

Import other node types? No

## Running

Just click "Run!"




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

#In RELION Manual picking, Display Tab

particle diameter (A): 400

Pick star-end coordinates helices? Yes


# Step04 - Extract Particles

#Extract

Particle box size (pix): 600

Rescale particles? Yes

Re-scaled size (pixels): 150

#Helix

Extract helical segments? Yes

Tube diameter (A): 400

Use bimodal angular priors? Yes

Coordinates are start-end only? Yes

Cut helical tubes into segments? Yes

Number of asymmetrical units: 1

Helical rise (A): 100

# Step05 - 2D classificaiton

#CTF

Do CTF-correction? Yes

Ignore CTFs until first peak? Yes

#Optimization

Number of classes: 50

Mask diameter (A): 400

#Helix

Classify 2D helical segments? Yes

Tube diameter (A): 400

Do bimodal angular searches? Yes

Angular search range - psi (deg): 6

#Compute

Use GPU acceleration? Yes


#2D classification results showed good alignment.

# Further optimization - 1 Optimize ...




