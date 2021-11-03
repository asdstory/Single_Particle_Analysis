Topaz is application for particle detection in cryo-electron microscopy. Topaz uses convolutional neural networks trained from positive and unlabeled examples. Topaz can also do denoising of micrographs and tomograms..

References:
- Bepler, T., Morin, A., Rapp, M., Brasch, J., Shapiro, L., Noble, A.J., Berger, B. Positive-unlabeled convolutional neural networks for particle picking in cryo-electron micrographs. Nat Methods 16, 1153–1160 (2019).

### Step1 mkdir a new folder, and then randomly copy some raw image (here after motioncor) to it.

```sh
cd /lscratch/$SLURM_JOB_ID

mkdir -p rawdata/micrographs

mkdir -p rawdata/micrographs

cd /data/dout2/20211004Krios_mOCT1-noGFP-LMNG/MotionCorr/job003/finished-frames

cp $(ls | grep '[0-9].mrc' |sort -R | head -50) /lscratch/$SLURM_JOB_ID/rawdata/micrographs/

```

### Step2 preprocess

```sh

topaz preprocess -d 0 -v -s 4 -o processed/micrographs/ rawdata/micrographs/*.mrc


topaz convert -s 8 -o data/EMPIAR-10025/processed/particles.txt data/EMPIAR-10025/rawdata/particles.txt
```

### Step3 

