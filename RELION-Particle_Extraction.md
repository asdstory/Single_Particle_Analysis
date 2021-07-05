### This is typical example of how RELIONdo particle extraction:
Doing it without MPI: 
```sh
`which relion_preprocess` --i Select/job049/micrographs.star --coord_dir Import/job050/ --coord_suffix _automatch.star --part_star Extract/job128/particles.star --part_dir Extract/job128/ --extract --extract_size 200 --scale 100 --norm --bg_radius 37 --white_dust 5 --black_dust 5 --invert_contrast   --pipeline_control Extract/job128/
```

Or, doing it with MPI:
```sh
`which relion_preprocess_mpi` --i Select/job049/micrographs.star --coord_dir Import/job050/ --coord_suffix _automatch.star --part_star Extract/job085/particles.star --part_dir Extract/job085/ --extract --extract_size 200 --scale 100 --norm --bg_radius 37 --white_dust 5 --black_dust 5 --invert_contrast  --only_do_unfinished   --pipeline_control Extract/job085/
```
