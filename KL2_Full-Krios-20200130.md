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

# Step02 - Motion correction

## I/O

Input movies STAR file: Import/job001/movies.star

First frame for corrected sum: 1

Last frame for corrected sum: 0

Dose per frame (e/A2): 1.43

Pre-exposure (e/A2): 0

Do dose-weighting? Yes

Save non-dose weighted as well? No

Save sum of power spectra? Yes

Sum power spectra every e/A2: 4

## Motion

Bfactor: 150

Number of particles X, Y: 5, 5

Group frames: 1

Binning factor: 2

Gain-reference image: No

Gain rotation: No

Gain flip: No

Use RELION's own implementation? Yes

## Running

Number of MPI procs: 100

Number of threads:2

Submit to queue? Yes

Queue name: multinode


# Step03 - CTF estimation

## I/O

Input micrographs STAR file: MotionCorr/job003/corrected_micrographs.star

Use micrograph without dose-weighting? No

Estimate phase shifts? No

Amount of astigmatism (A): 100

## CTFFIND-4.1

Use CTFFIND-4.1? Yes

## Running

Numberof MPI procs: 16




# Step04 - Particle Picking Manually

#In RELION Manual picking, Display Tab

particle diameter (A): 400

Pick star-end coordinates helices? Yes


# Step05 - Extract Particles

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

# Step06 - 2D classificaiton

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




