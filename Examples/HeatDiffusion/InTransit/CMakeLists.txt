project(Heat-diffusion-adios)
cmake_minimum_required(VERSION 3.26)

find_package(Fides REQUIRED)
#find_package(ADIOS2 REQUIRED)
set(CMAKE_CXX_STANDARD 20)
if (ADIOS2_VERSION VERSION_GREATER_EQUAL "2.8.0")
  set(ADIOS_DEFS FIDES_ADIOS_HAS_RANDOM_ACCESS)
endif()

find_package(Viskores REQUIRED)

if (Viskores_ENABLE_CUDA)
  enable_language(CUDA)
endif()

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
  set(VTKM_LIBS viskores::cont viskores::rendering viskores::filter)
  target_link_libraries(fides-sst-reader PUBLIC
     ${VTKM_LIBS} MPI::MPI_C MPI::MPI_CXX fides)
endif()

