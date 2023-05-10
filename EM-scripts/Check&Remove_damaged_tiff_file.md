```sh
for i in *_fractions.tiff; do if tiffinfo -D $i ; then echo file is OK; mv $i tmp/; else     echo file is corrupt; fi; done


```
