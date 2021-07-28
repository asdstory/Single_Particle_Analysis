# CRYO-EM: HOW TO CHANGE BOX SIZE AND PIXEL SIZE

From:
1. http://molecularart.dk/2015/11/cryo-em-how-to-change-box-size-and-pixel-size/
2. https://hpc.nih.gov/apps/EMAN2.html

# Short info that could be of interest for people new in cryo-EM:

module load EMAN2

e2iminfo.py cryosparc_P7_J30__localfilter_2.8A.mrc

# You can then change the box size (in pixels) the map by using Relion from the command line.

#For example if you want to change the box size of your map to 300x300x300 pixels from whatever it was before, you just type:

relion_image_handler --i cryosparc_P7_J30__localfilter_2.8A.mrc --new_box 200 --o cryosparc_200Pix.mrc

# You can also use relion_image_handler (among other things) for rescaling a map to a new pixel size (in Å).

#Let say you want to change the pixel size of your map from before to 4 Å:

relion_image_handler --i cryosparc_200Pix.mrc --rescale_angpix 1.26 --o cryosparc_200Pix1.26A.mrc

# You may want to change the pixel size first.

## If you want to get a map with Boxsize 200 and Pixel size 1.06A, you may want to do Pixel size first, and then box size, while use EMAN2 to check the box size that is :

- [ ] relion_image_handler --i cryosparc_P7_J30__localfilter_2.8A.mrc --rescale_angpix 1.26 --o cryosparc_Pix1.26A.mrc
- [ ] relion_image_handler --i cryosparc_Pix1.26A.mrc --new_box 200 --o cryosparc_200Pix1.26A.mrc
- [ ] e2iminfo.py cryosparc_200Pix1.26A.mrc


```shell
ml RELION/3.0.8
relion_image_handler --i job051_run_it050_class001.mrc --rescale_angpix 0.85 --force_header_angpix 0.85 --o  class001_pix0.85.mrc 
relion_image_handler --i cryosparc_Pix1.26A.mrc --new_box 200 --o cryosparc_200Pix1.26A.mrc

#Check details
relion_image_handler --i cryosparc_200Pix1.26A.mrc --stats
```


