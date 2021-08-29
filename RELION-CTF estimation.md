## Function and Application:
#This step is to estimate the CTF parameters for each corrected micrograph.

## Algorithm and Principle:
```sh
`which relion_run_ctffind_mpi` --i Import/job006/micrographs.star --o CtfFind/job012/ --Box 512 --ResMin 30 --ResMax 5 --dFMin 5000 --dFMax 50000 --FStep 500 --dAst 100 --ctffind_exe /usr/local/apps/ctffind/4.1.14/ctffind --ctfWin -1 --is_ctffind4  --fast_search   --pipeline_control CtfFind/job012/
```


## Materials and Methods:
#

## Results and Interpretation:
#
