---
layout: section
---

# A Heat Diffusion example

---
level: 2
---

# A CUDA-based mini-app

* Use Ascent
* Use Catalyst
* Use VTKm/Viskores

and get a feel for the ease-of-use and deployment efforts

---

### Ascent instrumentation
<div class="grid grid-cols-[55%_45%]">
<div> <!-- #left -->
```
git clone https://github.com/jfavre/SummerUniversity2024
cd SummerUniversity2024/cuda/practicals/diffusion

uenv image pull insitu_ascent/0.9.5:2109123735

uenv start --view=modules insitu_ascent/0.9.5:2109123735
module load ascent/0.9.5-5tvprek
module load cmake/3.31.8-ujwjqf3
module load cray-mpich/8.1.32-fvq4yfa
module load cuda/12.8.1-fel3gie
module load gcc/13.4.0-yrhdyox
module load hdf5/1.14.6-q54kcdk
module load libfabric/1.22.0-sw5dkak

cmake -S . -B buildAscent-cuda \
      -DCMAKE_CUDA_ARCHITECTURES=90 -DCMAKE_BUILD_TYPE=Release \
      -DINSITU=Ascent

cmake --build buildAscent-cuda

sbatch run_ascent.sh
```
</div>
<div> <!-- #right -->

<img src="/img/Temperature-Ascent.40000.png" style="width: 35vw; min-width: 300px;">
<br>
</div>
</div>
---

### Catalyst instrumentation

```

git clone https://github.com/jfavre/SummerUniversity2024
cd SummerUniversity2024/cuda/practicals/diffusion

uenv start paraview/6.0.1:2191677242@daint --view=default

cmake -S . -B buildCatalyst \
      -DCMAKE_CUDA_ARCHITECTURES=90 -DCMAKE_BUILD_TYPE=Release \
      -DINSITU=Catalyst

cmake --build buildCatalyst

sbatch run_catalyst.sh
```

---

### Catalyst and data on the GPU: the special case of NVIDIA Grace-Hopper
<br>

- NVIDIA\'s NVLink-C2C interconnect enables fast, low latency, and <span v-mark.highlight.yellow>cache coherent interaction</span> between different chiplets
- Every Processing Unit (PU) has complete access to all main memory
- Each GH200 is composed of two NUMA nodes
- Memory allocated with malloc(), new() and mmap() <span v-mark.highlight.yellow>can be accessed by all CPUs and GPUs </span> in the compute node
- Memory allocated with <span v-mark.highlight.yellow>cudaMalloc() cannot be accessed from the CPU or other GPUs</span> on the compute node
- Placement of a memory page is <span v-mark.highlight.yellow>decided by the NUMA node of the thread that first writes
to it</span>, not by the thread that allocates it.
---

### Application: source code changes to run with ParaView Catalyst
<br>
<div class="grid grid-cols-[55%_45%]">
<div> <!-- #left -->
- allocate memory on the host <br>
<v-click> - first touch on the GPU-side <br></v-click>
<v-click> - no need to copy from GPU to host when we trigger the<br>
            in-situ visualizations</v-click>
<br>
<br>
<v-click> - we instrumented a CUDA simulator for the 2D<br>
            heat diffusion equation</v-click>
</div>
<div> <!-- #right -->

<img src="/img//Temperature-Catalyst.40000.png" style="width: 35vw; min-width: 300px;">
<br>
</div>
</div>
---

### Source code changes to run with ParaView Catalyst
<br>

- transform the CUDA-based mini-app to use ParaView Catalyst
```cpp

-    double *x_host = malloc_host<double>(buffer_size);
-    double *x0     = malloc_device<double>(buffer_size);
-    double *x1     = malloc_device<double>(buffer_size);
+    //double *x_host = malloc_host<double>(buffer_size);
+    double *x0     = malloc_host<double>(buffer_size);
+    double *x1     = malloc_host<double>(buffer_size);
```
```cpp
#ifdef USE_CATALYST
     // must copy data to host since we cannot use a CUDA-enabled Catalyst at this time
-    copy_to_host<double>(x1, x_host, buffer_size); // use x1 with most recent result
+    //copy_to_host<double>(x1, x_host, buffer_size); // use x1 with most recent result
     CatalystAdaptor::Execute(step, dt);
 #endif
```
```cpp
 template <typename T>
 T* malloc_host(size_t N, T value=T()) {
     T* ptr = (T*)(malloc(N*sizeof(T)));
-    std::fill(ptr, ptr+N, value);
+    //std::fill(ptr, ptr+N, value);
     return ptr;
 }

```
---

### VTK-m instrumentation
<div class="grid grid-cols-[55%_45%]">
<div> <!-- #left -->
```

git clone https://github.com/jfavre/SummerUniversity2024
cd SummerUniversity2024/cuda/practicals/diffusion

uenv start --view=modules insitu_ascent/0.9.5:2109123735

module load cmake/3.31.8-ujwjqf3
module load cray-mpich/8.1.32-fvq4yfa
module load cuda/12.8.1-fel3gie
module load gcc/13.4.0-yrhdyox
module load libfabric/1.22.0-sw5dkak

export SPACK_SYSTEM_CONFIG_PATH=/user-tools/config/
spack load vtk-m

cmake -S . -B buildVTKm \
      -DCMAKE_CUDA_ARCHITECTURES=90 -DCMAKE_BUILD_TYPE=Release \
      -DINSITU=VTK-m

cmake --build buildVTKm

sbatch run_vtkm.sh
```
</div>
<div> <!-- #right -->

<img src="/img/Temperature-vtkm.040000.00.png" style="width: 35vw; min-width: 300px;">
<br>
</div>
</div>
