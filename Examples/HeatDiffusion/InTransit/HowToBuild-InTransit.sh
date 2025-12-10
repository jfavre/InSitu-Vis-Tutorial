uenv start paraview/6.0.1:2191677242 --view=default
spack load adios2 

git clone https://gitlab.kitware.com/vtk/fides.git

cmake -S fides -B fides-adios2.11Build \
  -DCMAKE_CXX_COMPILER=c++ -DCMAKE_C_COMPILER=gcc \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=`pwd`/fides-adios2.11-install \
  -DViskores_DIR=/capstor/scratch/cscs/jfavre/Viskores-build/lib/cmake/viskores-1.1 \
  -DFIDES_ENABLE_EXAMPLES=OFF -DFIDES_ENABLE_TESTING=OFF

cmake --build fides-adios2.11Build -j8 --target install

cmake -B buildSSTConsumer -S . \
  -DCMAKE_BUILD_TYPE=Release \
  -DFides_DIR=`pwd`/fides-adios2.11-install/lib/cmake/fides \
  -DViskores_DIR=/capstor/scratch/cscs/jfavre/Viskores-build/lib/cmake/viskores-1.1

cmake --build buildSSTConsumer
 
# First run. Classic output to an ADIOS BP file
# make sure adios2.xml contains the string <engine type="BP4">
 
python3 heat_diffusion_insitu_serial.py 

bpls -la diffusion.bp

# Second run. In transit transfer to a data consumer

# make sure adios2.xml contains the string <engine type="SST">

rm -rf diffusion.bp
python3 heat_diffusion_insitu_serial.py &

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/capstor/scratch/cscs/jfavre/Viskores-build/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`spack location -i adios2`/lib
./buildSSTConsumer/fides-sst-reader
# view images
eog diffusion*png

