# ***********************************************
# WARNING!!!
# Don't change the values in the default section.
# These values will be used if you don't have a correct personal section or don't define them in your personal section.
# The number of frames is zero-based (starting from 0).
# ***********************************************

[default]
# *** Basic options ***
align_program = MotionCor2      ; Backend program for drift correction. Options: MotionCor2 and dosefgpu_driftcorr;
sum_start_frame = 0             ; The first frame for the average images.
sum_end_frame = 0               ; The last frame for the low-dose average image (0 disables this option). The average of all frames is always generated (*_all_frames.mrc) when dosefgpu_driftcorr is used.
sum_bin = 1                     ; Binning. It can be decimal (e.g. 1.5x binning). 1x binning is used by default, assuming super-resolution images are acquired.
gain_reference =                ; Gain reference image. Gain reference is not used by default. Uncomment either of the following options to use a proper gain reference image. Or you can specify your own gain reference image (use absolute path).
#gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_7420x7676_norm_latest.mrc      ; Gain reference image (super-resolution mode).
#gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc      ; Gain reference image (counting mode).
defect_map =                    ; Defect map image (0 for normal pixels and 1 for bad pixels).

# *** MotionCor2 specific options ***
patch = 5                       ; Number of patches (N by N) to be used for patch based alignment. Use 0 if you need to disable patch based alignment.
iter = 10                       ; Maximum iterations for iterative alignment.
group = 1                       ; Group specified number of frames by adding them together before alignment. Use 1 if no grouping is needed.
pixsize = 1.06                  ; Pixel size (in Angstrom) of the input movie frames. Caution: pixel sizes of the counting and super-resolution modes are different!
dose_per_pixel_second = 8       ; Number of electrons per pixel per second. Normally, we use 8 e-/pix/s for the counting mode and 2 e-/pix/s for the super-resolution mode.
exposure_time_per_frame = 200   ; Exposure time (in mini-seconds) of each movie frame, e.g. 250 for 4 frames per second.
combine_gpu = 0                 ; Don't change this!
program_motioncor2 =            ; The absolute path to the MotionCor2 program. Do not change it unless you really have to use you own version of MotionCor2.

# *** Advanced options ***
additional_options =            ; These additional parameters will be passed to MotionCor2 or dosefgpu_driftcorr directly. Check the options of MotionCor2 or dosefgpu_driftcorr. Use with caution: the program will stop working if any incorrect paramete
r is used.

# The default section ends
#################################################

# Sections for personal settings starts here.
# Format of the section header:
# [YYYY-MM-DD-HH-MM-username]
# The section header will be used as the folder name to store aligned average images and the raw frame data.
# Make sure the time stamp is in the correct format.
# Raw frame stacks with a creation time newer than the time stamp will be aligned using the settings in the personal section.
# Copy necessary options from the default section and modify them accordingly.

#################################################

# Uncomment and modify any of these sections that best fits your imaging parameters.

# Image acquisition with Leginon; counting mode on K2
[2020-03-30-00-00-MavN_EDTA-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-04-04-10-00-MavN_CaCl2-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-04-16-10-00-MavN_purple-box-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-04-27-10-00-OAT1_stick1965-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-04-27-16-00-PnuC_3Nano2.7-leginon-counting]
sum_bin = 1
pixsize = 0.83
dose_per_pixel_second = 5.9
exposure_time_per_frame = 125
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-05-01-18-00-PnuC_25NR_C8-leginon-counting]
sum_bin = 1
pixsize = 0.83
dose_per_pixel_second = 5.9
exposure_time_per_frame = 125
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-05-01-21-00-PnuC_25NR_C8-130k-mag-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-05-25-00-00-apo-Patched-130k-mag-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 6.8
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-06-22-17-00-Bor1_borate-leginon-counting]
sum_bin = 1
pixsize = 0.83
dose_per_pixel_second = 5.0
exposure_time_per_frame = 125
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-07-20-15-00-UAC-NAM_rod-1986_image-shift-leginon-counting]
sum_bin = 1
pixsize = 0.83
dose_per_pixel_second = 6.0
exposure_time_per_frame = 125
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-07-24-16-00-Patched-SMO-rod-137-130k-mag-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8.0
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc

[2020-08-20-00-00-SMO-nanobody-130k-mag-leginon-counting]
sum_bin = 1
pixsize = 1.06
dose_per_pixel_second = 8.0
exposure_time_per_frame = 200
gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_norm_latest.mrc
defect_map = /home/jianglab/local/align_frames/micef_krios_k2_3710x3838_defect_latest.mrc




# Image acquisition with Leginon; super-resolution mode on K2
#[2020-03-30-14-13-YourSampleName-leginon-superres]
#sum_bin = 2
#pixsize = 0.53
#dose_per_pixel_second = 2
#exposure_time_per_frame = 200
#gain_reference = /home/jianglab/local/align_frames/micef_krios_k2_7420x7676_norm_latest.mrc
#defect_map = /home/jianglab/local/align_frames/micef_krios_k2_7420x7676_defect_latest.mrc

# Image acquisition with SerialEM; counting mode on K2
#[2020-03-30-14-13-YourSampleName-serialem-counting]
#sum_bin = 1
#pixsize = 1.06
#dose_per_pixel_second = 8
#exposure_time_per_frame = 200

# Image acquisition with SerialEM; super-resolution mode on K2
#[2020-03-30-14-13-YourSampleName-serialem-superres]
#sum_bin = 2
#pixsize = 0.53
#dose_per_pixel_second = 2
#exposure_time_per_frame = 200
