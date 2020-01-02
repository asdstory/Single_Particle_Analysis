# MRC (file format)
From Wikipedia, the free encyclopedia https://en.wikipedia.org/wiki/MRC_(file_format)

Filename extension	.mrc

Type of format	3D electron density file or 2D image file

Website	http://www.ccpem.ac.uk/mrc_format/mrc2014.php

MRC is a file format that has become industry standard in cryo-electron microscopy (cryoEM) and electron tomography (ET), where the result of the technique is a three-dimensional grid of voxels each with a value corresponding to electron density or electric potential. It was developed by the MRC (Medical Research Council, UK) Laboratory of Molecular Biology.[1] In 2014, the format was standardised.[2] The format specification is available on the CCP-EM website.

The MRC format is supported by many of the software packages listed in b:Software Tools For Molecular Microscopy.

See also
CCP4 (file format)

# How to open and process MRC file

One of the common method is using mrcfile, a Python implementation of the MRC2014 file format, which is used in structural biology to store image and volume data.

Link: https://pypi.org/project/mrcfile/

It allows MRC files to be created and opened easily using a very simple API, which exposes the file’s header and data as numpy arrays. The code runs in Python 2 and 3 and is fully unit-tested.
This library aims to allow users and developers to read and write standard-compliant MRC files in Python as easily as possible, and with no dependencies on any compiled libraries except numpy. You can use it interactively to inspect files, correct headers and so on, or in scripts and larger software packages to provide basic MRC file I/O functions.

## Key Features

Clean, simple API for access to MRC files

Easy to install and use

Validation of files according to the MRC2014 format

Seamless support for gzip and bzip2 files

Memory-mapped file option for fast random access to very large files

Asynchronous opening option for background loading of multiple files

Runs in Python 2 & 3, on Linux, Mac OS X and Windows

# References
 Crowther, R.A.; Henderson, R.; Smith, J.M. (January 1996). "MRC Image Processing Programs". Journal of Structural Biology. 116 (1): 9–16. doi:10.1006/jsbi.1996.0003. PMID 8742717.
 
 Cheng, Anchi; Henderson, Richard; Mastronarde, David; Ludtke, Steven J.; Schoenmakers, Remco H.M.; Short, Judith; Marabini, Roberto; Dallakyan, Sargis; Agard, David; Winn, Martyn (November 2015). "MRC2014: Extensions to the MRC format header for electron cryo-microscopy and tomography". Journal of Structural Biology. 192 (2): 146–150. doi:10.1016/j.jsb.2015.04.002. PMC 4642651. PMID 25882513.

Burnley T, Palmer C & Winn M (2017) Recent developments in the CCP-EM software suite. Acta Cryst. D73:469–477. doi: 10.1107/S2059798317007859. https://pypi.org/project/mrcfile/

# External links
MRC specification
