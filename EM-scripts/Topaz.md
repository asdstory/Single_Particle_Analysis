Topaz is application for particle detection in cryo-electron microscopy. Topaz uses convolutional neural networks trained from positive and unlabeled examples. Topaz can also do denoising of micrographs and tomograms..

References:
- Bepler, T., Morin, A., Rapp, M., Brasch, J., Shapiro, L., Noble, A.J., Berger, B. Positive-unlabeled convolutional neural networks for particle picking in cryo-electron micrographs. Nat Methods 16, 1153–1160 (2019).
- https://github.com/tbepler/topaz/blob/master/tutorial/01_quick_start_guide.ipynb
- https://github.com/tbepler/topaz/blob/master/tutorial/02_walkthrough.ipynb
- 

### Step1 Setup

mkdir a new folder, and then randomly copy some raw image (here after motioncor) to it.

```sh
cd /lscratch/$SLURM_JOB_ID

mkdir -p rawdata/micrographs

cd /data/dout2/20211004Krios_mOCT1-noGFP-LMNG/MotionCorr/job003/finished-frames

cp $(ls | grep '[0-9].mrc' |sort -R | head -100) /lscratch/$SLURM_JOB_ID/rawdata/micrographs/



```

### Step2 Denoise micrographs

```sh
topaz denoise /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/rawdata/micrographs/*.mrc --model unet --device 0 --format mrc --patch-size 1536 --patch-padding 384 --normalize --output /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/denoise/micrographs/
```

### Step3 preprocess

```sh

[dout2@cn4179 micrographs]$ ml IMOD
[+] Loading IMOD 4.11.5 . Running with 56  CPUs 
[dout2@cn4179 micrographs]$ header 14sep05c_c_00004gr_00032sq_00040hl_00002es_c.mrc

 RO image file on unit   1 : 14sep05c_c_00004gr_00032sq_00040hl_00002es_c.mrc     Size=     222485 K

                    This file has an old-style MRC header.

 Number of columns, rows, sections .....    7420    7676       1
 Map mode ..............................    2   (32-bit real)              
 Start cols, rows, sects, grid x,y,z ...    0     0     0       1      1      1
 Pixel spacing (Angstroms)..............   1.000      1.000      1.000    
 Cell angles ...........................   90.000   90.000   90.000
 Fast, medium, slow axes ...............    X    Y    Z
 Origin on x,y,z .......................    0.000       0.000       0.000    
 Minimum density .......................  -3.5590    
 Maximum density .......................   91.954    
 Mean density ..........................   16.100    
 tilt angles (original,current) ........   0.0   0.0   0.0   0.0   0.0   0.0
 Space group,# extra bytes,idtype,lens .        0        0        0        0

     0 Titles :



topaz preprocess -d 0 -v -s 8 -o processed/micrographs/ rawdata/micrographs/*.mrc

topaz convert --from star --to coord -o particles.txt particles.star 

topaz convert -s 8 -o data/EMPIAR-10025/processed/particles.txt data/EMPIAR-10025/rawdata/particles.txt

topaz preprocess /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/denoise/micrographs/*.mrc --scale 4 --sample 1 --num-workers 16 --format mrc,png --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/processed/micrographs/

topaz preprocess finished-frames/*[0-9].mrc --scale 4 --sample 1 --num-workers 16 --format mrc --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/

topaz preprocess original_2/*[0-9].mrc --scale 4 --sample 1 --num-workers 8 --format mrc --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/

topaz preprocess original_2/20211007_*.mrc --scale 4 --sample 1 --num-workers 8 --format mrc --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/ &

topaz preprocess original_2/20211008_*.mrc --scale 4 --sample 1 --num-workers 8 --format mrc --device 1 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/ &

topaz preprocess original_2/20211009_*.mrc --scale 4 --sample 1 --num-workers 8 --format mrc --device 2 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/ &

for i in MotionCorr/job003/finished-frames/*_????????.mrc; do echo topaz preprocess $i --scale 4 --sample 1  --format mrc --niters 100 --alpha 900 --beta 1 --verbose --destdir MotionCorr/job003/processed/micrographs/`basename $i`; done > runpar.cmd 

for i in processed/micrographs/*.mrc; do rm orignal_2/`basename $i`; done


module load EMscript
runpar_gpu.py -p32 runpar.cmd

topaz convert -s 4 -o particles.txt ../../../ManualPick/job063/rawdata/micrographs/particles.txt

topaz convert -s 8 -o processed/particles.txt rawdata/particles.txt 

```

### Step4 Training

