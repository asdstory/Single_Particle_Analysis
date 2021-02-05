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

<img src="Figures/Leginon_Image_Shift_Information.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
