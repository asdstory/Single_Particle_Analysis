### After particle subtraction, we may want to do quick reconstruction again using subtracted particles in order to get quick view of which part was actually subtracted.

```sh
relion_reconstruct --i subtracted.star --o subtracted_3D.mrc --sym c3 
```
or 

```sh
mpirun -n 20 relion_reconstruct_mpi --i t100_class2.star --o t100_class2.mrc --maxres 4.5 --ctf >& log1 &
```
