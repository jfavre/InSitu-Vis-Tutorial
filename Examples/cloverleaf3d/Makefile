ASCENT_DIR ?= /user-tools/env/default
include $(ASCENT_DIR)/share/ascent/ascent_config.mk

INC_FLAGS = $(ASCENT_INCLUDE_FLAGS)
FFLAGS = -DUSE_MOD -fopenmp -fallow-invalid-boz -fallow-argument-mismatch -w -g $(INC_FLAGS)
LNK_FLAGS = $(ASCENT_LINK_RPATH) $(ASCENT_MPI_LIB_FLAGS) -fopenmp
FC = mpif90
CC = mpicc
CXX = mpicxx

.DEFAULT:
	-echo $@ does not exist.

all: cloverleaf3d.exe

PdV.o: ./PdV.f90 clover.o report.o PdV_kernel.o revert.o update_halo.o ideal_gas.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./PdV.f90
PdV_kernel.o: ./PdV_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./PdV_kernel.f90
accelerate.o: ./accelerate.f90 clover.o accelerate_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./accelerate.f90
accelerate_kernel.o: ./accelerate_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./accelerate_kernel.f90
advec_cell_driver.o: ./advec_cell_driver.f90 clover.o advec_cell_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./advec_cell_driver.f90
advec_cell_kernel.o: ./advec_cell_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./advec_cell_kernel.f90
advec_mom_driver.o: ./advec_mom_driver.f90 clover.o advec_mom_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./advec_mom_driver.f90
advec_mom_kernel.o: ./advec_mom_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./advec_mom_kernel.f90
advection.o: ./advection.f90 clover.o advec_cell_driver.o advec_mom_driver.o update_halo.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./advection.f90
build_field.o: ./build_field.f90 clover.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./build_field.f90
calc_dt.o: ./calc_dt.f90 clover.o calc_dt_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./calc_dt.f90
calc_dt_kernel.o: ./calc_dt_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./calc_dt_kernel.f90
clover.o: ./clover.F90 data.o definitions.o pack_kernel.o
	$(FC) $(CPPDEFS) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./clover.F90
clover_leaf.o: ./clover_leaf.f90 clover.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./clover_leaf.f90
data.o: ./data.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./data.f90
definitions.o: ./definitions.f90 data.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./definitions.f90
field_summary.o: ./field_summary.f90 clover.o ideal_gas.o field_summary_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./field_summary.f90
field_summary_kernel.o: ./field_summary_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./field_summary_kernel.f90
flux_calc.o: ./flux_calc.f90 clover.o flux_calc_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./flux_calc.f90
flux_calc_kernel.o: ./flux_calc_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./flux_calc_kernel.f90
generate_chunk.o: ./generate_chunk.f90 clover.o generate_chunk_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./generate_chunk.f90
generate_chunk_kernel.o: ./generate_chunk_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./generate_chunk_kernel.f90
hydro.o: ./hydro.f90 clover.o timestep.o viscosity.o PdV.o accelerate.o flux_calc.o advection.o reset_field.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./hydro.f90
ideal_gas.o: ./ideal_gas.f90 clover.o ideal_gas_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./ideal_gas.f90
ideal_gas_kernel.o: ./ideal_gas_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./ideal_gas_kernel.f90
initialise.o: ./initialise.f90 clover.o parse.o report.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./initialise.f90
initialise_chunk.o: ./initialise_chunk.f90 clover.o initialise_chunk_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./initialise_chunk.f90
initialise_chunk_kernel.o: ./initialise_chunk_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./initialise_chunk_kernel.f90
pack_kernel.o: ./pack_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./pack_kernel.f90
parse.o: ./parse.f90 data.o report.o clover.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./parse.f90
read_input.o: ./read_input.f90 clover.o parse.o report.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./read_input.f90
report.o: ./report.f90 data.o clover.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./report.f90
reset_field.o: ./reset_field.f90 clover.o reset_field_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./reset_field.f90
reset_field_kernel.o: ./reset_field_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./reset_field_kernel.f90
revert.o: ./revert.f90 clover.o revert_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./revert.f90
revert_kernel.o: ./revert_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./revert_kernel.f90
start.o: ./start.f90 clover.o parse.o update_halo.o ideal_gas.o build_field.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./start.f90
timer.o: ./timer.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./timer.f90
timer_c.o: ./timer_c.c
	$(CC) $(CPPDEFS) $(CPPFLAGS) $(CFLAGS) $(OTHERFLAGS) $(OTHER_CFLAGS) -c	./timer_c.c
