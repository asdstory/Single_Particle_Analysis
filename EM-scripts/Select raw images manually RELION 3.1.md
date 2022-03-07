*Since RELION 3.1, the relion_display function cannot perform correct lowpass anymore, you will only get dark image instead of raw images with clear particles. Therefore, this new protocol is to compensate this by using relion_image_handler to rescale the raw image first and then open relion_display function and manually select/remove raw images after CTFFind step. *

# Step01 - Convert motioncorrected raw image into small scale images 



```sh
# cd to your target Motioncor job folder
cd MotionCorr/job044/finished-frames/

# Create a new folder for temporary use
mkdir tmp

# Then, move all mrc files into above folder
mv *_????????.mrc tmp/

# Run relion_image_handler to convert images into rescaled small images for view.

cd back to project directory:

for i in MotionCorr/job044/finished-frames/tmp/*_????????.mrc; do echo relion_image_handler --i $i --o MotionCorr/job044/finished-frames/`basename $i` --angpix 1 --rescale_angpix 10; done > runpar.cmd

for i in MotionCorr/job145/Micrographs_selected/tmp/*_????????.mrc; do echo relion_image_handler --i $i --o MotionCorr/job145/Micrographs_selected/`basename $i` --angpix 1 --rescale_angpix 10; done > runpar.cmd

module load EMscript
runpar_gpu.py -p32 runpar.cmd

# Now, you will have rescaled raw images for view and selection using relion_display multiviewer
```


# Step02 - Start a Relion

cd to your project folder, and start a relion project GUI, e.g., in Biowulf I do:

- [ ] cd /data/dout2/20200427Krios_PnuC_3NR_Nanodisc
- [ ] module load RELION/3.0.8
- [ ] relion&

# Step03 - Start a new subset selection job from project GUI
## I/O

OR select from micrographs.star: CtfFind/job006/micrographs_ctf.star

- [ ] click "Run"

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Start%20a%20new%20Selection.png" width="600">

- [ ] A Relion display GUI will pop-up, just close it, and mark the above Select job as finished by clicking "Job action" button and then "Mark as finished" 

*Now you will get the selection job number, which will be used in the next step, e.g., here I get "Select/job016/"*

# Step04 - Start a display GUI from command line

Go back to the terminal, cd to the main project folder (the one that contains relion default pipeline.star) and type/copy & paste the following command, make sure you change the job number of the input (CtfFind/job006/micrographs_ctf.star) and the output (Select/job016/micrographs.star), other wise you won't be able to save selected micrographs.star successfully. 

```shell
`which relion_display` --i CtfFind/job006/micrographs_ctf.star --display rlnMicrographName --scale 0.07 --lowpass 30 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20 --fn_imgs Select/job016/micrographs.star
```
```sh
`which relion_display` --i CtfFind/job047/micrographs_ctf.star --ignore_optics --display rlnMicrographName --scale 0.07 --lowpass 30 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20000 --fn_imgs Select/job049/micrographs.star
```
```sh
`which relion_display` --gui --i CtfFind/job047/micrographs_ctf.star --allow_save --fn_imgs Select/job049/micrographs.star  --pipeline_control Select/job049/
```
```sh
`which relion_display` --i CtfFind/job047/micrographs_ctf.star  --display rlnMicrographName --scale 0.65 --lowpass 0 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20000 --fn_imgs Select/job049/micrographs.star

`which relion_display` --i Select/job156/micrographs.star  --display rlnMicrographName --scale 0.65 --lowpass 20 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20000 --fn_imgs Select/job157/micrographs.star

```


Or, to select from ctf image:

```sh
`which relion_display` --i CtfFind/job027/micrographs_ctf.star --display rlnCtfImage --scale 0.07 --lowpass 30 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20 --fn_imgs Select/job032/micrographs.star
```

*Note:  You may want to change the **--max_nr_images from 20 to the image number you have**, problem is it may take longer time to open all of them*

# Step05 - Start browing, selecting and saving

A new Relion display GUI will pop-up (may take long time if open too many images), in which we will see all raw images. 

- [ ] Click the first image, and then right click again and click "Select all below"

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Select%20all%20below.png" width="600">

- [ ] Now, by pulling up and down, we can glance over all raw images, just click any images we don't want. 
- [ ] When finished, just right click any of the images selected (in red frame), and click "Save STAR with selected images". You will see in the terminal telling you "Saved Select/job016/micrographs.star with xx selected images".

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Save%20STAR.png" width="600">

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Saved%20terminal.png" width="800">

Now that we finished image selection by glancing over all raw images, it is ready to pick particles and do following processing steps. Good luck!






