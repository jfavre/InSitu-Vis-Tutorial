##############################################################################
# A simple simulator for the heat equation in 2D, with an in-situ coupling
# using Catalyst https://catalyst-in-situ.readthedocs.io/en/latest/index.html
#
# Author: Jean M. Favre, Swiss National Supercomputing Center
#
# Can run in parallel, splitting the domain in the vertical direction
#
# Run: mpiexec -n 2 python3 heat_diffusion_insitu_parallel_Catalyst.py
#
# Tested with Python 3.10.12, Mon 11 Sep 13:42:19 CEST 2023
#
##############################################################################
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
import catalyst
import catalyst_conduit as conduit
import catalyst_conduit.blueprint

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
        self.yres = self.xres   # self.yres is redefined when splitting the parallel domain
        self.dx = 1.0 / (self.xres + 1)

    def initialize(self):
        """ 2 additional boundary points are added. Iterations will only touch
        the internal grid points.
        """
        self.rmesh_dims = [self.yres + 2, self.xres + 2]
        self.v = np.zeros(self.rmesh_dims)
        self.vnew = np.zeros([self.yres, self.xres])
        self.set_initial_bc()

    def set_initial_bc(self):
        if self.par_size > 1:
          if self.par_rank == 0:
            self.v[0,:] = [math.sin(math.pi * j * self.dx)
                           for j in range(self.rmesh_dims[1])]
            #self.ghosts[-1,:] = 1
          if self.par_rank == (self.par_size-1):
            self.v[-1,:] = self.v[0,:] * math.exp(-math.pi)
            #self.ghosts[0,:] = 1
        else:
          #first (bottom) row
          self.v[0,:] = [math.sin(math.pi * j * self.dx)
                         for j in range(self.rmesh_dims[1])]
          #last (top) row
          self.v[-1,:] = self.v[0,:] * math.exp(-math.pi)

    def finalize(self):
        """plot the scalar field iso-contour lines"""
        fig, ax = plt.subplots()
        CS = ax.contour(self.v, levels=10)
        ax.clabel(CS, inline=True, fontsize=10)
        ax.set_title('Temperature iso-contours')
        plt.savefig(f'Temperature-iso-contours.{self.iteration:04d}.png')
        #plt.show()

    def simulate_one_timestep(self):
        self.iteration += 1
        # print("Simulating time step: iteration=%d" % self.iteration)

        self.vnew = 0.25 * ( self.v[2:, 1:-1]  + # north neighbor
                             self.v[0:-2, 1:-1] + # south neighbor
                             self.v[1:-1, 2:] + # east neighbor
                             self.v[1:-1, :-2]) # west neighbor
        # copy vnew to the interior region of v, leaving the boundary walls untouched.
        self.v[1:-1,1:-1] = self.vnew.copy()

    def main_loop(self):
        while self.iteration < self.Max_iterations:
            self.simulate_one_timestep()

# we now define a sub-class of Simulation to add a Catalyst in-situ coupling

