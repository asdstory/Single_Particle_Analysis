## Import:
```sh
relion_import  --do_movies  --optics_group_name "opticsGroup1" --angpix 0.425 --kV 300 --Cs 2.7 --Q0 0.1 --beamtilt_x 0 --beamtilt_y 0 --i "finished-frames/*.tif" --odir Import/job043/ --ofile movies.star --continue  --pipeline_control Import/job043/
relion_import  --do_coordinates  --i "MotionCorr/job044/finished-frames/*_automatch.star" --odir Import/job050/ --ofile coords_suffix_automatch.star --continue  --pipeline_control Import/job050/
```

## Motion correction
```sh
`which relion_run_motioncorr_mpi` --i Import/job043/movies_group.star --o MotionCorr/job044/ --first_frame_sum 1 --last_frame_sum -1 --use_own  --j 2 --bin_factor 2 --bfactor 150 --dose_per_frame 1.3054 --preexposure 0 --patch_x 7 --patch_y 5 --eer_grouping 0 --dose_weighting  --save_noDW  --only_do_unfinished   --pipeline_control MotionCorr/job044/
```

## CTF estimation
```sh
`which relion_run_ctffind_mpi` --i MotionCorr/job044/corrected_micrographs.star --o CtfFind/job047/ --Box 512 --ResMin 30 --ResMax 4 --dFMin 5000 --dFMax 30000 --FStep 500 --dAst 100 --use_noDW  --ctffind_exe /usr/local/apps/ctffind/4.1.14/ctffind --ctfWin -1 --is_ctffind4  --fast_search  --only_do_unfinished   --pipeline_control CtfFind/job047/
```

## Manual picking
```sh
`which relion_manualpick` --i CtfFind/job047/micrographs_ctf.star --odir ManualPick/job048/ --pickname manualpick --allow_save   --fast_save --selection ManualPick/job048/micrographs_selected.star --scale 0.2 --sigma_contrast 3 --black 0 --white 0 --lowpass 20 --ctf_scale 1 --particle_diameter 100  --pipeline_control ManualPick/job048/ && echo CtfFind/job047/micrographs_ctf.star > ManualPick/job048/coords_suffix_manualpick.star
```

## Subset selection
```sh
`which relion_display` --gui --i CtfFind/job047/micrographs_ctf.star --allow_save --fn_imgs Select/job049/micrographs.star  --pipeline_control Select/job049/
```























