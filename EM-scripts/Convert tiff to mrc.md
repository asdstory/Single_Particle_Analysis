```sh
for i in ./*_fractions.tiff; do echo tif2mrc $i tmp/`basename $i .tiff`.mrc; done > runpar.cmd

ml EMscrpt

runpar_gpu.py -p32 runpar.cmd
```
