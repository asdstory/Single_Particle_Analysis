Processing the dataset of CBFSMMHC_20200103TF20-Fulllength_50mM, 310 images.

# Step01 - Import images (motion corrected by MotionCorr2)

Input files: corrected-averages/*_sum_DW.mrc

Node type: 2D micrographs/tomograms(*.mrc)

# Step02 - CTF estimation

## I/O

Spherical aberration (mm): 1.2 #this dataset was collected on TF20, Building 8, under low mag (29kx)

Voltage (kV): 200

Amplitude contrast: 0.1

Magnified pixel size (Angstrom): 1.26

Amount of astigmastism (A): 100

## Searches

Use as default

## CTFFIND-4.1

Use CTFFIND-4.1? Yes

## Running

Number of MPI procs: 9


# Step03 - Particle Picking Manually

## In RELION Manual picking, Display Tab

particle diameter (A): 400

Pick star-end coordinates helices? Yes


# Step04 - Extract Particles

## Extract

Particle box size (pix): 600

Rescale particles? Yes

Re-scaled size (pixels): 150

## Helix

Extract helical segments? Yes

Tube diameter (A): 400

Use bimodal angular priors? Yes

Coordinates are start-end only? Yes

Cut helical tubes into segments? Yes

Number of asymmetrical units: 1

Helical rise (A): 100

# Step05 - 2D classificaiton

## CTF

Do CTF-correction? Yes

Ignore CTFs until first peak? Yes

## Optimization

Number of classes: 50

Mask diameter (A): 400

## Helix

Classify 2D helical segments? Yes

Tube diameter (A): 400

Do bimodal angular searches? Yes

Angular search range - psi (deg): 6

## Compute

Use GPU acceleration? Yes


#2D classification results showed good alignment.

# Further optimization - 1 Optimize ...
