# DummySPH

- https://github.com/jfavre/DummySPH.git

[DummySPH] is a mini-app to test in situ visualization libraries for Smoothed
Particle Hydrodynamics. DummySPH supports a set of tests:

- rendering or thresholding or compositing or binning or histsampling or occa

runtime options:

- aos = ON or OFF # ON = AOS (tipsy data), OFF = SOA (std::vector data)
- fp64 = ON or OFF # OFF=<float>, ON=<double>
- tipsy = ON or OFF
- h5part = ON or OFF

and input files:

- hr8799_bol_bd1.017300 # tipsy input file
- dump_wind-shock.h5 # sphexa input file

[DummySPH]: https://github.com/jfavre/DummySPH.git

## Build and run on Alps

### BINNING

```sh
# setup the environment:
uenv image pull build::insitu_ascent/0.9.5:2109123735@daint
uenv start -v default insitu_ascent/0.9.5:2109123735

# get the code:
git clone https://github.com/jfavre/DummySPH.git DummySPH.git
cd DummySPH.git ; git checkout dededc1 ; git switch -c dededc1 ; cd ..

# build with:
cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CUDA_HOST_COMPILER=mpicxx \ 
    -DSTRIDED_SCALARS=OFF \
    -DSPH_DOUBLE=ON \
    -DCAN_LOAD_TIPSY=OFF \
    -DCAN_LOAD_H5Part=ON \
    -DINSITU=Ascent \
    -DAscent_DIR=$(find /user-tools/ -name ascent | grep ascent- | grep cmake) \
    -DCMAKE_CUDA_ARCHITECTURES=90 \
    -S DummySPH.git/src -B build
    # -DSPH_DOUBLE=OFF also works

cmake --build build -j # -v

# run with:
srun -n 1 -t5 ./build/bin/dummysph_ascent --binning rho
# or
srun -n 1 -t5 ./build/bin/dummysph_ascent --binning rho \
    --h5part /capstor/store/cscs/cscs/public/reframe/resources/ascent/inputs/dump_wind-shock.h5
```

#### Outputs

A successful job will generate the following output files:

- simple_trigger_actions.yaml:

```yaml
-
  action: "add_queries"
  queries:
    q1:
      params:
        expression: "min(field('rho'))"
        name: "min_rho"
    q2:
      params:
        expression: "max(field('rho'))"
        name: "max_rho"
```

and the ascent_session.yaml file:

```
min_rho:
  0:
    type: "value_position"
    attrs:
      value:
        value: 0.908040046691895
        type: "double"
      position:
        value: [0.118777185678482, 0.111976027488708, 0.0997187718749046]
        ...
max_rho:
  0:
    type: "value_position"
    attrs:
      value:
        value: 11.6892757415771
```
