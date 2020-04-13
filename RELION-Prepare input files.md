# High level flowchart of RELION. 

![](https://github.com/asdstory/Single-particle-cryo-EM-data-processing/blob/master/Fig%201%20High%20level%20flowchart%20of%20RELION.jpeg)

*Figure from Kimanius et al. eLife 2016;5:e18722. DOI: 10.7554/eLife.18722

# Prepare input files

Following information is from: https://www3.mrc-lmb.cam.ac.uk/relion/index.php/Prepare_input_files

# Recommended image preprocessing
The procedures outlined below are suited if you have already done your preprocessing in another program package and you want to use the stack(s) of particles created by that package. If you are starting fresh from a set of raw frames, you may find the new (as of release-1.1) preprocess run-type inside the RELION GUI more convenient.

## General comments on data quality
RELION will work best if your input images are:

Even-sized (Odd dimensions are not implemented)
Square i.e. xdim=ydim
Clean from false particles (note that RELION does NOT discard any images during refinement).
Unmasked (masking is performed internally)
Non-interpolated (prevent any prior rotations/translations: use the originally scanned pixel values)
If downscaling is necessary because of memory issues: use a window-operation in Fourier-space, not a convolution in real-space (e.g. with a rectangle/B-spline).
Uncorrected for CTF (this is done internally)
If your data have previously been phase-flipped, that's OK: just tell RELION about it
Actually, if you are not planning to correct for CTFs inside RELION (e.g. for negative stain data), phase-flipping is recommended.
If your data have previously been pre-Wiener filtered or pre-multiplied by their CTF, that's a bad thing to do: go back to the original data.
Normalised Make sure the average density in the background area is (approximately) zero!!. Also, the standard deviation in the noise should be (approximately) one.
## Negative stain data
The use of CTF phase-flipped particles without further CTF correction inside RELION is the recommended procedure for negative stain data:

Get a MRC/SPIDER/IMAGIC stack of your clean, unfiltered, unmasked and phase-flipped particles. Often direct extraction from phase-flipped micrographs is the easiest and best option. Alternatively, extract the particles from the raw micrographs and perform phase-flipping on the extracted particles. Use your favourite package to do this, e.g. EMAN(2), XMIPP, IMAGIC, SPIDER, etc.
Input this stack into the relion_preprocess command-line program (available from version 1.1 onwards) to re-scale and re-window your original particles to even-size (if necessary) and to normalize them. The output MRC stack (or STAR file) can be directly used as input for RELION refinement.
## cryo-EM data
For cryo-EM data, full CTF-correction (including amplitudes and phases) inside RELION is highly recommended. Therefore, the recommended procedure involves telling RELION about the CTF parameters of each particle:

Get one or multiple MRC/SPIDER/IMAGIC stack(s) of your clean, unfiltered, unmasked and non-CTF-corrected (only phase-flipping is also OK). Often direct extraction from the raw micrographs is the easiest and best option.
Create a STAR file that contains the necessary CTF parameters (rlnDefocusU, rlnDefocusV, rlnDefocusAngle, rlnVoltage, rlnSphericalAberration, rlnAmplitudeContrast and rlnMicrographName) for all particles. The next section explains how to do this.
Input this STAR file into the relion_preprocess command-line program (available from version 1.1 onwards) to re-scale and re-window your original particles to even-size (if necessary) and to normalize them. The output STAR file can be directly used as input for RELION refinement.
## Dividing your data into groups
For refinement inside RELION you may divide your data into groups, so that a different noise spectrum and signal scale factor is estimated for each group independently. This is typically not necessary for refinements with negative stain data, but highly recommended when using cryo-EM data. Usually, each micrograph comprises one group. Therefore, the division into groups is based on the rlnMicrographName column in the input STAR file. However, to get robust noise and signal estimates, make sure each group contains at least ~10-20 particles. If you have very few particles per micrograph, then you may want to combine multiple micrographs into one group (i.e. use the same rlnMicrographName for particles coming from multiple micrographs). If you do so, make sure you join micrographs with similar apparent signal-to-noise ratios. Often this means with similar defocus values, but do note that each particle may still have its own defocus values (CTF corrections are done per-particle, not per group).

# Creating input STAR files
The STAR file format is explained on the Conventions page. STAR files are easily readable plain text files, for which shell utilities like awk are very convenient. However, because not all users will be equally proficient in shell scripting, RELION comprises several shell script implementations to provide some basic operations with STAR files. See the STAR file utilities page for a description of these utilities, of which relion_star_loopheader, relion_star_datablock_stack and relion_star_datablock_singlefiles are used below.

## Generate STAR files from separate stacks for each micrograph
If the input images are in a separate stack for each micrograph, then one could use the following commands to generate the input STAR file:


relion_star_loopheader rlnImageName rlnMicrographName rlnDefocusU rlnDefocusV rlnDefocusAngle rlnVoltage rlnSphericalAberration rlnAmplitudeContrast > my_images.star
relion_star_datablock_stack 4 mic1.mrcs mic1.mrcs 10000 10500 30 200 2 0.1  >> my_images.star
relion_star_datablock_stack 3 mic2.mrcs mic2.mrcs 21000 20500 25 200 2 0.1  >> my_images.star
relion_star_datablock_stack 2 mic3.mrcs mic3.mrcs 16000 15000 35 200 2 0.1  >> my_images.star

(Where the three stacks contain respectively 4, 3 and 2 images.) This would result in this STAR file that could be used directly as input into RELION. Note the rlnMicrographName label, and the repetition of the micrograph names on the datablock lines, which will lead to the inclusion of a unique rlnMicrographName for each micrograph. By doing so, distinct noise spectra will be estimated for each micrograph.

## Generate STAR files from particles in single-file format
If the input images are in single-file format in distinct directories for each micrograph, then the commands would be:

relion_star_loopheader rlnImageName rlnMicrographName rlnDefocusU rlnDefocusV rlnDefocusAngle rlnVoltage rlnSphericalAberration rlnAmplitudeContrast > my_images.star
relion_star_datablock_singlefiles "mic1/*.spi" mic1 16000 15000 35 200 2 0.1  >> my_images.star
relion_star_datablock_singlefiles "mic2/*.spi" mic2 16000 15000 35 200 2 0.1  >> my_images.star
relion_star_datablock_singlefiles "mic3/*.spi" mic3 16000 15000 35 200 2 0.1  >> my_images.star

And the result would be this equivalent STAR file.

## Generate STAR files from XMIPP-style CTFDAT files
To generate a STAR file from an XMIPP-style ctfdat file, one could use:

relion_star_loopheader rlnImageName rlnMicrographName rlnDefocusU rlnDefocusV rlnDefocusAngle rlnVoltage rlnSphericalAberration rlnAmplitudeContrast > all_images.star
relion_star_datablock_ctfdat all_images.ctfdat>>  all_images.star
Generate STAR files from FREALIGN-style .par files
To generate a STAR file from a FREALIGN-style .par file, one could use:

relion_star_loopheader rlnImageName rlnMicrographName rlnDefocusU rlnDefocusV rlnDefocusAngle rlnVoltage rlnSphericalAberration rlnAmplitudeContrast > all_images.star
awk '{if ($1!="C") {print $1"@./my/abs/path/bigstack.mrcs", $8, $9, $10, $11, " 80 2.0 0.1"}  }' < frealign.par >> all_images.star
Assuming the voltage is 80kV, the spherical aberration is 2.0 and the amplitude contrast is 0.1. Also, a single stack is assumed called: /my/abs/path/bigstack.mrcs.

# Preparing references
2D class averaging is typically performed in an unsupervised manner, i.e. without user-provided references. 3D classification or refinement does require a (single) 3D reference structure. This map should be provided in MRC or SPIDER format, and it should have the same dimensions as the input images. Take care that the pixel size (in Angstroms) matches that of the experimental images, as currently an internal magnification correction is not implemented. Because the Gaussian model used to calculate probabilities is based on the squared differences between the experimental images and projections of the reference, the absolute intensity scale (or grey-scale) of the reference map is relevant. However, RELION may correct for the greyscale internally at relatively small computational costs (just set the Ref. map is on absolute greyscale? option in the GUI to No.)

To limit model bias it is generally recommended to strongly low-pass filter your initial reference. The Optimisation tab in the GUI has an entry to set an initial low-pass filter.

## Important note for 3D classification
Although for 3D classification an external reference may work OK (as illustrated in the fully guided 3D classification example), one often gets better results by starting classification from a consensus model that was generated from the structurally heterogeneous data set itself. To that purpose, one may refine (for multiple iterations) the external reference (as a single class) against the entire data set. The resulting model may then be used to generate (low-pass filtered!) random seeds and classify the data using multiple classes.

Note that the option Ref. map is on absolute greyscale? in the GUI should then probably be set to No for the initial single-reference refinement, and then to Yes for the actual classification run.
