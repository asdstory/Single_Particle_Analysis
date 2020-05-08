# e2evalimage.py:

https://blake.bcm.edu/emanwiki/EMAN2/Programs/e2evalimage

- [ ] e2evalimage.py --apix 1.058 --voltage 300 --ac 0.1 --cs 2.7 ‪C:\Users\asdst_000\Desktop\class_averages-1.png

# e2proc2d.py

https://blake.bcm.edu/emanwiki/EMAN2/Programs/e2proc2d

1) make sure that your 3-D density map has the helical axis aligned along Z. If not, you can use e2proc3d.py with the --rot option to manually rotate it.
2) use e2project3d.py to generate ~azimuthal projections
- [ ] e2project3d.py mymap.mrc --outfile=proj.hdf --orientgen=eman:alt_min=88:delta=3:perturb=0 -v2
(note if it is an N-start helix, you could add --sym=cN to speed the process)

3) use e2proc2d to compute the average 2-D power spectrum
- [ ] e2proc2d.py class_averages-2.mrcs class_averages-2-.mrcs --apix=1.058 --fftavg=powspec-2.png

4) Display
- [ ] e2display.py powspec.hdf
