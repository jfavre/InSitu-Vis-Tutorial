cmake_minimum_required(VERSION 3.23)

project(ascent_tests)
set(CMAKE_CXX_STANDARD 20)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
include(setup_GTest)

find_package(MPI REQUIRED COMPONENTS CXX)
find_package(Ascent REQUIRED)

function(buildTest testname)
    set(exename ${testname})
    add_executable(${exename} ${testname}.cpp)
    target_include_directories(${exename} PRIVATE "${PROJECT_SOURCE_DIR}" "${PROJECT_SOURCE_DIR}/..") # t_utils.hpp
    target_link_libraries(${exename} ascent::ascent GTest::gtest_main)
endfunction()

function(buildMPItest testname)
    set(exename ${testname})
    add_executable(${exename} ${testname}.cpp)
    target_include_directories(${exename} PRIVATE "${PROJECT_SOURCE_DIR}/..") # t_utils.hpp
    target_link_libraries(${exename} ascent::ascent_mpi GTest::gtest_main)
endfunction()


#{{{ BASIC_TESTS
set(BASIC_TESTS t_ascent_smoke
                t_ascent_runtime_options
                t_ascent_data_binning
                t_ascent_utils
                t_ascent_logging
                t_ascent_annotations
                t_ascent_derived
                t_ascent_empty_runtime
                t_ascent_expressions
                t_ascent_external_surfaces
                t_ascent_cinema_a
                t_ascent_color_bar_pos
                t_ascent_render_2d
                t_ascent_render_3d
                t_ascent_render_2d_poly
                t_ascent_render_3d_poly
                t_ascent_render_2d_mixed
                t_ascent_render_3d_mixed
                t_ascent_render_auto_camera
                t_ascent_info
                t_ascent_render_bounds
                t_ascent_web_flow
                t_ascent_web_main
                t_ascent_clip
                t_ascent_scalar_renderer
                t_ascent_multi_topo
                t_ascent_gradient
                t_ascent_qcriterion
                t_ascent_divergence
                t_ascent_vorticity
                t_ascent_relay
                t_ascent_conduit_extract
                t_ascent_vtk_file_extract
                t_ascent_htg
                t_ascent_flatten
                t_ascent_partition
                t_ascent_clip_with_field
                t_ascent_contour
                t_ascent_iso_volume
                t_ascent_image_compare
                t_ascent_pipelines_to_pipelines
                t_ascent_threshold
                t_ascent_transform
                t_ascent_slice
                t_ascent_scale
                t_ascent_particle_advection
                t_ascent_patch_amr
                t_ascent_vector_ops
                t_ascent_flow_runtime
                t_ascent_recenter
                t_ascent_rover
                t_ascent_lagrangian
                t_ascent_log
                t_ascent_amr
                t_ascent_queries
                t_ascent_failed_pipeline
                t_ascent_commands
                t_ascent_steering
                t_ascent_triggers
                t_ascent_blueprint_reductions
                t_ascent_sampling
                t_ascent_sample
                t_ascent_uniform_grid
                t_ascent_mir
                t_ascent_hola)
#}}}

#{{{ DEVICE_TESTS
#ko/gh200 set(DEVICE_TESTS  t_ascent_execution_policies
set(DEVICE_TESTS  t_ascent_memory
                  t_ascent_gpu_data_source)
#}}}

#{{{ MPI_TESTS
set(MPI_TESTS  t_ascent_mpi_smoke
               t_ascent_mpi_empty_runtime
               t_ascent_mpi_derived
               t_ascent_mpi_expressions
               t_ascent_mpi_flatten
               t_ascent_mpi_partition
               t_ascent_mpi_render_2d
               t_ascent_mpi_render_3d
               t_ascent_mpi_statistics
               t_ascent_mpi_multi_topo
               t_ascent_mpi_slice
               t_ascent_mpi_uniform_grid
               t_ascent_mpi_vtk_file_extract
               t_ascent_mpi_add_ranks
               t_ascent_mpi_add_domain_ids
               t_ascent_mpi_unique_ids)

list(APPEND MPI_TESTS t_ascent_hola_mpi)
#}}}

foreach(ttt ${BASIC_TESTS} ${DEVICE_TESTS})
    buildTest(${ttt})
endforeach()

if(MPI_FOUND)
    foreach(ttt ${MPI_TESTS})
        buildMPItest(${ttt})
    endforeach()
endif()

#{{{ CUDA:
#    ascent.git/src/tests/ascent/t_ascent_gpu_data_source.cpp
#    ascent.git/src/tests/ascent/t_ascent_render_3d.cpp
#
# # we need to make sure CUDA_RESOLVE_DEVICE_SYMBOLS is on for our target
# # (it propgates some way magically in 3.14, but not in 3.21)
# if(CMAKE_CUDA_COMPILER)
#     set_property(TARGET ascent_mpi_render_example PROPERTY CUDA_RESOLVE_DEVICE_SYMBOLS ON)
# endif()
# if(CMAKE_CUDA_COMPILER)
# 	set_property(TARGET ascent_render_example PROPERTY CUDA_ARCHITECTURES "90")
# endif()
#}}}
