

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
526  14:17  modules="gcc/9.2.0 CUDA/11.3.0 openmpi/4.1.1/gcc-9.2.0 fftw/3.3.9/openmpi-4.1.1/gcc-9.2.0 fltk/1.3.5/gcc-9.2.0"
  527  14:17  CA=60
  528  14:17  cd build/
  529  14:17  ls
  530  14:17  pwd
  531  14:18  PREFIX=/data/dout2/Programs/apps/RELION/4.0-beta-1/relion/build
  532  14:19  WRAPDIR=/usr/local/apps/RELION/wrapped/${VER}/gcc_new_${CA}
  533  14:19  pwd
  534  14:19  module purge
  535  14:20  module load $modules cmake/3.16.4
  536  14:20  export LDFLAGS="$LDFLAGS -Wl,-rpath=${LD_LIBRARY_PATH}"
  537  14:21  cmake -DCUDA_ARCH=${CA} -DCMAKE_INSTALL_PREFIX=${PREFIX} ..
  && make -j ${SLURM_CPUS_ON_NODE} 
    && make install
```
