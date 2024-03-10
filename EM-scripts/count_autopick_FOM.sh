# Count Particles from Autopick, with FOM threshold. 

# This script is used to determine the best FOM threshold for particle extraction jobs.

count=0; for i in *_autopick.star; do awk '$3 >= 2' $i;  
