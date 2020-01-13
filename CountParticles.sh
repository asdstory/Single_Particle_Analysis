# Count Particles from the .star file.

#This script is used when we want to know how many particles left after we do subset selection, e.g. after we perform sorting particles and subset select by the ZScore.

#When run this script, please do not use "sh", use "bash" instead. sh and bash are two different shells. While in the first case you are passing your script as an argument to the sh interpreter, in the second case you decide on the very first line which interpreter will be used.

- [ ] bash CountParticles.sh 

******************************************
#!/bin/bash

input="particles.star"
i=0
while IFS= read -r line
do
#  echo "$line"
    echo i: $i
    if [[ $line =~ \@  ]]; then
        i=$(( i+1  ))
    fi
done < "$input"
echo Total particles selected: $i 

#$ cat myscript
##!/bin/bash
#echo "First arg: $1"
#echo "Second arg: $2"
#$ ./myscript hello world
#First arg: hello
#Second arg: world
******************************************
