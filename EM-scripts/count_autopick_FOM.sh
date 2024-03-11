# Count Particles from Autopick, with FOM threshold. 

# This script is used to determine the best FOM threshold for particle extraction jobs.


#!/bin/bash

declare -i c;
c=0;
FOM=$1;
echo $FOM

for i in *_autopick.star;
#  do echo $i;
  do
  function count() { awk -v FOM=$FOM '$3+0 >= FOM+0 { count++ } END {print count}'  "$1"; };
#  function count() {     awk '$3+0 >= 10 { count++ } END {print count}'  "$1"; };
  c+=$(count $i);
done

echo Total particles selected: $c

# awk '$3+0 >= 10 { count++ } END {print count}  ' FoilHole_266910_Data_255258_255260_20240301_193301_Fractions_autopick.star


#input="particles.star"
#i=0
#while IFS= read -r line
#do
#  if [[ $line =~ \@ ]]; then
#      i=$(( i+1 ))
#  fi
#done < "$input"

#echo Total particles selected: $i

# count=0; for i in *_autopick.star; do awk '$3 >= 2' $i;  

