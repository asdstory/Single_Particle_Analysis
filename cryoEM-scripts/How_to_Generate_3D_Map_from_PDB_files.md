*In some cases of SPR, we may need an initial model. One way to generate an initial model is to convert from the pdb file from RCSB PDB database, to find a protein with similar topology and convert pdb to get mrc map.

# On my Linux computer, Jianglab, we do

```
module load EMAN/1.9_jiang

pdb2mrc 4qim.pdb 4qim.mrc apix=1.06 res=2.6 center box=200
```

In this way, we get initial model with desired pixel size and box size for class3D reconstruction. 

*For more details, see: https://www.mrc-lmb.cam.ac.uk/rlw/text/doc/progs/pdb2mrc.html. 


