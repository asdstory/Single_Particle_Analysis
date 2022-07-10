

#### Instructions from Wolfgang/HPC/NIH:
```sh
This example uses stock relion so modify to use your own source dir
    instead of a github tag


    modules="gcc/9.2.0 CUDA/11.3.0 openmpi/4.1.1/gcc-9.2.0 fftw/3.3.9/openmpi-4.1.1/gcc-9.2.0 fltk/1.3.5/gcc-9.2.0"
    CA=60
    PREFIX=/path/to/where/you/want/to/install
    WRAPDIR=/usr/local/apps/RELION/wrapped/${VER}/gcc_new_${CA}

    cd /lscratch/${SLURM_JOB_ID}
    rm -rf relion
    git clone https://gcc02.safelinks.protection.outlook.com/?url=https%3A%2F%2Fgithub.com%2F3dem%2Frelion.git&amp;data=05%7C01%7Ctongyi.dou%40nih.gov%7C9713c232783c4193672108da50858b7b%7C14b77578977342d58507251ca2dc2b06%7C0%7C0%7C637910831758829619%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&amp;sdata=yeR5rBSZrAhhNsmVH6jDTiZMnyL8riuyRetF0GrFgpg%3D&amp;reserved=0
    cd relion
    git checkout ver4.0

    mkdir build \
    && cd build \
    && module purge \
    && module load $modules cmake/3.16.4

    export LDFLAGS="$LDFLAGS -Wl,-rpath=${LD_LIBRARY_PATH}"
    cmake -DCUDA_ARCH=${CA} -DCMAKE_INSTALL_PREFIX=${PREFIX} .. \
    && make -j ${SLURM_CPUS_ON_NODE} \
    && make install

    $PREFIX/bin/relion --help
```

#### The version I modified
```sh 
modules="gcc/9.2.0 CUDA/11.3.0 openmpi/4.1.1/gcc-9.2.0 fftw/3.3.9/openmpi-4.1.1/gcc-9.2.0 fltk/1.3.5/gcc-9.2.0"
CA=60
PREFIX=/data/dout2/Programs/apps/RELION/relion/4.0-beta-1
WRAPDIR=/usr/local/apps/RELION/wrapped/${VER}/gcc_new_${CA}
pwd
module purge
module load $modules cmake/3.16.4
export LDFLAGS="$LDFLAGS -Wl,-rpath=${LD_LIBRARY_PATH}"
cmake -DCUDA_ARCH=${CA} -DCMAKE_INSTALL_PREFIX=${PREFIX} ..
  && make -j ${SLURM_CPUS_ON_NODE}
  && make install

  $PREFIX/bin/relion --help
```


