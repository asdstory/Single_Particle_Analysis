#!/bin/tcsh -f

#####**************************************************************************#####
#Despcription: This program is used to make Relion star file from gctf or ctffind3 log.
#Copyright@MRC-LMB
#Author: Kai Zhang
#Last Edit: 2014-5-11
#####**************************************************************************#####

#global setup for output format
set KBold="\x1b\x5b1m"
set KDefault="\x1b\x5b0m"
set KUnderline="\x1b\x5b4m"
set KFlash="\x1b\x5b5m"

#end of global setup


set args = ${#argv}

set Proc_name=`echo $0 | awk '{n=split($1,scr,"/");print scr[n];}'`

if ( $args <= 1 || $1 == '--help' || $1 == '-h' ) then


        printf "${KBold}Despcription: ${KDefault}This program is used to make Relion star file from Gctf or ctffind3 log..\n"
        printf "${KBold}Usage:${KDefault}   $Proc_name <micrographs*.mrc> \n"
        printf "${KBold}example:${KDefault} $Proc_name  Micrographs/Falcon*.mrc \n"
        printf "${KBold}example:${KDefault} $Proc_name  Micrographs/Falcon*_gctf.log \n"

        exit(1)
endif

set all_micrographs="${argv}"
set gctf_star=all_micrographs_gctf.star

###################################################################
echo "" > $gctf_star
echo "data_" >> $gctf_star
echo "" >> $gctf_star
echo "loop_" >> $gctf_star
echo "_rlnMicrographName #1" >> $gctf_star
echo "_rlnCtfImage #2" >> $gctf_star
echo "_rlnDefocusU #3" >> $gctf_star
echo "_rlnDefocusV #4" >> $gctf_star
echo "_rlnDefocusAngle #5" >> $gctf_star
echo "_rlnVoltage #6" >> $gctf_star
echo "_rlnSphericalAberration #7" >> $gctf_star
echo "_rlnAmplitudeContrast #8" >> $gctf_star
echo "_rlnMagnification #9" >> $gctf_star
echo "_rlnDetectorPixelSize #10" >> $gctf_star
echo "_rlnCtfFigureOfMerit #11" >> $gctf_star

foreach mrcf ($all_micrographs)
#<<< foreach 1001
#set rootN=`echo $mrcf | gawk '//{print length($1) - 4 }'`
#set root=`echo $mrcf |cut -c 1-${rootN}`

set root1=`echo $mrcf |sed 's/.mrc//g' `
set root2=`echo $mrcf |sed 's/_gctf.log//g' `
set root3=`echo $mrcf |sed 's/_ctffind3.log//g' `

if ( $mrcf == ${root1}.mrc ) then
set root=${root1}
else if ( $mrcf == ${root2}_gctf.log ) then
set root=${root2}
else if ( $mrcf == ${root3}_ctffind3.log ) then
set root=${root3}
endif

set ctflog=${root}_gctf.log
#echo "$ctff $ctflog"
if ( ! -f $ctflog || -z $ctflog ) then

set ctflog=${root}_ctffind3.log
if ( ! -f $ctflog || -z $ctflog ) then

echo "Warning: ${root}_gctf.log or ${root}_ctffind3.log  does not exist or empty! Escaping it."

continue
endif

endif

set EM_para=`grep -a -A 1 "AmpCnst" $ctflog | awk '{if(NR==2)print}'`
#echo "EM_para $EM_para"

set Defocus=`awk '/Final Values/{print}' $ctflog`
#echo "Defocus $Defocus"
set rlnDefocusU=$Defocus[1]
set rlnDefocusV=$Defocus[2]
set rlnDefocusAngle=$Defocus[3]
set rlnVoltage=$EM_para[2]
set rlnSphericalAberration=$EM_para[1]
set rlnAmplitudeContrast=$EM_para[3]
set rlnMagnification=$EM_para[4]
set rlnDetectorPixelSize=$EM_para[5]

if ( "$ctflog" == ${root}_gctf.log || "$ctflog" == ${root}_ctffind3.log ) then
set rlnCtfFigureOfMerit=$Defocus[4]
set ctff=${root}.ctf
set rlnCtfImage="${ctff}:mrc"


else 
echo "Warning: ${root}_gctf.log or ${root}_ctffind3.log  does not exist! Escaping it."

endif

printf "%s %s %12.6f %12.6f %12.6f %12.6f %12.6f %12.6f %12.6f %12.6f %12.6f\n" ${root}.mrc $rlnCtfImage $rlnDefocusU $rlnDefocusV $rlnDefocusAngle $rlnVoltage $rlnSphericalAberration $rlnAmplitudeContrast $rlnMagnification $rlnDetectorPixelSize $rlnCtfFigureOfMerit  >> $gctf_star

echo "$mrcf $rlnCtfImage $rlnDefocusU $rlnDefocusV $rlnDefocusAngle $rlnVoltage $rlnSphericalAberration $rlnAmplitudeContrast $rlnMagnification $rlnDetectorPixelSize $rlnCtfFigureOfMerit"
end
#>>> foreach 1001

exit
