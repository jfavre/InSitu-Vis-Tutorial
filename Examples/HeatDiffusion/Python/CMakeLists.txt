project(Heat-diffusion-adios C CXX)
cmake_minimum_required(VERSION 3.26)

find_package(Fides REQUIRED)
find_package(ADIOS2 REQUIRED)
set(CMAKE_CXX_STANDARD 20)
if (ADIOS2_VERSION VERSION_GREATER_EQUAL "2.8.0")
  set(ADIOS_DEFS FIDES_ADIOS_HAS_RANDOM_ACCESS)
endif()

get_target_property(FIDES_INCLUDES fides::fides INTERFACE_INCLUDE_DIRECTORIES)

set(default_build_type "RelWithDebInfo")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
  set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

find_package(Viskores REQUIRED)

#if (Viskores_ENABLE_CUDA)
#  enable_language(CUDA)
#endif()

if(ADIOS2_HAVE_MPI)
  set(FIDES_USE_MPI TRUE)
  set(MPI_DEFS FIDES_USE_MPI)
  set(MPI_LIBS MPI::MPI_CXX)
endif()

if (FIDES_USE_MPI)
  add_executable(fides-sst-reader fides-sst-reader.cpp)
  viskores_add_target_information(fides-sst-reader
                            DROP_UNUSED_SYMBOLS
                            MODIFY_CUDA_FLAGS
                            DEVICE_SOURCES fides-sst-reader.cpp)
# 2. Manually apply it to your target
if(FIDES_INCLUDES)
  target_include_directories(fides-sst-reader PRIVATE ${FIDES_INCLUDES})
endif()
  set(VISKORES_LIBS viskores::cont viskores::filter_contour viskores::rendering viskores::filter)
  target_compile_definitions(fides-sst-reader PRIVATE ${MPI_DEFS} ${RENDERING_DEFS})
  target_link_libraries(fides-sst-reader PRIVATE
      ${VISKORES_LIBS} ${MPI_LIBS} fides::fides adios2::cxx)
endif()

