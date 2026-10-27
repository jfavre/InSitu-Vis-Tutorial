##############################################################################
# A simple simulator for the heat equation in 2D
#
# Parallel version
#
# Author: Jean M. Favre, Swiss National Supercomputing Center
#
# The Simulation data is written with ADIOS2, with 3 possible outcomes
# A) the default, uses the "BP4" format, writting the time-dependent series to disk
#    with the Fides attributes which enable ParaView to read the data properly
# B) switching to the "SST" mode, the writer expects a data consumer (see fides-sst-reader.cpp)
# C) switching to the "InTransit-vis" mode, ADIOS2 must be compiled with the ParaView plugin

# run: mpiexec -n 2 python3 heat_diffusion_adios_write.py
#
# Tested with Python 3.14.5, Tue Oct 27 11:33:53 AM CET 2026
##############################################################################
import sys, math
import argparse
import numpy as np
import adios2
from mpi4py import MPI

class Simulation:
    """
    A simple 4-point stencil simulation for the heat equation
    
    Attributes
    ----------
    resolution : int
        the number of grid points on the I and J axis (default 64)
    iterations : int
        the maximum number of iterations (default 100)
    """
    def __init__(self, resolution=64, iterations=100):
        self.par_size = 1
        self.par_rank = 0
        self.iteration = 0 # current iteration
        self.Max_iterations = iterations
        self.xres = resolution
        # self.yres is redefined when splitting the parallel domain
        self.dx = 1.0 / (self.xres + 1)

    def Initialize(self):
        """ 2 additional boundary points are added. Iterations will only touch
        the internal grid points.
        """
        self.rmesh_dims = [self.yres + 2, self.xres + 2]
        print("dimensions = ", self.rmesh_dims)
        self.v = np.zeros(self.rmesh_dims) # includes 2 ghosts
        #self.vnew = np.zeros([self.yres, self.xres])
        self.set_initial_bc()
        
    def Initialize_ADIOS(self, adios_io: bool):
        self.adios = adios2.Adios("adios2.xml", self.comm)
        if adios_io:
          self.io = self.adios.declare_io("InSitu-vis")
        else:
          self.io = self.adios.declare_io("writerIO")

    # Global dimensions: Z, Y, X
        shape = [1, self.xres + 2, self.xres + 2]

    # Select the physical rows belonging to this rank.
    # Exclude internal ghost rows.
        if self.par_rank == 0:
            local_start = 0
        else:
            local_start = 1

        if self.par_rank == self.par_size - 1:
            local_end = self.yres + 2
        else:
            local_end = self.yres + 1

    # Local data to write
        self.output = np.ascontiguousarray( self.v[local_start:local_end, :][np.newaxis, :, :])

    # Global start offset
        start_y = self.par_rank * self.yres + local_start

        start = [0, start_y, 0]
        count = list(self.output.shape)

        print(f"Rank {self.par_rank}: "
              f"shape={shape}, start={start}, count={count}")

        self.T_id = self.io.define_variable("temperature", self.output, shape, start, count)
        self.step_id = self.io.define_variable("step", np.array([1], dtype=np.int32))

        self.io.define_attribute("Fides_Data_Model", "uniform")
        self.io.define_attribute("Fides_Origin", np.array([0., 0., 0.]))
        self.io.define_attribute("Fides_Spacing", np.array([self.dx, self.dx, self.dx]))
        self.io.define_attribute("Fides_Dimension_Variable", "temperature")
        self.io.define_attribute("Fides_Variable_List", ["temperature"])
        self.io.define_attribute("Fides_Variable_Associations", ["points"])

    def set_initial_bc(self):
        if self.par_size > 1:
          if self.par_rank == 0:
            self.v[0,:] = [math.sin(math.pi * j * self.dx)
                           for j in range(self.rmesh_dims[1])]
          if self.par_rank == (self.par_size - 1):
            self.v[-1,:] = [math.sin(math.pi * j * self.dx)
                           for j in range(self.rmesh_dims[1])]
        else:
          #first (bottom) row
          self.v[0,:] = [math.sin(math.pi * j * self.dx)
                         for j in range(self.rmesh_dims[1])]
          #last (top) row
          self.v[-1,:] = [math.sin(math.pi * j * self.dx)
                         for j in range(self.rmesh_dims[1])]

    def Finalize(self):
      import gc
      # Ensure ADIOS2 objects are destroyed before MPI finalization.
      self.io = None
      self.adios = None
      gc.collect()

    def SimulateOneTimestep(self):
        # there is no ghost-data exchange. Run in serial-mode only
        self.iteration += 1

        self.vnew = 0.25 * ( self.v[2:, 1:-1]  +  # north neighbor
                             self.v[0:-2, 1:-1] +  # south neighbor
                             self.v[1:-1, 2:] +  # east neighbor
                             self.v[1:-1, :-2])  # west neighbor
        # copy vnew to the interior region of v, leaving the boundary walls untouched.
        self.v[1:-1, 1:-1] = self.vnew.copy()
      
    def MainLoop(self, frequency=100):
        engine = self.io.open("diffusion.bp", adios2.bindings.Mode.Write)
        while self.iteration < self.Max_iterations:
          if self.iteration % frequency == 0:
            if self.par_rank == 0:
                local_start = 0
            else:
                local_start = 1

            if self.par_rank == self.par_size - 1:
                local_end = self.yres + 2
            else:
                local_end = self.yres + 1

            self.output = np.ascontiguousarray(self.v[local_start:local_end, :][np.newaxis, :, :])

            engine.begin_step()
            engine.put(self.T_id, self.output)
            engine.put(self.step_id, np.array([self.iteration], dtype=np.int32))
            engine.end_step()
          self.SimulateOneTimestep()
        engine.close()
        del engine

