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

## Particle extraction
```sh
`which relion_preprocess_mpi` --i Select/job049/micrographs.star --reextract_data_star Select/job080/particles.star --recenter --recenter_x 0 --recenter_y 0 --recenter_z 0 --part_star Extract/job083/particles.star --part_dir Extract/job083/ --extract --extract_size 200 --norm --bg_radius 75 --white_dust 5 --black_dust 5 --invert_contrast  --only_do_unfinished   --pipeline_control Extract/job083/ && echo Select/job049/micrographs.star > Extract/job083/coords_suffix_extract.star

`which relion_preprocess_mpi` --i Select/job049/micrographs.star --coord_dir Import/job050/ --coord_suffix _automatch.star --part_star Extract/job152/particles.star --part_dir Extract/job152/ --extract --extract_size 200 --scale 100 --norm --bg_radius 37 --white_dust 5 --black_dust 5 --invert_contrast   --pipeline_control Extract/job152/
```

## 2D classification
```sh
`which relion_refine_mpi` --o Class2D/job152/run --i Extract/job085/particles.star --dont_combine_weights_via_disc --scratch_dir /lscratch/$SLURM_JOB_ID --pool 30 --pad 2  --ctf  --ctf_intact_first_peak  --iter 50 --tau2_fudge 2 --particle_diameter 200 --fast_subsets  --K 200 --flatten_solvent  --zero_mask  --oversampling 1 --psi_step 12 --offset_range 5 --offset_step 2 --norm --scale  --j 3 --gpu ""  --pipeline_control Class2D/job152/
```

## 3D classification
```sh
`which relion_refine_mpi` --o Class3D/job152/run --i Extract/job083/particles.star --ref ../InitialModels/job051_run_it050_class001_Box200px0.85.mrc --firstiter_cc --ini_high 50 --dont_combine_weights_via_disc --scratch_dir /lscratch/$SLURM_JOB_ID --pool 3 --pad 2  --skip_gridding  --ctf --ctf_corrected_ref --iter 75 --tau2_fudge 4 --particle_diameter 200 --fast_subsets  --K 4 --flatten_solvent --zero_mask --oversampling 1 --healpix_order 3 --offset_range 5 --offset_step 2 --sym C1 --norm --scale  --j 1 --gpu ""  --pipeline_control Class3D/job152/
```

## 3D auto-refine
```sh
`which relion_refine_mpi` --o Refine3D/job152/run --auto_refine --split_random_halves --i Select/job107/particles.star --ref Class3D/job105/run_it070_class002.mrc --firstiter_cc --ini_high 40 --dont_combine_weights_via_disc --pool 30 --pad 2  --skip_gridding  --ctf --ctf_corrected_ref --particle_diameter 160 --flatten_solvent --zero_mask --oversampling 1 --healpix_order 2 --auto_local_healpix_order 4 --offset_range 5 --offset_step 2 --sym C1 --low_resol_join_halves 40 --norm --scale  --j 1 --gpu ""  --pipeline_control Refine3D/job152/
```

## Mask creation
```sh
`which relion_mask_create` --i Refine3D/job110/run_class001.mrc --o MaskCreate/job152/mask.mrc --lowpass 15 --ini_threshold 0.0005 --extend_inimask 3 --width_soft_edge 6 --j 16  --pipeline_control MaskCreate/job152/
```

## Post-processing
```sh
`which relion_postprocess` --mask MaskCreate/job113/mask.mrc --i Refine3D/job110/run_half1_class001_unfil.mrc --o PostProcess/job152/postprocess  --angpix 0.85 --auto_bfac  --autob_lowres 10  --pipeline_control PostProcess/job152/
```

## CTF refinement
```sh
`which relion_ctf_refine_mpi` --i Refine3D/job300/run_data_image-shift-grouped.star --f PostProcess/job520/postprocess.star --o CtfRefine/job844/ --fit_defocus --kmin_defocus 30 --fit_mode fpmff --fit_beamtilt --kmin_tilt 30 --odd_aberr_max_n 3 --j 2  --pipeline_control CtfRefine/job844/
```

## Bayesian polishing
```sh
`which relion_motion_refine` --i Refine3D/job511/run_ct21_data.star --f PostProcess/job524/postprocess.star --corr_mic MotionCorr/job150/corrected_micrographs.star --first_frame 1 --last_frame -1 --o Polish/job844/ --min_p 10000 --eval_frac 0.5 --align_frac 0.5 --params3  --j 32  --pipeline_control Polish/job844/
```

## Particle subtraction
```sh
`which relion_project` --subtract_exp --i Refine3D/job777/run_ct25_class001.mrc --mask MaskCreate/SelfBuild/maskA.mrc --ang Refine3D/job777/run_ct25_data.star --o Subtract/job844/subtracted --ctf --angpix -1 
```


## Join star files
```sh
`which relion_star_handler` --combine --i " Select/job600/particles.star Select/job601/particles.star Select/job602/particles.star Select/job603/particles.star "  --check_duplicates rlnImageName  --o JoinStar/job605/join_particles.star  --pipeline_control JoinStar/job605/
```















