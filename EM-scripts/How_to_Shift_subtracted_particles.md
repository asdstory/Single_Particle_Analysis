## Here we use pyem subparticles.py to center/move the particles to the center, by giving the program exact x,y,z values we want to shift. 
### If we use the pyem/0.1 version, it is: 
```py
usage: subparticles.py [-h] [--apix APIX] [--boxsize BOXSIZE] [--class CLS]
                       [--displacement DISPLACEMENT] [--origin x,y,z]
                       [--target x,y,z] [--invert] [--psi PSI]
                       [--euler rot,tilt,psi] [--transform TRANSFORM]
                       [--recenter] [--adjust-defocus] [--shift-only]
                       [--loglevel LOGLEVEL] [--skip-join] [--suffix SUFFIX]
                       [--sym SYM]
                       input output
```

```py 
subparticles.py --apix 0.83 --boxsize 200 --target 0,0,-68 --shift-only subtracted.star subtracted_shift.star
```

### By using the pyem/0.4 version, it is: 
```py
python3 /home/dout2/programs/apps/pyem/pyem-0.4/subparticles.py
usage: subparticles.py [-h] [--apix APIX] [--boxsize BOXSIZE] [--class CLS]
                       [--displacement DISPLACEMENT] [--origin x,y,z]
                       [--target x,y,z] [--invert] [--psi PSI]
                       [--euler rot,tilt,psi] [--transform TRANSFORM]
                       [--recenter] [--adjust-defocus] [--shift-only]
                       [--loglevel LOGLEVEL] [--skip-join] [--suffix SUFFIX]
                       [--sym SYM] [--relion2]
                       input output

```

```py 
python3 /home/dout2/programs/apps/pyem/pyem-0.4/subparticles.py --apix 0.83 --boxsize 200 --target 0,0,-68 --shift-only subtracted.star subtracted_shift.star
```
