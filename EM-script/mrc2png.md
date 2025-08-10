```sh
for i in ./*.mrc; do echo relion_image_handler --i  $i --o `basename $i .mrc`.png --lowpass 10; done > runpar.cmd
```
