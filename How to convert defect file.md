## … use the defect file for MotionCor2?


According to SerialEM helpfile - http://bio3d.colorado.edu/SerialEM/hlp/html/about_camera.htm, here are the step to convert defect map that MotionCor2 needs:

Finally, if you want to run MotionCor2 directly on the unnormalized data, you should give it a defect map file as well as the gain reference file. You can make a defect map from the text file with ‘clip defect’ in IMOD 4.10.7 or higher:

- [ ] clip defect -D defects...txt  fileWithFrames  defects...mrc
where the fileWithFrames is used only to set the size of the output and can be any file of the right X and Y size. To make a compressed TIFF file, which will be much smaller, use:

- [ ] clip defect -D defects...txt  -f tif  fileWithFrames  defects...tif