timestep.o: ./timestep.f90 clover.o report.o update_halo.o viscosity.o calc_dt.o ideal_gas.o definitions.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./timestep.f90
update_halo.o: ./update_halo.f90 clover.o update_halo_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./update_halo.f90
update_halo_kernel.o: ./update_halo_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./update_halo_kernel.f90
viscosity.o: ./viscosity.f90 clover.o viscosity_kernel.o
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./viscosity.f90
viscosity_kernel.o: ./viscosity_kernel.f90
	$(FC) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./viscosity_kernel.f90
visit.o: ./visit.F90 clover.o update_halo.o viscosity.o ideal_gas.o
	$(FC) $(CPPDEFS) $(FPPFLAGS) $(FFLAGS) $(OTHERFLAGS) $(OTHER_FFLAGS) -c	./visit.F90
clover_main.o: ./clover_main.cpp
	$(CXX) -g -c $<

SRC = ./advec_mom_driver.f90 ./revert_kernel.f90 ./reset_field.f90 ./revert.f90 ./initialise_chunk.f90 ./reset_field_kernel.f90 ./report.f90 ./start.f90 ./parse.f90 ./viscosity.f90 ./ideal_gas.f90 ./field_summary_kernel.f90 ./calc_dt_kernel.f90 ./flux_calc_kernel.f90 ./visit.F90 ./PdV.f90 ./clover.F90 ./timestep.f90 ./hydro.f90 ./accelerate.f90 ./advection.f90 ./ideal_gas_kernel.f90 ./pack_kernel.f90 ./read_input.f90 ./PdV_kernel.f90 ./advec_cell_kernel.f90 ./advec_cell_driver.f90 ./timer.f90 ./data.f90 ./initialise_chunk_kernel.f90 ./flux_calc.f90 ./update_halo.f90 ./accelerate_kernel.f90 ./advec_mom_kernel.f90 ./update_halo_kernel.f90 ./initialise.f90 ./generate_chunk_kernel.f90 ./viscosity_kernel.f90 ./timer_c.c ./clover_leaf.f90 ./definitions.f90 ./field_summary.f90 ./generate_chunk.f90 ./calc_dt.f90 ./build_field.f90 ./clover_main.cpp

OBJ = advec_mom_driver.o revert_kernel.o reset_field.o revert.o initialise_chunk.o reset_field_kernel.o report.o start.o parse.o viscosity.o ideal_gas.o field_summary_kernel.o calc_dt_kernel.o flux_calc_kernel.o visit.o PdV.o clover.o timestep.o hydro.o accelerate.o advection.o ideal_gas_kernel.o pack_kernel.o read_input.o PdV_kernel.o advec_cell_kernel.o advec_cell_driver.o timer.o data.o initialise_chunk_kernel.o flux_calc.o update_halo.o accelerate_kernel.o advec_mom_kernel.o update_halo_kernel.o initialise.o generate_chunk_kernel.o viscosity_kernel.o timer_c.o clover_leaf.o definitions.o field_summary.o generate_chunk.o calc_dt.o build_field.o clover_main.o

clean:
	-rm -f $(OBJ) *.mod cloverleaf3d.exe

cloverleaf3d.exe: $(OBJ)
	$(FC) $(OBJ) -o $@ $(LNK_FLAGS)
