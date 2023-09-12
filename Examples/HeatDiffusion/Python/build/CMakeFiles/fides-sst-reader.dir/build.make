# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /local/apps/cmake-3.26.3-linux-x86_64/bin/cmake

# The command to remove a file.
RM = /local/apps/cmake-3.26.3-linux-x86_64/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build

# Include any dependencies generated for this target.
include CMakeFiles/fides-sst-reader.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/fides-sst-reader.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/fides-sst-reader.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/fides-sst-reader.dir/flags.make

CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o: CMakeFiles/fides-sst-reader.dir/flags.make
CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o: CMakeFiles/fides-sst-reader.dir/includes_CUDA.rsp
CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o: /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/fides-sst-reader.cpp
CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o: CMakeFiles/fides-sst-reader.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CUDA object CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o"
	/usr/bin/nvcc -forward-unknown-to-host-compiler $(CUDA_DEFINES) $(CUDA_INCLUDES) $(CUDA_FLAGS) -MD -MT CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o -MF CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o.d -x cu -c /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/fides-sst-reader.cpp -o CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o

CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CUDA source to CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.i"
	$(CMAKE_COMMAND) -E cmake_unimplemented_variable CMAKE_CUDA_CREATE_PREPROCESSED_SOURCE

CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CUDA source to assembly CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.s"
	$(CMAKE_COMMAND) -E cmake_unimplemented_variable CMAKE_CUDA_CREATE_ASSEMBLY_SOURCE

# Object files for target fides-sst-reader
fides__sst__reader_OBJECTS = \
"CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o"

# External object files for target fides-sst-reader
fides__sst__reader_EXTERNAL_OBJECTS =

fides-sst-reader: CMakeFiles/fides-sst-reader.dir/fides-sst-reader.cpp.o
fides-sst-reader: CMakeFiles/fides-sst-reader.dir/build.make
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_rendering-2.0.so.2.0.0
fides-sst-reader: /local/apps/fides-adios2.9-install/lib/libfides.so
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_io-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_image_processing-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_entity_extraction-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_clean_grid-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_connected_components-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_contour-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_vector_analysis-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_mesh_info-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_density_estimate-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_field_conversion-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_field_transform-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_flow-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_geometry_refinement-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_multi_block-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_resampling-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_scalar_topology-2.0.so.2.0.0
fides-sst-reader: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi_cxx.so
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_zfp-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_filter_core-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_worklet-2.0.so.2.0.0
fides-sst-reader: /local/apps/ADIOS2-v2.9.0-install/lib/libadios2_c_mpi.so.2.9.0
fides-sst-reader: /local/apps/ADIOS2-v2.9.0-install/lib/libadios2_c.so.2.9.0
fides-sst-reader: /local/apps/ADIOS2-v2.9.0-install/lib/libadios2_cxx11_mpi.so.2.9.0
fides-sst-reader: /local/apps/ADIOS2-v2.9.0-install/lib/libadios2_cxx11.so.2.9.0
fides-sst-reader: /usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkm_cont-2.0.so.2.0.0
fides-sst-reader: /local/apps/Ascent/install/vtk-m-v2.0.0/lib/libvtkmdiympi.so.2.0.0
fides-sst-reader: CMakeFiles/fides-sst-reader.dir/linkLibs.rsp
fides-sst-reader: CMakeFiles/fides-sst-reader.dir/objects1.rsp
fides-sst-reader: CMakeFiles/fides-sst-reader.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CUDA executable fides-sst-reader"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/fides-sst-reader.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/fides-sst-reader.dir/build: fides-sst-reader
.PHONY : CMakeFiles/fides-sst-reader.dir/build

CMakeFiles/fides-sst-reader.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/fides-sst-reader.dir/cmake_clean.cmake
.PHONY : CMakeFiles/fides-sst-reader.dir/clean

CMakeFiles/fides-sst-reader.dir/depend:
	cd /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build /home/jfavre/Projects/InSitu/InSitu-Vis-Tutorial2022/Examples/JacobiPython/build/CMakeFiles/fides-sst-reader.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/fides-sst-reader.dir/depend