#### ver4.0.lua file
```sh
[dout2@biowulf RELION]$ more ver4.0.lua 
local description = "http://www2.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page"
local version     = myModuleVersion() 
local app         = myModuleName()
local base        = "/usr/local/apps/"
local helpmessage = "Sets up "..app.." "..version.." on helix/biowulf cluster" 
local hostname    = capture("/bin/hostname")
hostname          = hostname:gsub("%s+", "")
local relionbase  = "wrapped-openmpi/ver4.0"

if (hostname == "biowulf.nih.gov") then

-- R should not run on the biowulf head node
   LmodError( [[

------------------------------------------------------
Running RELION is NOT allowed on the Biowulf login node.
Please submit a batch job, or allocate an interactive
node. See http://hpc.nih.gov/apps/relion for
information on using RELION on Biowulf.

For an interactive session, at the prompt, type

   sinteractive
------------------------------------------------------

]] )
end

conflict("Chimera")

help(helpmessage)
whatis(description)
whatis("Version " .. version)

if (mode() == "load") then
    LmodMessage("[+] Loading",app,version,"on",hostname)
end
if (mode() == "unload") then
    LmodMessage("[-] Unloading",app,version,"on",hostname)
end

-- This is needed to allow interactive srun/mpirun
unsetenv("SLURM_TASKS_PER_NODE")
unsetenv("SLURM_MEM_PER_NODE")
unsetenv("SLURM_MEM_PER_CPU")

-- Stuff for OpenMPI
--setenv('OMPI_MCA_btl_openib_allow_ib','1')
--setenv('OMPI_MCA_pml','ucx')
--setenv('OMPI_MCA_btl','^openib')

-- Stuff for MVAPICH2
--setenv("MV2_USE_RDMA_CM","1")
--setenv("MV2_USE_RoCE","1")
--setenv("MV2_RAIL_SHARING_POLICY","FIXED_MAPPING")

load("CUDA/11.3.0")
load("ctffind/4.1.14")
load("ResMap/1.1.4")
load("MotionCor2/1.3.0")
load("Ghostscript/9.22")
load("Gctf/1.06")
load("xpdf")
load("tex")
load("topaz/0.2.5")

prepend_path("PATH",                   pathJoin(base,app,relionbase,"bin"))
prepend_path("PATH",                   pathJoin(base,app,"utils"))

setenv("RELION_HOME",                  pathJoin(base,app,relionbase))
setenv("RELION_VERSION",               "4.0-beta-1")

setenv("RELION_ERROR_LOCAL_MPI",       "32")

setenv("RELION_QUEUE_USE",             "No")
setenv("RELION_QSUB_COMMAND",          "sbatch")
setenv("RELION_QUEUE_NAME",            "norm")

setenv("RELION_STD_LAUNCHER",          "srun --mpi=pmix")
setenv("RELION_MPIRUN",                "srun --oversubscribe --mpi=pmix")

setenv("RELION_QSUB_NRMPI",            "32")
setenv("RELION_MPI_MAX",               "2000")

setenv("RELION_QSUB_NRTHREADS",        "1")
setenv("RELION_THREAD_MAX",            "16")
setenv("RELION_SCRATCH_DIR",           "/lscratch/$SLURM_JOB_ID")

setenv("RELION_QSUB_EXTRA_COUNT",      "6")
setenv("RELION_QSUB_TEMPLATE",         pathJoin(base,app,"templates/common.sh"))
setenv("RELION_QSUB_EXTRA1",           "Walltime")
setenv("RELION_QSUB_EXTRA1_DEFAULT",   "1-00:00:00")
setenv("RELION_QSUB_EXTRA2",           "Memory Per Thread")
setenv("RELION_QSUB_EXTRA2_DEFAULT",   "8g")
setenv("RELION_QSUB_EXTRA3",           "Gres")
setenv("RELION_QSUB_EXTRA3_DEFAULT",   "lscratch:400")
setenv("RELION_QSUB_EXTRA4",           "Addl (ex4) SBATCH Directives")
setenv("RELION_QSUB_EXTRA4_DEFAULT",   "")
setenv("RELION_QSUB_EXTRA5",           "Addl (ex5) SBATCH Directives")
setenv("RELION_QSUB_EXTRA5_DEFAULT",   "")
setenv("RELION_QSUB_EXTRA6",           "Addl (ex6) SBATCH Directives")
setenv("RELION_QSUB_EXTRA6_DEFAULT",   "")

setenv("RELION_MINIMUM_DEDICATED",     "1")
setenv("RELION_PDFVIEWER_EXECUTABLE",  "xpdf")

```

#### The .lua file I modified:

```sh
[dout2@biowulf RELION]$ cat ver4.0.TYD.lua 
local description = "http://www2.mrc-lmb.cam.ac.uk/relion/index.php/Main_Page"
local version     = myModuleVersion() 
local app         = myModuleName()
local base        = "/data/dout2/Programs/apps"
local helpmessage = "Sets up "..app.." "..version.." on helix/biowulf cluster" 
local hostname    = capture("/bin/hostname")
hostname          = hostname:gsub("%s+", "")
local relionbase  = "relion/4.0-beta-1"

if (hostname == "biowulf.nih.gov") then

-- R should not run on the biowulf head node
   LmodError( [[

------------------------------------------------------
Running RELION is NOT allowed on the Biowulf login node.
Please submit a batch job, or allocate an interactive
node. See http://hpc.nih.gov/apps/relion for
information on using RELION on Biowulf.

For an interactive session, at the prompt, type

   sinteractive
------------------------------------------------------

]] )
end

conflict("Chimera")

help(helpmessage)
whatis(description)
whatis("Version " .. version)

if (mode() == "load") then
    LmodMessage("[+] Loading",app,version,"on",hostname)
end
if (mode() == "unload") then
    LmodMessage("[-] Unloading",app,version,"on",hostname)
end

-- This is needed to allow interactive srun/mpirun
unsetenv("SLURM_TASKS_PER_NODE")
unsetenv("SLURM_MEM_PER_NODE")
unsetenv("SLURM_MEM_PER_CPU")

-- Stuff for OpenMPI
--setenv('OMPI_MCA_btl_openib_allow_ib','1')
--setenv('OMPI_MCA_pml','ucx')
--setenv('OMPI_MCA_btl','^openib')

-- Stuff for MVAPICH2
--setenv("MV2_USE_RDMA_CM","1")
--setenv("MV2_USE_RoCE","1")
--setenv("MV2_RAIL_SHARING_POLICY","FIXED_MAPPING")

load("CUDA/11.3.0")
load("ctffind/4.1.14")
load("ResMap/1.1.4")
load("MotionCor2/1.3.0")
load("Ghostscript/9.22")
load("Gctf/1.06")
load("xpdf")
load("tex")
load("topaz/0.2.5")

prepend_path("PATH",                   pathJoin(base,app,relionbase,"bin"))
prepend_path("PATH",                   pathJoin(base,app,"utils"))

setenv("RELION_HOME",                  pathJoin(base,app,relionbase))
setenv("RELION_VERSION",               "4.0-beta-1")

setenv("RELION_ERROR_LOCAL_MPI",       "32")

setenv("RELION_QUEUE_USE",             "No")
setenv("RELION_QSUB_COMMAND",          "sbatch")
setenv("RELION_QUEUE_NAME",            "norm")

setenv("RELION_STD_LAUNCHER",          "srun --mpi=pmix")
setenv("RELION_MPIRUN",                "srun --oversubscribe --mpi=pmix")

setenv("RELION_QSUB_NRMPI",            "32")
setenv("RELION_MPI_MAX",               "2000")

setenv("RELION_QSUB_NRTHREADS",        "1")
setenv("RELION_THREAD_MAX",            "16")
setenv("RELION_SCRATCH_DIR",           "/lscratch/$SLURM_JOB_ID")

setenv("RELION_QSUB_EXTRA_COUNT",      "6")
setenv("RELION_QSUB_TEMPLATE",         pathJoin(base,app,"templates/common.sh"))
setenv("RELION_QSUB_EXTRA1",           "Walltime")
setenv("RELION_QSUB_EXTRA1_DEFAULT",   "1-00:00:00")
setenv("RELION_QSUB_EXTRA2",           "Memory Per Thread")
setenv("RELION_QSUB_EXTRA2_DEFAULT",   "8g")
setenv("RELION_QSUB_EXTRA3",           "Gres")
setenv("RELION_QSUB_EXTRA3_DEFAULT",   "lscratch:400")
setenv("RELION_QSUB_EXTRA4",           "Addl (ex4) SBATCH Directives")
setenv("RELION_QSUB_EXTRA4_DEFAULT",   "")
setenv("RELION_QSUB_EXTRA5",           "Addl (ex5) SBATCH Directives")
setenv("RELION_QSUB_EXTRA5_DEFAULT",   "")
setenv("RELION_QSUB_EXTRA6",           "Addl (ex6) SBATCH Directives")
setenv("RELION_QSUB_EXTRA6_DEFAULT",   "")

setenv("RELION_MINIMUM_DEDICATED",     "1")
setenv("RELION_PDFVIEWER_EXECUTABLE",  "xpdf")

```

#### echo $PATH after module load RELION/4.0_lp
```sh
/data/dout2/Programs/apps/RELION/utils:/data/dout2/Programs/apps/RELION/ver4.0_lp/bin:/usr/local/apps/topaz/0.2.5/bin:/usr/local/current/singularity/3.8.5-1/bin:/usr/local/apps/texlive/latex2rtf-2.3.17:/usr/local/apps/texlive/2022/bin/x86_64-linux:/usr/local/apps/xpdf/4.04/bin:/usr/local/apps/Gctf/1.06/bin:/usr/local/Ghostscript/9.22/bin:/usr/local/apps/MotionCor2/1.3.0:/usr/local/apps/ResMap/1.1.4:/usr/local/apps/ctffind/4.1.14:/usr/local/CUDA/11.3.0/bin:/usr/local/slurm/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/X11R6/bin:/usr/local/jdk/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/mysql/bin:/home/dout2/.local/bin:/home/dout2/bin:/opt/ibutils/bin

```

#### echo $PATH 
```sh
/usr/local/apps/RELION/utils:/usr/local/apps/RELION/wrapped-openmpi/ver4.0/bin:/usr/local/apps/topaz/0.2.5/bin:/usr/local/current/singularity/3.8.5-1/bin:/usr/local/apps/texlive/latex2rtf-2.3.17:/usr/local/apps/texlive/2022/bin/x86_64-linux:/usr/local/apps/xpdf/4.04/bin:/usr/local/apps/Gctf/1.06/bin:/usr/local/Ghostscript/9.22/bin:/usr/local/apps/MotionCor2/1.3.0:/usr/local/apps/ResMap/1.1.4:/usr/local/apps/ctffind/4.1.14:/usr/local/CUDA/11.3.0/bin:/usr/local/slurm/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/X11R6/bin:/usr/local/jdk/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/mysql/bin:/home/dout2/.local/bin:/home/dout2/bin:/opt/ibutils/bin

```
