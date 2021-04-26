# Automatic Particle picking
## Reference: 
https://hpc.nih.gov/apps/gautomatch.html

# For TF20 data, at 29kx:

#!/bin/bash

set -e

module load gautomatch

gautomatch --apixM 1.27 --diameter 80 --lave_D 100 --lave_min -0.8 --lsigma_cutoff 1.2  --cc_cutoff 0.25 *_sum_DW.mrc



# Allocate an interactive session and run the program. Sample session:

[user@biowulf]$ sinteractive --gres=gpu:k80:1 --mem=20g -c14

[user@biowulf]$ module load gautomatch

[user@cn3144 ~]$ gautomatch --apixM 1.34 --diameter 400 --T templates_lp40_3.2A.mrcs --apixT 3.2 --lave_D 100 --lave_min -0.8 --lsigma_cutoff 1.2  --cc_cutoff 0.25 test?.mrc

[user@cn3144 ~]$ gautomatch --apixM 0.93 --diameter 80 --T /data/dout2/PnuC_Map-Model/PnuCT0-3NR-C8_P6_J36_lf_3.0A_lp10_pj.mrcs --apixT 0.85 --lave_D 100 --lave_min -0.8 --lsigma_cutoff 1.2 --cc_cutoff 0.25 *Fractions.mrc


#Or, for simple use, just

# For TF20 data
gautomatch --apixM 1.27 --diameter 150 *_sum_DW.mrc 

# For Titan Krios data at low mag (13kx)
```
gautomatch --apixM 1.06 --diameter 80 --min_dist 30 *_sum_DW.mrc

#Batch job on biowulf

#Most jobs should be run as batch jobs.
#Create a batch input file (e.g. gautomatch.sh). For example:

#!/bin/bash

set -e
module load gautomatch
gautomatch --apixM 1.34 --diameter 400 --T templates_lp40_3.2A.mrcs --apixT 3.2 --lave_D 100 --lave_min -0.8 --lsigma_cutoff 1.2  --cc_cutoff 0.25 test?.mrc
```
## Submit this job using the Slurm sbatch command.

sbatch --partition=gpu --gres=gpu:k20x:1 --cpus-per-task=14 --mem=20g gautomatch.sh --time=06:00:00

# How to use Gautomatch in our Linux computer, JiangLab

module load Gautomatch/0.56

Gautomatch --apixM 1.26 --diameter 100 *_sum_DW.mrc

Gautomatch --apixM 1.26 --diameter 80 --min_dist 30 *_sum_DW.mrc
