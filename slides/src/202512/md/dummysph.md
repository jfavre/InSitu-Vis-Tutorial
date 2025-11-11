---
layout: section
---

# DummySPH

---
level: 2
---

# Ascent: UENV Setup (Ampere GPU) *WIP*

```shell
uenv start -v modules ...
module load gcc/13.4.0-v5udhnr  cuda/12.8.1-syqfixq  cray-mpich/8.1.32-e3dozl7  libfabric/1.22.0-4shi6yr
module load cmake/3.31.8-l2wdaet  hdf5/1.14.6-wvltbww  ascent/0.9.5-6y6zkws
```
```shell
mpicxx --version # g++ (Spack GCC) 13.4.0
mpichversion # 3.4a2
nvcc --version # V12.8.93
cmake --version # 3.31.8
h5dump --version # 1.14.6
```
<!-- #comment: see src/0 -->

---
level: 2
---

# Ascent: Setup (Hopper GPU)

```shell
uenv image pull build::insitu_ascent/0.9.5:2109123735
uenv start -v modules insitu_ascent/0.9.5:2109123735
```

<Admonition type="note" title="Input data">
h5dump -H /capstor/store/cscs/cscs/public/reframe/resources/ascent/inputs/dump_wind-shock.h5 |grep DATASET |sort -u

m, rho, temp, x,y,zm vx,vy,vz
</Admonition>

---
level: 2
---

# Ascent: rendering

- output: .png

<div grid="~ cols-2 gap-4" class="mt-4">
 <div class="col-span-1">

```yaml
action: "add_scenes"
scenes:
  s1:
    plots:
      p1:
        type: "pseudocolor"
        field: "rho"
        color_table:
          name: "viridis"
    renders:
      r1:
        color_bar_position: [-0.9, 0.9, 0.8, 0.85]
        camera:
          azimuth: 30.0
          elevation: 30.0
        image_prefix: "datasets/out_%04d"
        bg_color: [1.0, 1.0, 1.0]
        fg_color: [0.0, 0.0, 0.0]
```
 </div>

 <div class="col-span-1">
  <div class="w-full">
        <img src="/img/dummysph/ascent_rendering.png" />
  </div>

