###############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.
###############################################################################

###############################################################################
#
# Noise CMake Build for Ascent
#
###############################################################################

cmake_minimum_required(VERSION 3.23)
project(noise CXX)

find_package(MPI REQUIRED)
find_package(OpenMP)
find_package(Ascent REQUIRED)

set(noise_sources noise.cpp open_simplex_noise.c)
set(noise_header open_simplex_noise.h)

if(MPI_FOUND)
    set(exename noise)
    add_executable(${exename} ${noise_sources})
    target_compile_definitions(${exename} PRIVATE "-D PARALLEL")
    if(OPENMP_FOUND)
        target_compile_definitions(${exename} PRIVATE "-D NOISE_USE_OPENMP")
    endif()
    target_include_directories(${exename} PRIVATE ${ASCENT_INCLUDE_DIRS})
    target_link_libraries(${exename} ascent::ascent_mpi)

endif()
