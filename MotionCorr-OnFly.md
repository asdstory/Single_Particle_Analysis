#Login to Titan computer:
#Just ssh and use your Biowulf password.

ssh -X dout2@micefdata1.niddk.nih.gov

#Go to your data folder (the folder you want to put the image data to)

#if there is an existing "config.txt" file, backup it and then delete it (do it on micefdata1 on K2 computer)

#run Screen command in this folder

screen

# In the screen window, run following shell script:

/home/jianglab/local/align_frames/run_on_micefdata1.sh

#do following to exit screen (detach from screen)

ctrl+a+d

#If you want to attach the screen (get back to the screen), type

screen -r

#If you have multiple screen and want to switch, try

ctr+a+n or ctr+a+p

#List all the screens you have

screen -ls


##Rerence 1 : How to use screen on linux

https://hostpresto.com/community/tutorials/how-to-use-screen-on-linux/

##Reference 2

#Email from Jiansen

Hi Bertram,
 
I have updated my scripts and installed them for all users on micefdata1. Could you please put the attached shell script to a folder that is in the default search path of all users, such as '/usr/local/bin', and make it executable.
 
Huaibin, after that script is installed, users just need to run "unattended_motioncor2.sh" to start the motioncor2 script. Ask users not to run the old copy of scripts that they installed in their folders as those are already obsolete. Also ask users not to use their previous config.txt files as some options have been changed.
 
This is new and simplified protocol:
1. login to micefdata1.niddk.nih.gov
2. go to the data folder (before copying data to the folder)
3. if there is an existing "config.txt" file, backup it and then delete it (do it on micefdata1 on K2 computer)
4. run "unattended_motioncor2.sh"; a new "config.txt" file will be created automatically
5. edit "config.txt" file by uncommenting the appropriate section near the end of file (do it on micefdata1 on K2 computer) 
6. start to transfer K2 movie files to the folder
7. terminate the script when image acquisition is done

Best regards,
Jiansen