#### RELION compile on Biowulf/NIH:

```sh
Hi Tongyi,

Because of the heterogeneity of the HPC system, we compile RELION on a per-host basis.  All these executables are then modified to hard-code the paths to their required shared libraries, and then wrapped so that only the executables compiled to run on a particular node is actually run on that node.

The whole process is obscenely complicated.

Here is the most recent procedure I used to compile and install version 4.0.1:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Setup
=========================================================================
sinteractive --cpus-per-task=8 --mem-per-cpu=4g --constraint=x6140 --gres=lscratch:50
...
=========================================================================

Got new zip files
=========================================================================
cd /usr/local/src/relion
wget https://gcc02.safelinks.protection.outlook.com/?url=https%3A%2F%2Fgithub.com%2F3dem%2Frelion%2Farchive%2Frefs%2Ftags%2F4.0.1.zip&data=05%7C01%7Ctongyi.dou%40nih.gov%7C1d9e6a774a6448099a3308db815dacf1%7C14b77578977342d58507251ca2dc2b06%7C0%7C0%7C638246011561015840%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=BA0gnYHrS3QS8b%2ByVcOaZ8yEPpmWENBEsi5%2F4GkiZ44%3D&reserved=0
=========================================================================

Set variables:
=========================================================================
cat << VAR > /usr/local/src/relion/settings.sh
umask 002
module use /usr/local/apps/RELION/modules
export RELIONBASE=221113
export VER=4.0.1
export APP=relion
export SRCBASE=/usr/local/src/relion
export PREFIX=/lscratch/${SLURM_JOB_ID}/relion
export WRAPDIR=/usr/local/apps/RELION/221113
export BUILDDIR=/lscratch/${SLURM_JOB_ID}/relion-${VER}
export gv=9.2.0
export iv=2020.2.254
export cuv=11.3.0
export ov=4.1.3
export ffv=3.3.10
export flv=1.3.5
export cmv=3.16.4
export pv=0.14
VAR
=========================================================================

Built gcc and intel versions
=========================================================================
source /usr/local/src/relion/settings.sh
gcc_array=(gcc/${gv} CUDA/${cuv} openmpi/${ov}/gcc-${gv} fftw/${ffv}/gcc-${gv} fltk/${flv}/gcc-${gv})
intel_array=(intel/${iv} openmpi/${ov}/intel-${iv} fftw/${ffv}/intel-${iv} fltk/${flv}/intel-${iv})
tag_array=(35 37 60 70 80)
flag_array=(ivybridge haswell broadwell broadwell broadwell)
for i in 0 1 2 3 4 ; do
       STAGEDIR=${WRAPDIR}/${VER}/gcc_${tag_array[$i]}
       rm -rf ${PREFIX} ${BUILDDIR} ${STAGEDIR}
       cd /lscratch/${SLURM_JOB_ID}
       unzip ${SRCBASE}/${VER}.zip -d .
       cd ${BUILDDIR} && patch --unified --backup --verbose --suffix=.ORIG src/exp_model.cpp ${SRCBASE}/patches/${APP}-${VER}/src/exp_model.cpp.patch
       mkdir build && cd build && module purge && module load ${gcc_array[@]} cmake/${cmv}
       module list 2>&1 | tee -a gcc_${tag_array[$i]}.out
       ( cmake -DCUDA_ARCH=${tag_array[$i]} \
           -DCMAKE_C_FLAGS="-O3 -march=${flag_array[$i]}" \
           -DCMAKE_CXX_FLAGS="-O3 -march=${flag_array[$i]}" \
           -DCMAKE_INSTALL_PREFIX=${PREFIX} .. 2>&1 \
           && { for i in {1..5} ; do make -j ${SLURM_CPUS_ON_NODE} 2>&1 ; done } \
           && make install 2>&1 ) | tee -a gcc_${tag_array[$i]}.out
       rm -rf ${STAGEDIR} && mkdir -p ${STAGEDIR} && cd ${STAGEDIR}
       mv ${BUILDDIR}/build/gcc_${tag_array[$i]}.out $(dirname ${STAGEDIR})
       module purge >& /dev/null &&  module load ${gcc_array[@]} patchelf/${pv}
       for e in $(find ${PREFIX}/bin/ | sort); do
           if [[ -f ${e} ]]; then
               cp ${e} .
               f=$(basename $e)
               if file -b ${f} | grep -q ^ELF ; then
                   patchelf --force-rpath --set-rpath ${LD_LIBRARY_PATH} ${f}
               fi
           fi
       done
done
tag_array=("avx" "avx2" "avx512")
flag_array=("" "-xCORE-AVX2" "-xCORE-AVX512")
for i in 0 1 2 ; do
      STAGEDIR=${WRAPDIR}/${VER}/intel_${tag_array[$i]}
       rm -rf ${PREFIX} ${BUILDDIR} ${STAGEDIR}
       cd /lscratch/${SLURM_JOB_ID}
       unzip ${SRCBASE}/${VER}.zip -d .
       cd relion-${VER} && patch --unified --backup --verbose --suffix=.ORIG \
           src/exp_model.cpp ${SRCBASE}/patches/relion-${VER}/src/exp_model.cpp.patch
       mkdir build && cd build && module purge && module load ${intel_array[@]} cmake/${cmv}
       module list 2>&1 | tee intel_${tag_array[$i]}.out
       IFS=':' read -r -a array <<< "$LD_LIBRARY_PATH"
       tbblib=$(dirname $(for i in ${array[@]} ; do find $i -name libtbb.so ; done 2>/dev/null | tail -n 1 ) )
       (TBB_INSTALL_DIR=$tbblib OMPI_CC=icc OMPI_CXX=icpc LIBRARY_PATH= cmake -DALTCPU=ON -DMKLFFT=ON \
           -DCMAKE_C_COMPILER=icc -DCMAKE_CXX_COMPILER=icpc -DMPI_C_COMPILER=mpicc -DMPI_CXX_COMPILER=mpicxx \
           -DCMAKE_C_FLAGS="-O3 -ip -g -restrict ${flag_array[$i]}" \
           -DCMAKE_CXX_FLAGS="-O3 -ip -g -restrict ${flag_array[$i]}" \
           -DCMAKE_INSTALL_PREFIX=${PREFIX} .. 2>&1 \
           && { for i in {1..5} ; do make -j ${SLURM_CPUS_ON_NODE} 2>&1 ; done } \
           && make install 2>&1 ) | tee intel_${tag_array[$i]}.out
       rm -rf ${STAGEDIR} && mkdir -p ${STAGEDIR} && cd ${STAGEDIR}
       mv ${BUILDDIR}/build/intel_${tag_array[$i]}.out $(dirname ${STAGEDIR})
       module purge >& /dev/null &&  module load ${intel_array[@]} patchelf/${pv}
       for e in $(find ${PREFIX}/bin/ | sort); do
           if [[ -f ${e} ]]; then
               cp ${e} .
               f=$(basename $e)
               if file -b ${f} | grep -q ^ELF ; then
                   patchelf --force-rpath --set-rpath ${LD_LIBRARY_PATH} ${f}
               fi
           fi
       done
done
=========================================================================

And this was launched on a e7543 node
=========================================================================
sinteractive --cpus-per-task=8 --mem-per-cpu=4g --constraint=e7543 --gres=lscratch:50
...
source /usr/local/src/relion/settings.sh
gcc_array=(gcc/${gv} CUDA/${cuv} openmpi/${ov}/gcc-${gv} fftw/${ffv}/gcc-${gv} fltk/${flv}/gcc-${gv})
intel_array=(intel/${iv} openmpi/${ov}/intel-${iv} fftw/${ffv}/intel-${iv} fltk/${flv}/intel-${iv})
TAG="intel_sse4a"
STAGEDIR=${WRAPDIR}/${VER}/${TAG}
rm -rf ${PREFIX} ${BUILDDIR} ${STAGEDIR}
cd /lscratch/${SLURM_JOB_ID}
unzip -q ${SRCBASE}/${VER}.zip -d .
cd relion-${VER} && patch --unified --backup --verbose --suffix=.ORIG src/exp_model.cpp ${SRCBASE}/patches/relion-${VER}/src/exp_model.cpp.patch
mkdir build && cd build && module purge && module load ${intel_array[@]} cmake/${cmv}
module list 2>&1 | tee ${TAG}.out
IFS=':' read -r -a array <<< "$LD_LIBRARY_PATH"
tbblib=$(dirname $(for i in ${array[@]} ; do find $i -name libtbb.so ; done 2>/dev/null | tail -n 1 ) )
(TBB_INSTALL_DIR=${tbblib} OMPI_CC=icc OMPI_CXX=icpc LIBRARY_PATH= cmake -DALTCPU=ON -DMKLFFT=ON \
      -DCMAKE_C_COMPILER=icc -DCMAKE_CXX_COMPILER=icpc -DMPI_C_COMPILER=mpicc -DMPI_CXX_COMPILER=mpicxx \
      -DCMAKE_C_FLAGS="-O3 -ip -g -restrict" \
      -DCMAKE_CXX_FLAGS="-O3 -ip -g -restrict" \
      -DCMAKE_INSTALL_PREFIX=${PREFIX} .. 2>&1 \
      && { for i in {1..5} ; do make -j ${SLURM_CPUS_ON_NODE} 2>&1 ; done } \
      && make install 2>&1 ) | tee ${TAG}.out
rm -rf ${STAGEDIR} && mkdir -p ${STAGEDIR} && cd ${STAGEDIR}
mv ${BUILDDIR}/build/${TAG}.out $(dirname ${STAGEDIR})
module purge >& /dev/null &&  module load ${intel_array[@]} patchelf/${pv}
for e in $(find ${PREFIX}/bin/ | sort); do
      if [[ -f ${e} ]]; then
          cp ${e} .
          f=$(basename $e)
          if file -b ${f} | grep -q ^ELF ; then
              patchelf --force-rpath --set-rpath ${LD_LIBRARY_PATH} ${f}
          fi
      fi
done
=========================================================================

Create libexec and wrapper stuff stuff
=========================================================================
source /usr/local/src/relion/settings.sh
cd ${WRAPDIR}/${VER}
mkdir libexec && cd libexec
cat << EOF > wrapper.sh
#!/bin/bash
selfdir="\$(dirname \$(readlink -f \${BASH_SOURCE[0]}))"
up="\$(dirname \${selfdir})"
cmd="\$(basename \$0)"
if cat /proc/devices | grep -m 1 -o nvidia -q ; then
         if grep -h ^Model /proc/driver/nvidia/gpus/*/information | grep -m 1 -o K20X -q ; then
           exec "\${up}/gcc_35/\${cmd}" "\$@"
         elif grep -h ^Model /proc/driver/nvidia/gpus/*/information | grep -m 1 -o K80 -q ; then
           exec "\${up}/gcc_37/\${cmd}" "\$@"
         elif grep -h ^Model /proc/driver/nvidia/gpus/*/information | grep -m 1 -o P100 -q ; then
           exec "\${up}/gcc_60/\${cmd}" "\$@"
         elif grep -h ^Model /proc/driver/nvidia/gpus/*/information | grep -m 1 -o V100 -q ; then
           exec "\${up}/gcc_70/\${cmd}" "\$@"
         elif grep -h ^Model /proc/driver/nvidia/gpus/*/information | grep -m 1 -o A100 -q ; then
           exec "\${up}/gcc_80/\${cmd}" "\$@"
         fi
elif cat /proc/cpuinfo | grep -m 1 -o ' sse4a' -q ; then
         exec "\${up}/intel_sse4a/\${cmd}" "\$@"
elif cat /proc/cpuinfo | grep -m 1 -o ' avx512' -q ; then
         exec "\${up}/intel_avx512/\${cmd}" "\$@"
elif cat /proc/cpuinfo | grep -m 1 -o ' avx2 ' -q ; then
         exec "\${up}/intel_avx2/\${cmd}" "\$@"
else
         exec "\${up}/intel_avx/\${cmd}" "\$@"
fi
EOF
chmod a+x wrapper.sh
cd .. && mkdir bin && cd bin
d=$(dirname $(ls ${WRAPDIR}/${VER}/*/relion | head -n 1))
bd=$(basename $d)
for e in $(find ${d}/ -mindepth 1 | sort); do
      f=$(basename $e)
      if [[ -x $e ]]; then
          ln -s ../libexec/wrapper.sh $f
      else
          ln -s ../${bd}/$f $f
      fi
done
=========================================================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obviously, you will need to modify the base directories, as you don't have write permissions, and you would likely want to have it under your own control.

Let me know if you have any questions.

David

On 7/9/2023 5:34 PM, tongyi.dou@nih.gov wrote:
> 
> Hi HPC staff,
> 
> May I ask what kind of procedure we do to compile RELION on our Biowulf?  I saw we have wrapper somehow can allow compiled RELION run on different GPU/CPU nodes. Can anyone teach me how to compile my own version (I did some modifications on src).
> 
> Thanks in advance,
> 
> Tongyi Dou, Ph.D.
> 
> Biochemistry and Biophysics Center, NHLBI/NIH
> 
> 571-315-1159I Bldg. 50, Room 2150, Bethesda, MD 20892

-- 
David Hoover, Ph.D.
Computational Biologist
High Performance Computing Services,
Center for Information Technology,
National Institutes of Health
12 South Dr., Rm 2N207
Bethesda, MD 20892, USA
TEL: (+1) 301-435-2986
Email: hooverdm@hpc.nih.gov
```
### My own modified verion:
##### setting.sh:
```sh
umask 002
module use /home/dout2/Apps/modulefiles
export RELIONBASE=221113
export VER=composite_masks
export APP=relion
export SRCBASE=/home/dout2/Apps/RELION/4.0_jiang
export WRAPDIR=/home/dout2/Apps/RELION/${RELIONBASE}
export BUILDDIR=/lscratch/${SLURM_JOB_ID}/${VER}
export gv=9.2.0
export iv=2020.2.254
export cuv=11.3.0
export ov=4.1.3
export ffv=3.3.10
export flv=1.3.5
export cmv=3.23.0
export pv=0.14

```
##### build_gcc_intel_version.sh:
```sh
source /home/dout2/Apps/RELION/settings.sh
gcc_array=(gcc/${gv} CUDA/${cuv} openmpi/${ov}/gcc-${gv} fftw/${ffv}/gcc-${gv} fltk/${flv}/gcc-${gv})
intel_array=(intel/${iv} openmpi/${ov}/intel-${iv} fftw/${ffv}/intel-${iv} fltk/${flv}/intel-${iv})
tag_array=(35 37 60 70 80)
flag_array=(ivybridge haswell broadwell broadwell broadwell)
for i in 0 1 2 3 4 ; do
       STAGEDIR=${WRAPDIR}/${VER}/gcc_${tag_array[$i]}
       rm -rf ${PREFIX} ${BUILDDIR} ${STAGEDIR}
       cd /lscratch/${SLURM_JOB_ID}
       unzip ${SRCBASE}/${VER}.zip -d .
       cd ${BUILDDIR} && patch --unified --backup --verbose --suffix=.ORIG src/exp_model.cpp ${SRCBASE}/patches/${APP}-${VER}/src/exp_model.cpp.patch
       mkdir build && cd build && module purge && module load ${gcc_array[@]} cmake/${cmv}
       module list 2>&1 | tee -a gcc_${tag_array[$i]}.out
       ( cmake -DCUDA_ARCH=${tag_array[$i]} \
           -DCMAKE_C_FLAGS="-O3 -march=${flag_array[$i]}" \
           -DCMAKE_CXX_FLAGS="-O3 -march=${flag_array[$i]}" \
           -DCMAKE_INSTALL_PREFIX=${PREFIX} .. 2>&1 \
           && { for i in {1..5} ; do make -j ${SLURM_CPUS_ON_NODE} 2>&1 ; done } \
           && make install 2>&1 ) | tee -a gcc_${tag_array[$i]}.out
       rm -rf ${STAGEDIR} && mkdir -p ${STAGEDIR} && cd ${STAGEDIR}
       mv ${BUILDDIR}/build/gcc_${tag_array[$i]}.out $(dirname ${STAGEDIR})
       module purge >& /dev/null &&  module load ${gcc_array[@]} patchelf/${pv}
       for e in $(find ${PREFIX}/bin/ | sort); do
           if [[ -f ${e} ]]; then
               cp ${e} .
               f=$(basename $e)
               if file -b ${f} | grep -q ^ELF ; then
                   patchelf --force-rpath --set-rpath ${LD_LIBRARY_PATH} ${f}
               fi
           fi
       done
done
tag_array=("avx" "avx2" "avx512")
flag_array=("" "-xCORE-AVX2" "-xCORE-AVX512")
for i in 0 1 2 ; do
      STAGEDIR=${WRAPDIR}/${VER}/intel_${tag_array[$i]}
       rm -rf ${PREFIX} ${BUILDDIR} ${STAGEDIR}
       cd /lscratch/${SLURM_JOB_ID}
       unzip ${SRCBASE}/${VER}.zip -d .
       cd relion-${VER} && patch --unified --backup --verbose --suffix=.ORIG \
           src/exp_model.cpp ${SRCBASE}/patches/relion-${VER}/src/exp_model.cpp.patch
       mkdir build && cd build && module purge && module load ${intel_array[@]} cmake/${cmv}
       module list 2>&1 | tee intel_${tag_array[$i]}.out
       IFS=':' read -r -a array <<< "$LD_LIBRARY_PATH"
       tbblib=$(dirname $(for i in ${array[@]} ; do find $i -name libtbb.so ; done 2>/dev/null | tail -n 1 ) )
       (TBB_INSTALL_DIR=$tbblib OMPI_CC=icc OMPI_CXX=icpc LIBRARY_PATH= cmake -DALTCPU=ON -DMKLFFT=ON \
           -DCMAKE_C_COMPILER=icc -DCMAKE_CXX_COMPILER=icpc -DMPI_C_COMPILER=mpicc -DMPI_CXX_COMPILER=mpicxx \
           -DCMAKE_C_FLAGS="-O3 -ip -g -restrict ${flag_array[$i]}" \
           -DCMAKE_CXX_FLAGS="-O3 -ip -g -restrict ${flag_array[$i]}" \
           -DCMAKE_INSTALL_PREFIX=${PREFIX} .. 2>&1 \
           && { for i in {1..5} ; do make -j ${SLURM_CPUS_ON_NODE} 2>&1 ; done } \
           && make install 2>&1 ) | tee intel_${tag_array[$i]}.out
       rm -rf ${STAGEDIR} && mkdir -p ${STAGEDIR} && cd ${STAGEDIR}
       mv ${BUILDDIR}/build/intel_${tag_array[$i]}.out $(dirname ${STAGEDIR})
       module purge >& /dev/null &&  module load ${intel_array[@]} patchelf/${pv}
       for e in $(find ${PREFIX}/bin/ | sort); do
           if [[ -f ${e} ]]; then
               cp ${e} .
               f=$(basename $e)
               if file -b ${f} | grep -q ^ELF ; then
                   patchelf --force-rpath --set-rpath ${LD_LIBRARY_PATH} ${f}
               fi
           fi
       done
done
```

