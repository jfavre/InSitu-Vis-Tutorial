###############################################################################
# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.
###############################################################################

###############################################################################
#
# Kripke CMake Build for Ascent
#
###############################################################################

cmake_minimum_required(VERSION 3.23)
project(Kripke CXX)
find_package(MPI)
find_package(OpenMP)
find_package(Ascent REQUIRED)

set(KRIPKE_SOURCES
    Kripke/Directions.cpp
    Kripke/Grid.cpp
    Kripke/Kernel.cpp
    Kripke/Layout.cpp
    Kripke/Subdomain.cpp
    Kripke/Sweep_Solver.cpp
    Kripke/ParallelComm.cpp
    Kripke/Timing.cpp

    Kripke/Kernel/Kernel_3d_GDZ.cpp
    Kripke/Kernel/Kernel_3d_DGZ.cpp
    Kripke/Kernel/Kernel_3d_ZDG.cpp
    Kripke/Kernel/Kernel_3d_DZG.cpp
    Kripke/Kernel/Kernel_3d_ZGD.cpp
    Kripke/Kernel/Kernel_3d_GZD.cpp

    Kripke/ParallelComm/BlockJacobiComm.cpp
    Kripke/ParallelComm/SweepComm.cpp
    tools/kripke.cpp
    tools/testKernels.cpp
)

# kripke reqs mpi
if(MPI_FOUND)
# copy over example command line
#     configure_file(run_kripke_simple_example.sh
#                    ${CMAKE_CURRENT_BINARY_DIR}/run_kripke_simple_example.sh
#                    COPYONLY)
#     configure_file(ascent_actions.yaml ${CMAKE_CURRENT_BINARY_DIR}/ascent_actions.yaml COPYONLY)
#     configure_file(ascent_options.yaml ${CMAKE_CURRENT_BINARY_DIR}/ascent_options.yaml COPYONLY)
    include_directories(.)
    include_directories("tools")

    set(exename Kripke)
    add_executable(${exename} ${KRIPKE_SOURCES})
    target_compile_definitions(${exename} PRIVATE "-D PARALLEL")
    if(OPENMP_FOUND)
        target_compile_definitions(${exename} PRIVATE "-D KRIPKE_USE_OPENMP")
    endif()
    target_include_directories(${exename} PRIVATE ${ASCENT_INCLUDE_DIRS})
    target_link_libraries(${exename} ascent::ascent_mpi)

endif()
