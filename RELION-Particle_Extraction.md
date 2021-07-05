### This is typical example of how RELIONdo particle extraction:
Doing it without MPI: 
```sh
`which relion_preprocess` --i Select/job049/micrographs.star --coord_dir Import/job050/ --coord_suffix _automatch.star --part_star Extract/job128/particles.star --part_dir Extract/job128/ --extract --extract_size 200 --scale 100 --norm --bg_radius 37 --white_dust 5 --black_dust 5 --invert_contrast   --pipeline_control Extract/job128/
```

doing it with MPI:
```sh
`which relion_preprocess_mpi` --i Select/job049/micrographs.star --coord_dir Import/job050/ --coord_suffix _automatch.star --part_star Extract/job085/particles.star --part_dir Extract/job085/ --extract --extract_size 200 --scale 100 --norm --bg_radius 37 --white_dust 5 --black_dust 5 --invert_contrast  --only_do_unfinished   --pipeline_control Extract/job085/
```
Or, reextract particles like this:
```sh
`which relion_preprocess_mpi` --i Select/job049/micrographs.star --reextract_data_star Select/job080/particles.star --recenter --recenter_x 0 --recenter_y 0 --recenter_z 0 --part_star Extract/job083/particles.star --part_dir Extract/job083/ --extract --extract_size 200 --norm --bg_radius 75 --white_dust 5 --black_dust 5 --invert_contrast  --only_do_unfinished   --pipeline_control Extract/job083/ && echo Select/job049/micrographs.star > Extract/job083/coords_suffix_extract.star
```