class ParallelSimulation_With_Catalyst(Simulation):
    def __init__(self, resolution=64, iterations=100, meshtype="uniform", pv_script="catalyst_state.py"):
        self.comm = MPI.COMM_WORLD
        Simulation.__init__(self, resolution, iterations)
        self.MeshType = meshtype

        self.insitu = conduit.Node()
        self.pv_script = pv_script
        
    # Add Catalyst mesh definition
    def initialize(self):
        self.par_size = self.comm.Get_size()
        self.par_rank = self.comm.Get_rank()
        # split the parallel domain along the Y axis. No error check!
        self.yres = self.xres // self.par_size
        if self.MeshType == "rectilinear":
          self.xc = np.linspace(0, 1, self.xres + 2)
          self.yc = np.linspace((self.par_rank * self.yres) * self.dx,
                                (((self.par_rank + 1) * self.yres) + 1)* self.dx,
                                self.yres + 2)
        if self.MeshType in ('structured', 'unstructured'):
          self.xc, self.yc = np.meshgrid(np.linspace(0, 1, self.xres + 2),
                                         np.linspace((self.par_rank * self.yres) * self.dx,
                                                     (((self.par_rank + 1) * self.yres) + 1)* self.dx,
                                                     self.yres + 2),
                                         indexing='xy')
                                         
        if self.MeshType == "unstructured":
            self.conn = np.zeros(((self.xres + 1) * (self.yres + 1) * 4), dtype=np.int32)
            i=0
            for iy in range(self.yres+1):
                for ix in range(self.xres+1):
                    self.conn[4*i+0] = ix + iy*(self.xres + 2)
                    self.conn[4*i+1] = ix + (iy+1)*(self.xres + 2)
                    self.conn[4*i+2] = ix + (iy+1)*(self.xres + 2)+ 1
                    self.conn[4*i+3] = ix + iy*(self.xres + 2) + 1
                    i += 1
                    
        Simulation.initialize(self)
        self.initialize_catalyst()

    def main_loop(self):
      while self.iteration < self.Max_iterations:
        self.simulate_one_timestep()
        if self.par_size > 1:
          # if in parallel, exchange ghost cells now
          # define who is my neighbor above and below
          below = self.par_rank - 1
          above = self.par_rank + 1
          if self.par_rank == 0:
            below = MPI.PROC_NULL   # tells MPI not to perform send/recv
          if self.par_rank == (self.par_size-1):
            above = MPI.PROC_NULL   # should only receive/send from/to below
          self.comm.Sendrecv([self.v[-2,], self.xres + 2, MPI.DOUBLE],
                             dest=above, recvbuf=[self.v[-0,], self.xres + 2, MPI.DOUBLE], source=below)
          self.comm.Sendrecv([self.v[1,], self.xres + 2, MPI.DOUBLE],
                             dest=below, recvbuf=[self.v[-1,], self.xres + 2, MPI.DOUBLE], source=above)

        exec_params = conduit.Node()
        channel = exec_params["catalyst/channels/grid"]
        channel["type"] = "mesh"
        mesh = channel["data"]

        # create the coordinate set
        if self.MeshType == "rectilinear":
            mesh["coordsets/coords/type"] = self.MeshType
            mesh["coordsets/coords/values/x"].set_external(self.xc)
            mesh["coordsets/coords/values/y"].set_external(self.yc)
            #print("subset start at ", self.par_rank * self.yres, ", L = ", self.yres + 2)
            mesh["coordsets/coords/values/z"].set(0.0)
        elif self.MeshType == "uniform":
            mesh["coordsets/coords/type"] = self.MeshType
            mesh["coordsets/coords/dims/i"] = self.xres + 2
            mesh["coordsets/coords/dims/j"] = self.yres + 2
            mesh["coordsets/coords/origin/x"] = 0.0
            mesh["coordsets/coords/origin/y"] = self.par_rank * self.yres * self.dx
            mesh["coordsets/coords/spacing/dx"] = self.dx
            mesh["coordsets/coords/spacing/dy"] = self.dx
        else: # self.MeshType in ('structured', 'unstructured'):
            mesh["coordsets/coords/type"] = "explicit"
            mesh["coordsets/coords/values/x"].set_external(self.xc.ravel())
            mesh["coordsets/coords/values/y"].set_external(self.yc.ravel())
        mesh["topologies/mesh/type"] = self.MeshType
        mesh["topologies/mesh/coordset"] = "coords"

        if self.MeshType == "structured":
            mesh["topologies/mesh/elements/dims/i"] = np.int32(self.xres + 1)
            mesh["topologies/mesh/elements/dims/j"] = np.int32(self.yres + 1)

        if self.MeshType == "unstructured":
            mesh["topologies/mesh/elements/shape"] = "quad"
            mesh["topologies/mesh/elements/connectivity"].set_external(self.conn)

        # create a vertex associated field called "temperature"
        mesh["fields/temperature/association"] = "vertex"
        mesh["fields/temperature/topology"] = "mesh"
        # set_external does not handle multidimensional numpy arrays or
        # multidimensional complex strided views into numpy arrays.
        # Views that are effectively 1D-strided are supported.
        mesh["fields/temperature/values"].set_external(self.v.ravel())

        # make sure the mesh we created conforms to the blueprint
        verify_info = conduit.Node()
        if not conduit.blueprint.mesh.verify(mesh, verify_info):
            print("Heat mesh verify failed!")
        else:
            if self.iteration == 1:
              print(mesh.to_yaml())
            #pass

        state = exec_params["catalyst/state"]
        state["timestep"] = self.iteration
        state["time"] = self.iteration * 0.1
        catalyst.execute(exec_params)

    def initialize_catalyst(self):
        """Creates a Conduit node """
        self.insitu["catalyst/scripts/script/filename"] = self.pv_script
        self.insitu["catalyst_load/implementation"] = "paraview"

        # open Catalyst
        catalyst.initialize(self.insitu)

    def finalize_catalyst(self):
        """close"""
        catalyst.finalize(self.insitu)
        
def main():
    #sim = Simulation(resolution=64, iterations=500)
    # choices are meshtype="uniform", "rectilinear", "structured", "unstructured"
    sim = ParallelSimulation_With_Catalyst(meshtype="unstructured",
                                           iterations=3000,
                                           pv_script="../C++/catalyst_state.py")
    sim.initialize()
    sim.main_loop()
    sim.finalize_catalyst()
 
main()