[rendering](https://ascent.readthedocs.io/en/latest/Actions/Examples.html#an-example-changing-the-rendering-bounds-of-a-3d-field)
 </div>

</div>

---
level: 2
---

# Ascent: thresholding

- output: Conduit Blueprint HDF5 .root -> VisIt

<div grid="~ cols-2 gap-1" class="mt-4">
 <div class="col-span-1">
 <Transform :scale="0.7">
```yaml
  action: "add_queries"
  queries:
    q1:                                       
      params:                                 
        expression: "min(field('rho')).value" 
        name: "min_rho"                       
    q2:
      params:
        expression: "max(field('rho')).value"
        name: "max_rho"
-
  action: "add_pipelines"
  pipelines:
    p1:
      f1:
        type: "threshold"
        params:
          field: "rho"
          min_value: "min_rho + 0.25 *(max_rho - min_rho)"
          max_value: "max_rho - 0.25 *(max_rho - min_rho)"
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

 </Transform>
 </div>

 <div class="col-span-1">
  <div class="w-90">
        <img src="/img/dummysph/ascent_thresholding.png" />
  </div>

[__thresholding](https://ascent.readthedocs.io/en/latest/Actions/Examples.html#an-example-of-using-the-threshold-filter)
 </div>

</div>


---
level: 2
---

# Ascent: binning

- output: ascent_session.yaml

<div grid="~ cols-3 gap-1" class="mt-4">
<div class="col-span-1">

```yaml
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

[data-binning](https://ascent.readthedocs.io/en/latest/Actions/Examples.html#an-example-of-data-binning-binning-spatially-and-summing-a-field)
</div>

<div class="col-span-1">
<Transform :scale="0.9">

```yaml
 min_rho:
  0:
    type: "value_position"
    attrs:
      value:
        value: 0.908040046691895
        type: "double"
      position:
        value: [0.118777185975482,
                0.111976027488708,
                0.0997187718749046]
        type: "vector"
      element:
        rank: 0
        domain_index: 0
        index: 304343
        assoc: "vertex"
    time: 2.22580130724132e-317
```
</Transform>
</div>

<div class="col-span-1">
<Transform :scale="0.9">

```yaml
max_rho:
  0:
    type: "value_position"
    attrs:
      value:
        value: 11.6892757415771
        type: "double"
      position:
        value: [0.118454301397405,
                0.112679170766208,
                0.144455551349358]
        type: "vector"
      element:
        rank: 0
        domain_index: 0
        index: 1013560
        assoc: "element"
    time: 2.22580130724132e-317
```
</Transform>
</div>

</div>

---
level: 2
---

# Ascent: histogram sampling

- output: Conduit Blueprint HDF5 .root -> VisIt

<div grid="~ cols-2 gap-1" class="mt-4">
 <div class="col-span-1">
 <Transform :scale="0.9">

```yaml
  action: "add_pipelines"
  pipelines:
    p1:
      f1:
        type: "histsampling"
        params:
          sample_rate: 0.05
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

 </Transform>

 </div>

 <div class="col-span-1">
  <div class="w-90">
        <img src="/img/dummysph/ascent_histsampling.png" />
  </div>

[__histsampling](https://ascent.readthedocs.io/en/latest/Actions/Examples.html#an-example-of-the-sampling-filter-using-histogram-based-approach)
 </div>

</div>

---
level: 2
---

# Ascent: compositing (wip)

---
level: 2
---

# Ascent: occa (wip)

---
layout: two-cols-header
---

# Ascent: clipping (SPH-EXA)

::left::

<Transform :scale="0.8">

```yaml
  action: "add_triggers"
  triggers:
    t1:
      params:
        condition: "cycle() % 1 == 0"
        actions:
          -
            action: "add_queries"
            queries:q1:params:
                  expression: "field('kx') * field('m') / field('xm')"
                  name: "density"
          -
            action: "add_pipelines"
            pipelines:
              pl_threshold_thin_clip_z:  pl_threshold_thin_clip_y:
                f1:                        f1:
                  type: "threshold"          type: "threshold"
                  params:                    params:
                    field: "z"                 field: "y"
                    min_value: 0.12425         min_value: 0.12425
                    max_value: 0.12575         max_value: 0.12575
```
</Transform>

::right::

<Transform :scale="0.55">

```yaml
          -
            action: "add_scenes"
            scenes:s1:plots:
                  p1:                                    p2:
                    type: "pseudocolor"                    type: "pseudocolor"
                    field: "density"                       field: "density"
                    pipeline: "pl_threshold_thin_clip_z"   pipeline: "pl_threshold_thin_clip_y"
                    min_value: 1                           min_value: 1
                    max_value: 10                          max_value: 10
                    color_table:                           color_table:
                      name: "Yellow - Gray - Blue"           name: "Yellow - Gray - Blue"
                      annotation: "false"                    annotation: "true"
                    points:                                points:
                      radius: 0.001                          radius: 0.001
                renders:r1:
                    image_prefix: "datasets/density.%05d"
                    image_width: 1920
                    image_height: 1080
                    camera:
                      look_at: [0.5, 0.125, 0.125]
                      position: [0.5, 0.125, 3.0]
                      up: [0.0, 1.0, 0.0]
                      azimuth: -35.0
                      elevation: 25.0
                      zoom: 5.25
                    dataset_bounds: [0.0, 1.0, 0.0, 0.25, 0.0, 0.25]
                    color_bar_position: [0.2, 0.9, -0.9, -0.75]
```

<img src="/img/dummysph/ascent_sphexa_density.png" class="h-60 ml-35 mr-1" border="1px" />

</Transform>

<style>
.two-cols-header {
  column-gap: 2px;
}
</style>
