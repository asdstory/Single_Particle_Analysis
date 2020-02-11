generalbn=1...._sum    #input the general basename of origin mrc file, in which . represent a letter or digit
binn=6    #input the bin number will be done on the mrc and fft
MagPixel=1.07   #Pixel size
apixbin=`echo "$MagPixel*$binn"|bc`   #Actual pixel size after binned 

#Use ctffind4 to creat the ctf files, then link the *_pow.ctf and *_pow.txt files here

#Creat a .sh file (step1), run which will merge CTF parameter, then manually discard the images with bad CTF parameters (defocus & stigmator)
echo -e "#Firstly run this .sh file, then using sort command to show the ctf parameters and discard the bad images\n\n#Type sort command as:\n#sort -nk 2 2.ctfparm\n#for a in \`cut -c 1-7\`;do mv \$a* ctfparm_discarded;done (press enter)\n#select the lines defocus >3, control C + control V (press enter)\n#control + D\n\n#Use same method, dsicard all bad parameters including:\n#sort -r -nk 2 2.ctfparm [discard defocus < 1.2]\n#sort -nk 2 3.ctfparm [discard stigmator >10]\n#sort -r -nk 2 3.ctfparm\n#sort -r -nk 5 3.ctfparm [discard defocus fit range< 6]\n""\`mkdir ctfparm_discarded\`\nfor a in *pow.txt;do echo \$a \`tail -n 1 \$a\`|awk -F\" \" '{print \$1\" \"\$3\" \"\$4\" \"\$5\" \"\$6\" \"\$7*100\" \"\$8}';done > 1.ctfparm\n""awk '{print \$1\" \"sqrt(\$2*\$3)/10000}'<1.ctfparm >2.ctfparm\n""awk '{print \$1\" \"(sqrt((\$2-\$3)*(\$2-\$3))/(\$2+\$3)*2*100)\" \"\$5\" \"\$6\" \"\$7}' < 1.ctfparm >3.ctfparm\n">>step1_ctfpara_selection.sh

#Creat a runparfile (step2), runpar which will prepare binned  mrc
for i in `ls 1*.mrc` #only for the origin *.mrc, Do Not includ the *_pow.mrc.
do
bn=`basename $i .mrc`
echo -e "cd `pwd`;""sampilcopy2d.py $i $i single 0,0,A${binn},0">>step2_runpar_prepare_hed.par
done

#Creat a .sh file (step3), run wchih will creat the all_mrc.hed
echo -e "for j in *_bin${binn}.mrc\n""do\n""bnmrc=\`basename \$j _bin${binn}.mrc\`\n""proc2d \$j all_mrc.hed apix=$apixbin lp=[15] hp=[400] comment=\$bnmrc\n""done\n">>step3_creat_all_mrc_hed.sh

#Then, manually select good mrc, and save as good_mrc.hed (if save several times, change save name and then change back to good_mrc.hed, do not overwrite directly).
#Use ctffind4 to creat the ctf files, then link the *_pow.ctf file here

#Creat a .sh file (step4), run which will creat a temp_ctf.hed, which contain the ctf (*_pow.ctf) of the images in good_mrc.hed
echo -e "#The search content, such as '1...._sum', is from the prfix of origin mrc files, change it if necessary\n""#creat a temp_ctf.hed, which contain the ctf (*pow.ctf) of the mrc in good_mrc.hed\n""for bnctf in \`grep -a -o '$generalbn' good_mrc.hed\`\n""do\n""proc2d \${bnctf}_pow.ctf temp_ctf.hed comment=\$bnctf\n""done">>step4_creat_temp_ctf_hed.sh

#Then, manually select good cft images from temp_ctf.hed, and save as good_ctf.hed (if save several times, change name and then change back to good_ctf.hed, do not overwrite directly).

#Creat a .sh file (step5), run which will output the mrc link to a dir final_images, and creat a good image list
echo -e "#Creat a dir final_images, and link the mrc in good_ctf.hed in it\n""#search content '1...._sum' is from the prfix of origin mrc, change it if necessary\n""\`mkdir final_images\`\n""cd final_images\n""for bnfinal in \`grep -a -o '$generalbn' ../good_ctf.hed\`\n""do\n""ln -s ../\${bnfinal}.mrc .\n""echo \${bnfinal}.mrc>>final.list\n""done">>step5_output_links.sh 
