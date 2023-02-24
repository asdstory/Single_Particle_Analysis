
```sh
`which relion_display` --i Select/job032/micrographs.star --display rlnMicrographName --scale 0.2 --sigma_contrast 3 --black 0 --white 0 --allow_save --col 2 --max_nr_images 40 --lowpass 20  --fn_imgs Select/job044/micrographs.star  --pipeline_control Select/job044/ 

`which relion_display` --i Select/job156/micrographs.star  --display rlnMicrographName --scale 0.65 --lowpass 20 --col 5 --ori_scale 0.1 --allow_save --max_nr_images 20000 --fn_imgs Select/job157/micrographs.star

`which relion_manualpick` --i Select/job032/micrographs.star --odir ManualPick/job045/ --pickname manualpick --allow_save   --fast_save --selection ManualPick/job045/micrographs_selected.star --scale 0.2 --sigma_contrast 3 --black 0 --white 0 --lowpass 20 --particle_diameter 100  --pipeline_control ManualPick/job045/
```
