### Setup our own Python environment and run personalized scripts on Biowulf:

Source: https://hpc.nih.gov/docs/diy_installation/conda.html

```sh
source myconda
mamba activate python2.7
#Then, run our script
python2 /data/dout2/Scripts/relion_group_image_shift_import.py --clusters=49 --image_shift_data=/data/dout2/Database/Image_Shift/leginon_image_shift_data_all_2023-07-14.txt --input_star=movies.star --output_star=movies_group.star

mamba deactivate
```