class ParallelSimulation(Simulation):
    def __init__(self, resolution, iterations):
        self.comm = MPI.COMM_WORLD
        Simulation.__init__(self, resolution, iterations)

    # Override Initialize for parallel
    def Initialize(self):
        self.par_size = self.comm.Get_size()
        self.par_rank = self.comm.Get_rank()
        # split the parallel domain along the Y axis. No error check!
        self.yres = self.xres // self.par_size
        Simulation.Initialize(self)

    def Finalize(self):
        Simulation.Finalize(self)
        
    def SimulateOneTimestep(self):
        Simulation.SimulateOneTimestep(self)

        if self.par_size > 1:
            # if in parallel, exchange ghost cells now
            # define who is my neighbor above and below
            below = self.par_rank - 1
            above = self.par_rank + 1
            if self.par_rank == 0:
                below = MPI.PROC_NULL   # tells MPI not to perform send/recv
            if self.par_rank == (self.par_size - 1):
                above = MPI.PROC_NULL   # should only receive/send from/to below
            self.comm.Sendrecv(
                sendbuf=self.v[-2, :].copy(),
                dest=above,
                recvbuf=self.v[0, :],
                source=below
            )

            self.comm.Sendrecv(
                sendbuf=self.v[1, :].copy(),
                dest=below,
                recvbuf=self.v[-1, :],
                source=above)
'''
The first operation sends the last interior row upward and
receives the lower neighbor's last interior row into the bottom ghost.

The second sends the first interior row downward and
receives the upper neighbor's first interior row into the top ghost.
'''
# Main program
#
def main(args):
    sim = ParallelSimulation(resolution=args.res, iterations=args.timesteps)
    sim.Initialize()
    sim.Initialize_ADIOS(args.pv)
    sim.MainLoop(frequency=args.freq)
    sim.Finalize()


parser = argparse.ArgumentParser(description="heat diffusion miniapp with ADIOS2 output")
parser.add_argument("-t", "--timesteps", type=int, help="number of timesteps (default: 10000)", default=10000)
parser.add_argument("-f", "--freq", type=int, help="stride to write data (default: 500)", default=500)
parser.add_argument("--res", type=int, help="resolution in each direction (default: 64)", default=64)
group = parser.add_mutually_exclusive_group()
group.add_argument('--bp4', action='store_true', help='Use BP4 (default)')
group.add_argument('--pv',  action='store_true', help='Use ParaView')
group.add_argument('--sst', action='store_true', help='Use SST')

if __name__ == "__main__":
    args = parser.parse_args()
    # BP4 is the default if no option is specified
    if not (args.bp4 or args.pv or args.sst):
      args.bp4 = True
    main(args)

