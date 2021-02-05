# Backgroud
### When you already get a at least 4.5A resolution after particle polishing and want to further improve/push, you may want to start estimate the beamtilt. Since Leginon uses image shift when collecting images, e.g., 4x4 or 5x5 per batch, we may want to introduce the image shift information from Leginon database into RELION star file so that we can estimate Beamtilt and do high order aberration correction. In another word, to do better CTF correction by doing high order aberration estimation/correction.

# Step 1 - Export the Beamtilt information from Leginon

### Login to the leginon computer
- [ ] ssh krios@leginon.niddk.nig.gov
### Go to the "/local/bin/" folder and run the script "get_image_shift_data_all.sh" and name the output file, which contain the Beamtilt information for every image Leginon has taken.
- [ ] cd /local/bin
- [ ]  ./get_image_shift_data_all.sh > leginon_image_shift_data_all_2021-02-04.txt
### And if you view this file, you will be able to see the ID, date, grid name and the image shift information that Leginon generated when taking each image. 
- [ ] more leginon_image_shift_data_all_2021-02-04.txt

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Leginon_Image_Shift_Information.png?raw=true"
     alt="leginon_image_shift_data from leginon"
     style="float: left; margin-right: 10px;" />

# Step 2 - Introduce ImageShift information into the RELION .star file (usually Refine3D job star file)
### Go to your dataset/project job folder, find the star file "run_data.star", and may remember the absolute address for this file.
- [ ] cd Refine3D/job300/
- [ ] pwd
### Go to the import folder of RELION, try export your image list in this way. This image list will be used in the program later.
- [ ] cat movies.star | grep .tif > image_list.txt
### Go to our own Linux machine, type "module avail", you will be able to find the "EMscript/0.1" which was written by Jiansen.
- [ ] module avail
- [ ] module load EMscript/0.1
### Just run the program in this way, input the (1)clusters, e.g. 16, or 25 (depends on how you collect the data using Leginon, e.g. 4x4 or 5x5), (2)image list,(3)star file, (4)image shift file, it will generate a new star file which you can use in later CTF refine jobs and turn on the estimate Beamtilt option to estimate the beamtilt aberrations.
- [ ] relion_group_image_shift.py --clusters=16 --image_shift_data=/data/nhlbi-nfs/lab-jiang/EM-RAW-DATA/jiangji2/krios_image_shift_data_all_20201119.txt --image_list=image_list.txt --input_star=run_data.star --output_star=run_data_image-shift-grouped.star
### You should be able to see the new "run_data_image-shift-grouped.star", which will be like this if you view it that the "\_rlnBeamTiltClass #32" was inserted.
- [ ] more run_data_image-shift-grouped.star

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/run_data_image-shift-grouped-star.png?raw=true"
     alt="run_data_image-shift-grouped.star"
     style="float: left; margin-right: 10px;" />
### Jiansen's script will also generate a pdf file showing how good the cluster/group results will be. In general, if you see something like this then it should be fine/the program should work.
- [ ] gvfs-open image_shiftPnuC_20apr27a_g3.pdf

<img src="https://github.com/asdstory/Single-Particle-Reconstruction/blob/master/Figures/Image_shift_cluster%20result%20pdf.png?raw=true"
     alt="run_data_image-shift-grouped-star"
     style="float: left; margin-right: 1px;" />



