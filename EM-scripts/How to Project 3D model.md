# Input:
3D model in .mrc format (e.g. input.mrc)
# How to
To project for particle picking, you do not need many fews. Therefore, a coarse angular sampling is recommended, such as 20 or 30 degrees. 

We will use RELION for projecting the 3D volume. But, before projecting, we will low-pass filter the model. 

## Log into any lab machine and type: 
```sh
$ module load relion
$ relion_image_handler --i input.mrc --o input_lp.mrc --angpix 1 --lowpass 10
$ relion_project --i input_lp.mrc --o input_lp_proj --nr_uniform 10
```
*This will output a stack of projects in .mrcs format and an accompanying .star file.

# Converting into individual files for Appion
If you want to pick particles in Appion, you will need to create individual .mrc files for these projections. 

## To do this: 
```sh
$ module load eman2
$ e2proc2d.py input_lp_proj.mrcs mrc  --unstacking
```
*This will output a series of files named mrc-??.mrc that can be uploaded to Appion.
