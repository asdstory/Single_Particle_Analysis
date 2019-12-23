# Processing PnuC_3NR data_20190429, totally 1673 images

# Step01 - Import images (motion corrected by MotionCorr2) /Job045

Input files: 2019-04-29-PnuC-C8_Krios_patch-7-corrected-averages/*_sum_DW.mrc

Node type: 2D micrographs/tomograms(*.mrc)

# Step02 - CTF estimation /Job046

## I/O

Spherical aberration (mm): 2.7
Voltage (kV): 300 # Because this dataset was collected on Titan Krios, Building 13, under low mag (13kx)
Amplitude contrast: 0.1
Magnified pixel size (Angstrom): 1.08
Amount of astigmastism (A): 100

## Searches

Use as default

## CTFFIND-4.1

Use CTFFIND-4.1? Yes

# Step03 - Select /Job047

## I/O

OR select from micrographs.star: CtfFind/job046/micrographs_ctf.star

## Class options

Re-center the class averages? Yes

Regroup the particles? No

## Subsets 

Select based on metadata values? Yes

Metadata label for subset selction: rlnCtfMaxResolution

Minimum metadata value: -9999.

Maximum metadata value: 5.

## Duplicates

OR: remove duplicates? No



# Step04 - Particle Picking Manually /Joab049

## Display

Particle diameter (A): 150

Scale for micrographs: 0.25

Sigma contrast: 3

Lowpass filter (A): 20

Highpass filter (A): 0

Pixel size (A): 1.08



# Step05 - Extract Particles /Job098

## Extract

Particle box size (pix): 256

Invert contrast? Yes

Normalize particles? Yes

Diameter background circle (pix): 200

Rescale particles? Yes

Re-scaled size (Pixels): 64 


# Step06 - 2D classificaiton /Job099

# CTF

Do CTF-correction? Yes
Ignore CTFs until first peak? No

# Optimization

Number of classes: 50

Number of iterations: 25

Mask diameter (A): 150

# Step07 - Select /Job108

# Step08 - AutoPick /Job118

# Step09 - Extract /Job122

# Step10 - Class 2D /Job153

# Step11 - Select Particles /Job156

# Step12 - InitialModel /Job157

# Step13 - Class3D /Job163

# Step14 - Select /Job165

# Step15 - Extract Particles /Job166

# Step16 - Refine3D /Job167

# Step17 - MaskCreate /Job180

# Step18 - PostProcess /Job181

# Step19 - Polish


















