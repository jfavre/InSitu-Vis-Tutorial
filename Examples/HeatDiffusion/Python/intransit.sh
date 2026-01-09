#!/bin/bash
#SBATCH --job-name="ADIOS-InTransit"
#SBATCH --nodes=1
#SBATCH --ntasks=3

#SBATCH --account=csstaff
#SBATCH --time=00:05:00
#SBATCH --partition=debug
#SBATCH --constraint=gpu
#SBATCH --exclusive
#SBATCH --mem=450G
#SBATCH --uenv=paraview/6.0.1:v1
#SBATCH --view=default

## demo test runnig a data producer in parallel with 2 tasks, writing data in SST mode
## with one data consumer (the fides-sst-reader) running on 1 task

spack load adios2
mkdir $SCRATCH/InTransit
cp buildSSTConsumer/fides-sst-reader $SCRATCH/InTransit
cp heat_diffusion_insitu_parallel.py $SCRATCH/InTransit
cp adios2.xml $SCRATCH/InTransit
cp diffusion-catalyst-fides.json $SCRATCH/InTransit

cd $SCRATCH/InTransit
rm -rf diffusion.bp*

srun -n 2 -N1 --exclusive python3 heat_diffusion_insitu_parallel.py &
srun -n 1 -N1 --exclusive sleep 5 && $SCRATCH/InTransit/fides-sst-reader

wait
