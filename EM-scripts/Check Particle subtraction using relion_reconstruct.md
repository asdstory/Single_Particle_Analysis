### After particle subtraction, we may want to do quick reconstruction again using subtracted particles in order to get quick view of which part was actually subtracted.

```sh
relion_reconstruct --i /data/dout2/20200427Krios_PnuC_3NR_Nanodisc/Subtract/job744/subtracted_100k.star  --o /data/dout2/20200427Krios_PnuC_3NR_Nanodisc/Subtract/job744/subtracted_3D_100k.mrc --sym c3 --ctf TRUE
```
or 

```sh
mpirun -n 20 relion_reconstruct_mpi --i t100_class2.star --o t100_class2.mrc --maxres 4.5 --ctf >& log1 &
```
