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

### However, you may want to switch python version from 2 to 3 first before running subparticles.py

```sh
sudo update-alternatives --config python
```

```py
subparticles.py
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
subparticles.py --apix 0.83 --boxsize 200 --target 0,0,-68 --shift-only subtracted.star subtracted_shift.star
```
#### The subparticles.py is from: https://github.com/asarnow/pyem
