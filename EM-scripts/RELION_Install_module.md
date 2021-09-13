### Install instructions from: 
https://relion.readthedocs.io/en/latest/Installation.html


### 3.1.lua file setup configure:

```ssh
-- Author: Jiansen Jiang
-- Created: 12/31/2017
-- Last Updated: 12/31/2017

local version = "3.1 - GPU"
local base = "/data/jianglab-nfs/programs/apps/relion-3.1"

whatis("Name        => RELION")
whatis("Version     => " .. version)
whatis("Category    => application")
whatis("Description => RELION")
whatis("URL         => http://www2.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page")
load("CUDA/10.0")
-- load("openmpi/1.10.3/gcc-4.4.7-pmi2")
-- load("ctffind/4.0.17_jiang")
load("ctffind/4.1.13")
load("ResMap/1.1.4")
load("MotionCor2/1.2.1")

prepend_path("PATH",                   pathJoin(base,"bin"))
prepend_path("LD_LIBRARY_PATH",        pathJoin(base,"lib"))
setenv("RELION_HOME",                  base)
setenv("RELION_VERSION",               version)
setenv("RELION_QSUB_TEMPLATE",         "/usr/local/apps/RELION/batch_template_scripts/single_cpu.sh")
--setenv("RELION_CTFFIND_EXECUTABLE",    "/opt/Apps/ctffind-4.0.17/ctffind")
setenv("RELION_GCTF_EXECUTABLE",       "/usr/local/apps/RELION/Gctf_v0.50/bin/Gctf-v0.50_sm_30_cu7.5_x86_64")
setenv("RELION_UNBLUR_EXECUTABLE",     "/usr/local/apps/RELION/unblur_1.0.2/bin/unblur_openmp_7_17_15.exe")
setenv("RELION_SUMMOVIE_EXECUTABLE",   "/usr/local/apps/RELION/summovie_1.0.2/bin/sum_movie_openmp_7_17_15.exe")
--setenv("RELION_MOTIONCOR2_EXECUTABLE", "/usr/local/apps/RELION/MotionCor2/v1.0.4/MotionCor2")

setenv("RELION_QSUB_EXTRA1","Local Scratch Disk Space")
setenv("RELION_QSUB_EXTRA1_DEFAULT","200")
setenv("RELION_QSUB_EXTRA2","Walltime")
setenv("RELION_QSUB_EXTRA2_DEFAULT","5-00:00:00")
setenv("RELION_QSUB_EXTRA3","Memory Per Thread")
setenv("RELION_QSUB_EXTRA3_DEFAULT","8g")

-- For evince, shmeesh
-- prepend_path("PATH","/usr/local/apps/RELION/xpdf_wrapper/")

```
