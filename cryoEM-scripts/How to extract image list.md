## This shows how to extract image list from the imported movies.star file:

- [ ] awk 'BEGIN {FS = "/" }; {print $2 >> image_list.txt} ' movies.star
- [ ] awk -F/ 'print $2 >> image_list.txt' movies.star
