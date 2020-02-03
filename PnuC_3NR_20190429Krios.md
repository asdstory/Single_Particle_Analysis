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

## I/O

Input images STAR file: Select/job156/particles.star

Reference map: 4QTN/4QTN15_box64.mrc

## Reference

Ref. map is on absolute greyscale? No

Initial low-pass filter (A): 50

Symmetry: C3

## CTF

Do CTF-correction? Yes

Has reference been CTF-corrected? Yes

## Optimisation

Number of classes: 4

Regularisation parameter T: 4

Number of iterations: 50

Mask diameter (A): 150



# Step14 - Select Model /Job165

## I/O

Select classes from model.star: 

## Class options

Re-center the class averages? Yes

# Step15 - Extract Particles /Job166

## I/O

micrograph STAR file: CtfFind/job489/micrographs_ctf.star

OR re-extract refined particles? Yes

Refined particles STAR file: Select/job165/particles.star

OR: re-center refined coordinates? Yes

Recenter on - X,Y,Z (pix): 0 0 0 

## Extract

Particle box size (pix): 256

Invert contrast? Yes

Normalize particles? Yes

Diameter background circle (pix): 200

Rescale particles? No


# Step16 - Refine3D /Job167

## I/O

Input images STAR file: Extract/job166/particles.star

Reference map: Class3D/job163/run_ct25_it050_class001_box256.mrc

## Reference

Ref. map is on absolute greyscale? No

Initial low-pass filter (A): 50

Symmetry: C3

## CTF

Do CTF-correction? Yes

## Optimisation

Mask diameter (A): 150

Mask individual particles with zeros? Yes

Use solvent-flattened FSCs? No

## Compute

Use GPUs


# Step17 - MaskCreate /Job180

## I/O

Input 3D map: Refine3D/job167/run_ct15_class001.mrc

## Mask

Lowpass filter map (A): 15

Initial binarisation threshold: 0.02

Extend binary map this many pixels: 20

Add a soft-edge of this many pixels: 20

## Running

using CPUs.

# Step18 - PostProcess /Job181

## I/O

One of the 2 unfiltered half-map: Refine3D/job167/run_ct15_half1_class001_unfil.mrc

Solvent mask: MaskCreate/job180/mask.mrc

Calibrated pixel size (A): 1.08

## Sharpen

Estimate B-factor automatically? Yes

## Running

Using CPUs.




# Step19 - Polish


















