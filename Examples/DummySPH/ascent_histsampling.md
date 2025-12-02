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

### HISTSAMPLING

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
    # -DSPH_DOUBLE=OFF is not yet implemented

cmake --build build -j # -v

# run with:
srun -n 1 -t5 ./build/bin/dummysph_ascent --histsampling out
# or
srun -n 1 -t5 ./build/bin/dummysph_ascent --histsampling out \
    --h5part /capstor/store/cscs/cscs/public/reframe/resources/ascent/inputs/dump_wind-shock.h5
# ~1min runtime
```

#### Outputs

A successful job will generate the following output files:

- simple_trigger_actions.yaml:

```yaml
-
  action: "add_pipelines"
  pipelines:
    p1:
      f1:
        type: "histsampling"
        params:
          sample_rate: 0.5
          bins: 64
          field: "rho"
-
  action: "add_extracts"
  extracts:
    e1:
      type: "relay"
      pipeline: "p1"
      params:
        path: "datasets/out"
        protocol: "blueprint/mesh/hdf5"
        fields:
          - "rho"
```

and a Conduit Blueprint HDF5 file (that can be read with [VisIt]):

- datasets/out.cycle_000000.root (with    --h5part): ![png0](./img/histsampling/datasets/out.cycle_000000_root.png)

- datasets/out.cycle_000001.root (without --h5part): ![png1](./img/histsampling/datasets/out.cycle_000001_root.png)

[VisIt]: https://visit-dav.github.io/visit-website/releases-as-tables/#series-34
