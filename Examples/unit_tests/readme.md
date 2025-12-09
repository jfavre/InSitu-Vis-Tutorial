# Ascent unit tests

## Setup the environment (daint):

```sh
uenv start -v default /capstor/store/cscs/cscs/public/uenvs/ascent/daint.sqfs
uenv status
cd ./InSitu-Vis-Tutorial.git/Examples/unit_tests/

# get the src code:
git clone --depth 1 --branch v0.9.5 \
    https://github.com/Alpine-DAV/ascent.git ascent.git
cd ascent.git ; git switch -c v0.9.5 ; cd ..

cp -a alps/ascent.git/* ascent.git/
sed -i "s@_PWD_@$PWD@" ascent.git/src/tests/t_config.hpp
```

## Build with:

```
cmake -S ascent.git/src/tests/ascent \
-B build_v095 \
-DAscent_DIR=$(find /user-tools/ -name ascent | grep ascent- | grep cmake) \
-DCMAKE_CUDA_ARCHITECTURES=90

cmake --build build_v095 -j
```

## Run BASIC_TESTS with:

```
cd build_v095/
export OMP_NUM_THREADS=1
for ii in $(ls -1 t_ascent_* |grep  -v _mpi_) ;do echo "(mkdir -p _$ii; cd _$ii ; ../$ii &> o ;cd .. ;echo $ii) &" ;done |sh
# ps x |grep t_ascent |wc -l
```

### Check the results (daint):

```
# grep -m1 FAILED _t_ascent_*/o

_t_ascent_derived/o:[  FAILED  ] in conduit::utils::conduit_memcpy_strided_elements
    ./t_ascent_derived --gtest_list_tests # ascent_expressions.derived_simple / OCCA cuda kernel
    ./t_ascent_derived --gtest_filter=ascent_expressions.derived_simple


_t_ascent_failed_pipeline/o:[  FAILED  ] in diff_image
    [  FAILED  ] ascent_pipeline_failure.test_partial_failure

_t_ascent_gradient/o:[  FAILED  ] in diff_image
    [  FAILED  ] ascent_gradient.test_gradient_radial

_t_ascent_particle_advection/o:[  FAILED  ] -> needs `mkdir ./_output`

_t_ascent_render_3d/o:[  FAILED  ] in diff_image
    [  FAILED  ] ascent_render_3d.test_render_3d_original_bounds
    [  FAILED  ] ascent_render_3d.test_render_3d_multi_render_default_runtime
    [  FAILED  ] ascent_render_3d.test_render_3d_multi_render_mesh

_t_ascent_rover/o:[  FAILED  ] differences in the blueprint diff:
    [  FAILED  ] ascent_rover.test_xray_blueprint_braid
    [  FAILED  ] ascent_rover.test_xray_blueprint_braid_absorption_only

_t_ascent_slice/o:[  FAILED  ] in diff_image
    [  FAILED  ] ascent_slice.test_exaslice

_t_ascent_uniform_grid/o:[  FAILED  ] in diff_image
    [  FAILED  ] ascent_uniform_regular_grid.test_uniform_grid_equal_size_input_shift_origin
    [  FAILED  ] ascent_uniform_regular_grid.test_uniform_grid_equal_size_input_shift_origin_x
    [  FAILED  ] ascent_uniform_regular_grid.test_uniform_grid_equal_size_input_shift_origin_y
    ./t_ascent_uniform_grid --gtest_list_tests
    ./t_ascent_uniform_grid  --gtest_filter=ascent_uniform_regular_grid.test_uniform_grid_equal_size_input_shift_origin
```    

## Run MPI_TESTS with:

```
cd build_v095/
export OMP_NUM_THREADS=1
for ii in t_ascent_mpi_* ;do echo "(mkdir -p _$ii; cd _$ii ; srun -n2 -t2 -A `id -gn` ../$ii &> o ;cd .. ;echo $ii) &" ;done |sh
for ii in t_ascent_hola_mpi ;do echo "(mkdir -p _$ii; cd _$ii ; srun -n8 -t2 -A `id -gn` ../$ii &> o ;cd .. ;echo $ii) &" ;done |sh
```

### Check the results (daint):

```
_t_ascent_mpi_derived/o:[  FAILED  ] in conduit::utils::conduit_memcpy_strided_elements

_t_ascent_mpi_flatten/o: [Error] in Ascent::publish
```

### Check the results (eiger):

```
# grep -m1 FAILED _t_ascent_*/o

_t_ascent_derived/o:[  FAILED  ] ascent_jit_expressions.derived_support_test (310 ms)
_t_ascent_particle_advection/o:[  FAILED  ] ascent_streamline_point.test_streamline_point (25 ms)
```
