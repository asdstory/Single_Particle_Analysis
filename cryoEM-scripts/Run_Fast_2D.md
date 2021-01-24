# This script is to try to run a fast 2D classification of a new dataset
Mostly in order to have quick view of the results, or in another word, for grid/sample screening purpose. For example, to get quick results from TF20 screening data. Therefore, the start point is Raw image after motioncorr, e.g. "2020-12-04-TYD-Top1-corrected-averages"

## Step01 - cd to the dataset folder that contains the "xxx-xxx-xxx-corrected-averages"

## Step02 - Load the RELION module

- [ ] ml RELION

## Step03 - Start Relion, and then close it. This is to generate a new project. 

## Step04 - Run the following script, when running smoothly, you will get the 2D classification results directly. Just start Relion GUI again, you should be able to see the 2D classification results.


```sh

#!/bin/sh

cd 2021-01-15-TYD-Top1-corrected-averages

module load Gautomatch/0.56

Gautomatch --apixM 1.26 --diameter 100 *_sum_DW.mrc

cd -

relion_import  --do_coordinates  --i "2021-01-15-TYD-Top1-corrected-averages/*_automatch.box" --odir Import/job001/ --ofile coords_suffix_automatch.box --pipeline_control Import/job001/

relion_import  --do_micrographs  --optics_group_name "opticsGroup1" --angpix 1.26 --kV 200 --Cs 1.2 --Q0 0.1 --beamtilt_x 0 --beamtilt_y 0 --i "2021-01-15-TYD-Top1-corrected-averages/*_sum_DW.mrc" --odir Import/job002/ --ofile micrographs.star --pipeline_control Import/job002/

`which relion_run_ctffind_mpi` --i Import/job003/micrographs.star --o CtfFind/job003/ --Box 512 --ResMin 30 --ResMax 5 --dFMin 5000 --dFMax 50000 --FStep 500 --dAst 100 --ctffind_exe /data/jianglab-nfs/programs/apps/ctffind-4.1.13/ctffind --ctfWin -1 --is_ctffind4  --fast_search   --pipeline_control CtfFind/job003/

`which relion_preprocess_mpi` --i CtfFind/job003/micrographs_ctf.star --coord_dir Import/job001/ --coord_suffix _automatch.box --part_star Extract/job006/particles.star --part_dir Extract/job004/ --extract --extract_size 200 --norm --bg_radius 75 --white_dust 5 --black_dust 5 --invert_contrast   --pipeline_control Extract/job004/

`which relion_refine_mpi` --o Class2D/job005/run --i Extract/job005/particles.star --dont_combine_weights_via_disc --pool 3 --pad 2  --ctf  --ctf_intact_first_peak  --iter 25 --tau2_fudge 2 --particle_diameter 200 --fast_subsets  --K 50 --flatten_solvent  --zero_mask  --oversampling 1 --psi_step 12 --offset_range 5 --offset_step 2 --norm --scale  --j 2 --gpu "0"  --pipeline_control Class2D/job005/


```