#### RELION patch with composite mask:

```sh
Hi Tongyi,

This is a simple instruction that I gave to people who requested the method I talked about in the 3DEM GRC. I hope it may also be useful for you.

I recompiled Relion 3.1 with the latest patch in Biowulf. You can use it (RELION/3.1_jiang) or compile by yourself using the attached patch. The patch should work for both Relion 3 and 4.

Best,
Jiansen



From: Jiang, Jiansen (NIH/NHLBI) [E] <jiansen.jiang@nih.gov>
Sent: Thursday, June 30, 2022 6:45 PM
To: Pinton Tomaleri, Giovani <gptomaleri@caltech.edu>
Subject: Re: [3DEM Spain] - Help with a small membrane protein
 
Hi Gio,

I'm happy to share with you the simple steps to improve the cryoEM data processing of small membrane proteins. I'm not sure if it works in all situations but let me know if it helps you or not.

I have included in this email the patch file to Relion. Go to the folder of the Relion source code (where you see src, scripts, and other subfolders) and run this command:

patch -p1 < lowpass_mask_micelle_patch_20220630.diff

And then re-compile Relion. After that, you will be able to use two new parameters in Relion: --lowpass_mask_micelle and --lowpass

Now you need to generate two masks (stepped masks): a tight soft mask that is just slightly larger than your protein (the magenta mask in the following figure) and a generous soft mask that includes both protein and detergent/lipid micelle (the grey mask in the following figure). Normally the grey mask includes the volume within the magenta mask but some regions of the magenta mask can be outside the grey mask anyway. Usually I use Chimera to segment the density of the protein and generate the magenta mask using the segmented map.


Image


Once you have done the above steps, you are ready to run Relion 3D classification or 3D auto-refine using the stepped masks.

In the "I/O" tab, use the tight (magenta) mask for the "Reference mask".


Image

In the "Running" tab, put two extra parameters in "Additional arguments":

--lowpass_mask_micelle path-to-the-grey-mask --lowpass 20

This is where the large grey mask is used. The volume within the grey mask and excluded by the magenta mask (where the detergent micelle is supposed to be) will be low-pass filtered to 20 Angstroms. You can change the low-pass filter resolution to any number. We found 20 A works well in most situations.


Image

Then click "Run" and wait for exciting results.

This works for both 3D classification and 3D refinement.

Let me know if you need further explanation or help. And I truly hope that helps.

Best,
Jiansen
```

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
PREFIX=/data/dout2/Programs/apps/RELION/ver4.0_ori
WRAPDIR=/usr/local/apps/RELION/wrapped/${VER}/gcc_new_${CA}
pwd
module purge
module load $modules cmake/3.16.4
export LDFLAGS="$LDFLAGS -Wl,-rpath=${LD_LIBRARY_PATH}"
cmake -DCUDA_ARCH=${CA} -DRELION_TEST=ON -DCMAKE_INSTALL_PREFIX=${PREFIX}  ..
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
