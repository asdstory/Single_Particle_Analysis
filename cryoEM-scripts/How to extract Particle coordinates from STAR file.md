## cd to folder that contains particles.star, and type: 

```
awk 'NR>34 {print $1 " "  $2 >> "particleXY.star"}' particles.star
```
