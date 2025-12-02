#!/bin/bash -l
#SBATCH --job-name="catalyst"
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --constraint=gpu
#SBATCH --account=csstaff
##SBATCH --reservation=insitu
#SBATCH --exclusive
#SBATCH --time=00:10:00
#SBATCH --partition=normal
#SBATCH --uenv=paraview/6.0.1:2181378144
#SBATCH --view=default

mkdir -p $SCRATCH/Catalyst/test
cp $PWD/buildCatalyst/bin/heat_diffusion $SCRATCH/Catalyst/test
cp $PWD/catalyst_state.py $SCRATCH/Catalyst/test

pushd $SCRATCH/Catalyst/test

srun heat_diffusion  --res=128 --mesh=uniform catalyst_state.py
