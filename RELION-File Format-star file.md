RELION-File Format-star file.md

#Following information are from: https://www3.mrc-lmb.cam.ac.uk/relion//index.php?title=Conventions_%26_File_formats

*Also in this wikipedia link, we can find the image I/O file formats, and the definition of CTF.

# Image I/O

RELION reads the following image file formats:

- MRC individual images (with extension .mrc)
- MRC stacks (with extension .mrcs) (this is the recommended image format)
- SPIDER individual images (with extension .spi)
- SPIDER stacks (with extension .spi)
- IMAGIC stacks (with extensions .hed and .img)
- TIFF movies (with extensions .tif and .tiff)
- Preparation of the images is explained on the Prepare_input_files page.

For compatibility with other EM programs (e.g. UCSF MotionCor2, IMOD), TIFF images are flipped along the slow axis when being read into memory or written to a file. This happens regardless of the TIFFTAG_ORIENTATION value in the header.

RELION writes individual images and image stacks in MRC format. Because there is no distinction between 3D maps or stacks of 2D images in the MRC format, 3D maps are indicated with a .mrc extension, and stacks with a .mrcs extension. Individual images in stacks are indicated by an integer number (ranging from 1 to the number of images in the stack) followed by an "@" sign and the filename of the stack. Thereby, the first three images in a stack called my_images.mrcs are called:

1@my_images.mrcs
2@my_images.mrcs
3@my_images.mrcs
