### Source:

```sh

```

```sh
--lowpass_mask_micelle ../InitialModels/mOCT1-VB1_Protein_mask_Box320Pix083.mrc --lowpass 20

`which relion_refine_mpi` --o Refine3D/job287/run --auto_refine --split_random_halves --i Select/job237/particles.star --ref Class3D/job235/run_it050_class004.mrc --firstiter_cc --ini_high 30 --dont_combine_weights_via_disc --scratch_dir /lscratch/$SLURM_JOB_ID --pool 30 --pad 2  --skip_gridding  --ctf --particle_diameter 240 --flatten_solvent --zero_mask --solvent_mask ../InitialModels/mOCT1-mask_Box320Pix083.mrc --solvent_correct_fsc  --oversampling 1 --healpix_order 3 --auto_local_healpix_order 4 --offset_range 5 --offset_step 2 --sym C1 --low_resol_join_halves 40 --norm --scale  --j 1 --gpu "" --lowpass_mask_micelle ../InitialModels/mOCT1-VB1_Protein_mask_Box320Pix083.mrc --lowpass 20 --pipeline_control Refine3D/job287/
```
