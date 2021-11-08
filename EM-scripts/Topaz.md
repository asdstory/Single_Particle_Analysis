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

topaz preprocess -d 0 -v -s 4 -o processed/micrographs/ rawdata/micrographs/*.mrc

topaz convert --from star --to coord -o particles.txt particles.star 

topaz convert -s 8 -o data/EMPIAR-10025/processed/particles.txt data/EMPIAR-10025/rawdata/particles.txt

topaz preprocess /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/denoise/micrographs/*.mrc --scale 4 --sample 1 --num-workers 16 --format mrc,png --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir /data/dout2/TutorialData/Topaz/20211004Krios_mOCT1-noGFP/processed/micrographs/

topaz preprocess finished-frames/[0-9].mrc --scale 4 --sample 1 --num-workers 16 --format mrc --device 0 --niters 100 --alpha 900 --beta 1 --verbose --destdir processed/micrographs/

```

### Step4 Training

```sh
mkdir -p saved_modles/EMPIAR-10025

topaz train -n 400 --num-workers=8 --train-images data/EMPIAR-10025/processed/micrographs/ --train-targets data/EMPIAR-10025/processed/particles.txt --save-prefix=saved_models/EMPIAR-10025/model -o saved_models/EMPIAR-10025/model_training.txt


topaz train --train-images /path/to/preprocessed/images/ --train-targets /path/to/training_particles.csv --k-fold 5 --fold 0 --radius 3 --model resnet8 --image-ext .mrc --units 32 --dropout 0.0 --bn on --unit-scaling 2 --ngf 32 --method GE-binomial --autoencoder 0 --num-particles 300 --l2 0 --learning-rate 0.0002 --minibatch-size 256 --minibatch-balance 0.0625 --epoch-size 5000 --num-epochs 10 --num-workers -1 --test-batch-size 1 --device 0 --save-prefix /output/path/model --output /output/path/results.txt
```

### Step5 Extraction

```sh
mkdir -p data/EMPIAR-10025/topaz

topaz extract -r 14 -x 8 -m saved_models/EMPIAR-10025/model_epoch10.sav -o data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt data/EMPIAR-10025/processed/micrographs/*.mrc


topaz extract /path/to/preprocessed/images/*.mrc --model resnet16_u64 --radius 8 --threshold -6 --up-scale 1 --batch-size 1 --min-radius 5 --max-radius 100 --step-radius 5 --num-workers -1 --device 0 --output /path/to/extracted/particles.txt

topaz convert /path/to/extracted/particles.txt --verbose 1 --output /path/to/extracted/particles.star

topaz convert /path/to/extracted/particles.txt --verbose 1 --output /path/to/extracted/particles.csv
```
### Step5 change format of particle coordinates file

```sh
topaz convert -o data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.star data/EMPIAR-10025/topaz/predicted_particles_all_upsampled.txt 


```
