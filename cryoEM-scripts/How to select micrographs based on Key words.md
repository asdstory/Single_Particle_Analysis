# For examples, we only want the 202003 batch micrographs to be used in further data processing, we can do:

- For RELION 3.0:
- [ ] awk -e 'NR <= 18 {print $0 > "micrographs_ctf_selected.star"} NR >18 && $1 ~ /202003/ {print $0 >> "micrographs_ctf_selected.star"}' micrographs_ctf.star
