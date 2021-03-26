# Sometimes you may want to use multiple references for your class3D jobs in RELION, just like what you did in Cryosparc, especially to deal with heterogeneity. --From Dr Jiansen Jiang @ NIH
## How to do it: 
Just prepare the reference mrc files and then make a list star file as following (similar to the one RELION generated in Class3D jobs, the model.star file), then in the Class3D reference input option, load the star file as input reference. 

## Step 01 Generate an empty star file:

- [ ] touch class3D_model_5.star

## Step 02 Write down all template information into this star file as following: 

### File name: class3D_model_5.star
```
data_

loop_
_rlnReferenceImage #1
Class3D/job105/run_it_050_class001.mrc
Class3D/job105/run_it_050_class002.mrc
Class3D/job105/run_it_050_class003.mrc
Class3D/job105/run_it_050_class004.mrc
Class3D/job094/run_it_050_class001.mrc
```
