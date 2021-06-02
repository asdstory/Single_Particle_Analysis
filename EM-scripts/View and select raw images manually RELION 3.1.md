```sh





sjobs
fg 7

`which relion_display` --i CtfFind/job047/micrographs_ctf.star  --display rlnMicrographName --scale 0.05 --lowpass 0 --col 5 --ori_scale 1 --allow_save --max_nr_images 20 --fn_imgs Select/job049/micrographs.star &

head -n200 CtfFind/job047/micrographs_ctf.star > tmp/x1.star

relion_image_handler --i tmp/x1.star --o tmp/x2.mrcs --angpix 1 --rescale_angpix 10


for i in MotionCorr/job044/finished-frames/*_????????.mrc; do relion_image_handler --i $i --o tmp/`basename $i` --angpix 1 --rescale_angpix 10; done

for i in *.mrc; do echo _rlnMicrographName $i; done

for i in *.mrc; do echo _rlnMicrographName $i; done > x1.star
vi x1.star 

more ../CtfFind/job047/micrographs_ctf.star
relion_display --i x1.star --display rlnMicrographName
cat x1.star 

for i in MotionCorr/job044/finished-frames/*_????????.mrc; do echo relion_image_handler --i $i --o tmp/`basename $i` --angpix 1 --rescale_angpix 10; done

for i in MotionCorr/job044/finished-frames/*_????????.mrc; do relion_image_handler --i $i --o tmp/`basename $i` --angpix 1 --rescale_angpix 20; done

relion_display --i x1.star --display rlnMicrographName

for i in MotionCorr/job044/finished-frames/*_????????.mrc; do echo relion_image_handler --i $i --o tmp/`basename $i` --angpix 1 --rescale_angpix 10; done

for i in MotionCorr/job044/finished-frames/*_????????.mrc; do echo relion_image_handler --i $i --o tmp/`basename $i` --angpix 1 --rescale_angpix 10; done > runpar.cmd

wc -l runpar.cmd
cat runpar.cmd
sjobs
module load EMscript
runpar_gpu.py -p32 runpar.cmd


```