```sh
mkdir -p saved_models/EMPIAR-10025

topaz train -n 400 --num-workers=8 --train-images data/EMPIAR-10025/processed/micrographs/ --train-targets data/EMPIAR-10025/processed/particles.txt --save-prefix=saved_models/EMPIAR-10025/model -o saved_models/EMPIAR-10025/model_training.txt

topaz train -n 400 --num-workers=8 --train-images processed/micrographs/ --train-targets processed/particles.txt --save-prefix=saved_models/model -o saved_models/model_training.txt

[dout2@cn4179 EMPIAR-10025]$ topaz train -n 400 --num-workers=8 --train-images processed/micrographs/ --train-targets processed/particles.txt --save-prefix=saved_models/model -o saved_models/model_training.txt
# Loading model: resnet8
# Model parameters: units=32, dropout=0.0, bn=on
# Loading pretrained model: resnet8_u32
# Receptive field: 71
# Using device=0 with cuda=True
# Loaded 30 training micrographs with 1500 labeled particles
# source	split	p_observed	num_positive_regions	total_regions
# 0	train	0.00163	43500	26669790
# Specified expected number of particle per micrograph = 400.0
# With radius = 3
# Setting pi = 0.0130484716977524
# minibatch_size=256, epoch_size=1000, num_epochs=10
# Done!


topaz train --train-images /path/to/preprocessed/images/ --train-targets /path/to/training_particles.csv --k-fold 5 --fold 0 --radius 3 --model resnet8 --image-ext .mrc --units 32 --dropout 0.0 --bn on --unit-scaling 2 --ngf 32 --method GE-binomial --autoencoder 0 --num-particles 300 --l2 0 --learning-rate 0.0002 --minibatch-size 256 --minibatch-balance 0.0625 --epoch-size 5000 --num-epochs 10 --num-workers -1 --test-batch-size 1 --device 0 --save-prefix /output/path/model --output /output/path/results.txt

topaz train -n 400 --num-workers=50 --train-images micrographs/ --train-targets particles.txt --save-prefix=model -o model/training.txt

[dout2@cn4201 processed]$ topaz train -n 400 --num-workers=50 --train-images micrographs/ --train-targets particles.txt --save-prefix=model -o model/training.txt
WARNING: While bind mounting '/gs10:/gs10': destination is already in the mount point list
# Loading model: resnet8
# Model parameters: units=32, dropout=0.0, bn=on
# Loading pretrained model: resnet8_u32
# Receptive field: 71
# Using device=0 with cuda=True
Traceback (most recent call last):
  File "/usr/local/conda/bin/topaz", line 11, in <module>
    load_entry_point('topaz-em==0.2.4', 'console_scripts', 'topaz')()
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/main.py", line 148, in main
    args.func(args)
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/commands/train.py", line 641, in main
    image_ext=args.image_ext
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/commands/train.py", line 231, in load_data
    , sources=train_images.source)
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/utils/data/loader.py", line 130, in load_images_from_list
    im = load_image(path, standardize=standardize)
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/utils/data/loader.py", line 103, in load_image
    image = load_mrc(path, standardize=standardize)
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/utils/data/loader.py", line 51, in load_mrc
    image, header, extended_header = mrc.parse(content)
  File "/usr/local/conda/lib/python3.7/site-packages/topaz/mrc.py", line 111, in parse
    header = MRCHeader._make(header_struct.unpack(content[:1024]))
struct.error: unpack requires a buffer of 1024 bytes

topaz train -n 400 --num-workers=50 --train-images processed/micrographs/ --train-targets processed/particles.txt --save-prefix=saved_models/model -o saved_models/model_training.txt


```

### Step5 Extraction

```sh
mkdir -p data/EMPIAR-10025/topaz

topaz extract -r 14 -x 8 --per-micrograph --format star -m saved_models/model_epoch10.sav -o rawdata/micrographs/ processed/micrographs/*.mrc

topaz extract -r 14 -x 4 --per-micrograph --format star -m saved_models/model_epoch10.sav -o rawdata/micrographs/ processed/micrographs/*.mrc

topaz extract -r 14 -x 8 -m saved_models/EMPIAR-10025/model_epoch10.sav -o data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt data/EMPIAR-10025/processed/micrographs/*.mrc


topaz extract -r 28 -x 4 -m saved_models/EMPIAR-10025/model_epoch10.sav -o data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt data/EMPIAR-10025/processed/micrographs/*.mrc


topaz extract /path/to/preprocessed/images/*.mrc --model resnet16_u64 --radius 8 --threshold -6 --up-scale 1 --batch-size 1 --min-radius 5 --max-radius 100 --step-radius 5 --num-workers -1 --device 0 --output /path/to/extracted/particles.txt

topaz convert /path/to/extracted/particles.txt --verbose 1 --output /path/to/extracted/particles.star

topaz convert /path/to/extracted/particles.txt --verbose 1 --output /path/to/extracted/particles.csv

topaz convert --from coord --to star predicted_particles_all_upsampled.txt  -o predicted_particles_all_upsampled.star

topaz extract -r 14 -x 4 --per-micrograph --format star -m /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/saved_models/model_epoch10.sav -o processed/micrographs/ processed/micrographs/*.mrc


```
### Step5 change format of particle coordinates file

```sh
topaz convert -o data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.star data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt 


```

### Step6 Generate MRC particle stack

```sh

%%bash
source activate topaz

# here, we generate the particle stack using the predicted particles after upsamapling
# per-micrograph metadata (such as CTF parameters) can be optionally included in the 
# .star file generated with the particle stack

# --size specifies the dimensions of the particle crops
# --threshold specifies the score threshold above which to include particles in the stack
# --metadata is optional and in this case contains CTF parameters

# if output file is named "particles.mrc" then the .star file created will be "particles.star"

topaz particle_stack --image-root=data/EMPIAR-10025/rawdata/micrographs/ \
                     --size=400 \
                     --threshold=0 \
                     --metadata=data/EMPIAR-10025/rawdata/ctf_params.star \
                     -o data/EMPIAR-10025/topaz/predicted_particle_stack.mrcs \
                     data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt

```

