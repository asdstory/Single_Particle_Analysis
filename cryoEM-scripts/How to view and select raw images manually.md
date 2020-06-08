*This step-by-step protocol is used to view all the raw images by naked eyes and get rid of bad images based on experience, and then save selected/good micrograhs' STAR for further use. Thus, this step is usually used/performed after the CTF estimation step, and use the micrographs_ctf.star as the input.*

# Step01 - Start a Relion

cd to your project folder, and start a relion project GUI, e.g., in Biowulf I do:

- [ ] cd /data/dout2/20200427Krios_PnuC_3NR_Nanodisc
- [ ] module load RELION/3.0.8
- [ ] relion&

# Step02 - Start a new subset selection job from project GUI
## I/O

OR select from micrographs.star: CtfFind/job006/micrographs_ctf.star

- [ ] click "Run"

- [ ] A Relion display GUI will pop-up, just close it, and mark the above Select job as finished by clicking "Job action" button and then "Mark as finished" 

*Now you will get the selection job number, which will be used in the next step, e.g., here I get "Select/job016/"*

# Step03 - Start a display GUI from command line

Go back to the terminal and type/copy & paste the following command, make sure you change the job number of the input (CtfFind/job006/micrographs_ctf.star) and the output (Select/job016/micrographs.star), other wise you won't be able to save selected micrographs.star successfully. 

- [ ] `which relion_display` --i CtfFind/job006/micrographs_ctf.star --display rlnMicrographName --scale 0.07 --lowpass 30 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20 --fn_imgs Select/job016/micrographs.star

# Step04 - Start browing, selecting and saving

Now a new Relion display GUI will pop-up (may take long time if open too many images), in which we will see all raw images. 

- [ ] Click the first image, and then right click again and click "Select all below"
- [ ] Now, by pulling up and down, we can glance over all raw images, just click any images we don't want. 
- [ ] When finished, just right click any of the images selected (in red frame), and click "Save STAR with selected images". You will see in the terminal telling you "Saved Select/job016/micrographs.star" with xx selected images".

Now that we finished image selection by glancing over all raw images, it is ready to pick particles and do following processing steps. Good luck!





