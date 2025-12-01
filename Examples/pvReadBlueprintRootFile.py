# https://gitlab.kitware.com/paraview/paraview/blob/master/Examples/Plugins/PythonAlgorithm/PythonAlgorithmExamples.py
# https://llnl-conduit.readthedocs.io/en/latest/blueprint_mesh.html#mesh-index-protocol
#
# tested with Paraview v6 Mon  1 Dec 16:46:08 CET 2025
# Hint: download hdfview from https://www.hdfgroup.org/download-hdfview/
# Written by: Jean M, Favre, Swiss National Supercomputing Center
##############################################################################

import conduit
import conduit.relay.io
import numpy as np
from vtk import vtkPoints, vtkImageData, vtkRectilinearGrid, vtkStructuredGrid, vtkUnstructuredGrid, vtkIdList, vtkCellArray
from vtk import VTK_QUAD, VTK_TETRA, VTK_POLY_VERTEX, VTK_HEXAHEDRON
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.numpy_interface import algorithms as algs
from vtkmodules import vtkIOCatalystConduit
from paraview.util.vtkAlgorithm import *

def AddArrays(grid, mesh, nnodes):
  it = conduit.NodeIterator()
  it = mesh["mesh/fields"].children()
  while(it.has_next()):
    f = it.next()
    node = it.node()
    nparr = node["values"]
    if node.has_path("values/u"):
      u = np.copy(nparr["u"])
      v = np.copy(nparr["v"])
      w = np.copy(nparr["w"])
      uvw = algs.make_vector(u,v,w)
      if node["association"] == "vertex":
        assert u.shape[0] == nnodes
        grid.GetPointData().AddArray(dsa.numpyTovtkDataArray(uvw, it.name()))
      else:
        grid.GetCellData().AddArray(dsa.numpyTovtkDataArray(uvw, it.name()))
    else:
      nparr2 = np.copy(nparr) # forces the read to take place
      dArray = dsa.numpyTovtkDataArray(nparr2, it.name())
      if node["association"] == "vertex":
        grid.GetPointData().AddArray(dArray)
      else:
        grid.GetCellData().AddArray(dArray)

def ConduitNode_to_Points(mesh):
  assert mesh["mesh/topologies/mesh/type"] == "points"
  pointset = vtkUnstructuredGrid()
  xcoords = mesh["mesh/coordsets/coords/values/x"]
  ycoords = mesh["mesh/coordsets/coords/values/y"]
  zcoords = mesh["mesh/coordsets/coords/values/z"]
  coords = algs.make_vector(xcoords, ycoords, zcoords)

  points = vtkPoints()
  pointset.SetPoints(points)
  points.SetData(dsa.numpyTovtkDataArray(coords, "coords"))

  nnodes = xcoords.shape[0]
  pointset.Allocate(1)
  mlist = vtkIdList()
  mlist.SetNumberOfIds(nnodes)
  for c in range(nnodes):
    mlist.SetId(c, c)
  pointset.InsertNextCell(VTK_POLY_VERTEX, mlist)
  if mesh.has_path("mesh/fields"):
    AddArrays(pointset, mesh, nnodes)

  return pointset

def ConduitNode_to_UnstructuredGrid(mesh):
  assert mesh["mesh/topologies/mesh/type"] == "unstructured"
  unstructured = vtkUnstructuredGrid()
  xcoords = mesh["mesh/coordsets/coords/values/x"]
  ycoords = mesh["mesh/coordsets/coords/values/y"]

  if mesh.has_path("mesh/coordsets/coords/values/z"): # this is a 3D grid
    zcoords = mesh["mesh/coordsets/coords/values/z"]
    coords = algs.make_vector(np.copy(xcoords), np.copy(ycoords), np.copy(zcoords))
  else:
    coords = algs.make_vector(np.copy(xcoords), np.copy(ycoords), np.zeros_like(xcoords))

  points = vtkPoints()
  unstructured.SetPoints(points)
  points.SetData(dsa.numpyTovtkDataArray(coords, "coords"))

  nnodes = xcoords.shape[0]
  connectivity = mesh["mesh/topologies/mesh/elements/connectivity"]
  shape        = mesh["mesh/topologies/mesh/elements/shape"]

  mlist = vtkIdList()  
  if shape == "point":
    unstructured.Allocate(1)
    mlist.SetNumberOfIds(nnodes)
    for c in range(nnodes):
      mlist.SetId(c, c)
    unstructured.InsertNextCell(VTK_POLY_VERTEX, mlist)
  elif shape == "quad":
    nelts = connectivity.shape[0] // 4; print("nelts = ", nelts, " of shape ", shape)
    unstructured.Allocate(nelts)
    mlist.SetNumberOfIds(4)
    for c in range(nelts):
      for ii in range(4):
        mlist.SetId(ii, connectivity[4*c+ii])
      unstructured.InsertNextCell(VTK_QUAD, mlist)
  elif shape == "tet":
    nelts = connectivity.shape[0] // 4; print("nelts = ", nelts, " of shape ", shape)
    unstructured.Allocate(nelts)
    mlist.SetNumberOfIds(4)
    for c in range(nelts):
      for ii in range(4):
        mlist.SetId(ii, connectivity[4*c+ii])
      unstructured.InsertNextCell(VTK_TETRA, mlist)
  elif shape == "hex":
    nelts = connectivity.shape[0] // 8; print("nelts = ", nelts, " of shape ", shape)
    unstructured.Allocate(nelts)
    mlist.SetNumberOfIds(8)
    for c in range(nelts):
      for ii in range(8):
        mlist.SetId(ii, connectivity[8*c+ii])
      unstructured.InsertNextCell(VTK_HEXAHEDRON, mlist)
  else:
    print("found unsupported cells type")
  if mesh.has_path("mesh/fields"):
    AddArrays(unstructured, mesh, nnodes)
  return unstructured

def ConduitNode_to_StructuredGrid(mesh):
  assert mesh["mesh/topologies/mesh/type"] == "structured"
  structured = vtkStructuredGrid()
  xcoords = mesh["mesh/coordsets/coords/values/x"]
  ycoords = mesh["mesh/coordsets/coords/values/y"]
  dims    = [mesh["mesh/topologies/mesh/elements/dims/i"]+1,
            mesh["mesh/topologies/mesh/elements/dims/j"]+1,
            1]
  if mesh.has_path("mesh/topologies/mesh/elements/dims/z"): # this is a 3D grid
    dims[2] = mesh["mesh/topologies/mesh/elements/dims/z"]+1
    zcoords = mesh["mesh/coordsets/coords/values/z"]
    coords = algs.make_vector(np.copy(xcoords), np.copy(ycoords), np.copy(zcoords))
  else:
    coords = algs.make_vector(np.copy(xcoords), np.copy(ycoords), np.zeros_like(xcoords))

  structured.SetDimensions(dims)
  points = vtkPoints()
  structured.SetPoints(points)
  points.SetData(dsa.numpyTovtkDataArray(coords, "coords"))

  nnodes = np.prod(dims)
  if mesh.has_path("mesh/fields"):
    AddArrays(grid, mesh, nnodes)

  return structured

def Make_structured_grid(fname):
  mesh = conduit.Node()
  conduit.relay.io.load(mesh, fname, "hdf5")
  structured = ConduitNode_to_StructuredGrid(mesh)
  return structured
  
def ConduitNode_to_RectilinearGrid(mesh):
  assert mesh["mesh/topologies/mesh/type"] == "rectilinear"
  rectilinear = vtkRectilinearGrid()
  xcoords = mesh["mesh/coordsets/coords/values/x"]
  ycoords = mesh["mesh/coordsets/coords/values/y"]
  dims    = [xcoords.shape[0], ycoords.shape[0], 1]
  if mesh.has_path("mesh/coordsets/coords/values/z"): # this is a 3D grid
    zcoords = mesh["mesh/coordsets/coords/values/z"]
    dims[2] = zcoords.shape[0]
  else:
    zcoords = np.array([0.0])

  rectilinear.SetDimensions(dims)
  rectilinear.SetXCoordinates(dsa.numpyTovtkDataArray(np.copy(xcoords), "xcoords"))
  rectilinear.SetYCoordinates(dsa.numpyTovtkDataArray(np.copy(ycoords), "ycoords"))
  rectilinear.SetZCoordinates(dsa.numpyTovtkDataArray(np.copy(zcoords), "zcoords"))
  
  nnodes = np.prod(dims)              
  if mesh.has_path("mesh/fields"):
    AddArrays(rectilinear, mesh, nnodes)

  return rectilinear
  
def Make_rectilinear_grid(fname):
  mesh = conduit.Node()
  conduit.relay.io.load(mesh, fname, "hdf5")
  rectilinear = ConduitNode_to_RectilinearGrid(mesh)
  return rectilinear

def ConduitNode_to_UniformGrid(mesh):
  assert mesh["mesh/topologies"].child(0)["type"] == "uniform"
  uniform = vtkImageData()
  # initialize for a 2D grid and check later if a 3D grid is present
  origin  = [mesh["mesh/coordsets/coords/origin/x"],
             mesh["mesh/coordsets/coords/origin/y"],
             0.]
  spacing = [mesh["mesh/coordsets/coords/spacing/dx"],
             mesh["mesh/coordsets/coords/spacing/dy"],
             1.0]
  dims    = [mesh["mesh/coordsets/coords/dims/i"],
             mesh["mesh/coordsets/coords/dims/j"],
             1]
  if mesh.has_path("mesh/coordsets/coords/dims/k"): # this is a 3D grid
    origin[2]  = mesh["mesh/coordsets/coords/origin/z"]
    spacing[2] = mesh["mesh/coordsets/coords/spacing/dz"]
    dims[2]    = mesh["mesh/coordsets/coords/dims/k"]

  uniform.SetOrigin(origin)
  uniform.SetSpacing(spacing)
  uniform.SetDimensions(dims)

  nnodes = np.prod(dims)              
  if mesh.has_path("mesh/fields"):
    AddArrays(uniform, mesh, nnodes)
  return uniform
  
def Make_uniform_grid(fname):
  mesh = conduit.Node()
  conduit.relay.io.load(mesh, fname, "hdf5")
  uniform = ConduitNode_to_UniformGrid(mesh)
  return uniform

def createModifiedCallback(anobject):
    import weakref
    weakref_obj = weakref.ref(anobject)
    anobject = None
    def _markmodified(*args, **kwars):
        o = weakref_obj()
        if o is not None:
            o.Modified()
    return _markmodified

@smproxy.reader(name="ConduitBlueprintReader", label="Conduit Blueprint Python Reader",
                extensions="root", file_description="Conduit Blueprint HDF5 files")
class ConduitBlueprintReader(VTKPythonAlgorithmBase):
    """A reader that reads a Conduit Blueprint HDF5 file"""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=1, outputType='vtkPartitionedDataSet')
        self._filename = None

    @smproperty.stringvector(name="FileName")
    @smdomain.filelist()
    @smhint.filechooser(extensions="root", file_description="HDF5 Conduit Blueprint files")
    def SetFileName(self, name):
        """Specify filename for the file to read."""
        if self._filename != name:
            self._filename = name
            self.Modified()

    def RequestInformation(self, request, inInfoVec, outInfoVec):
        executive = self.GetExecutive()
        outInfo = outInfoVec.GetInformationObject(0)
        return 1

    def RequestData(self, request, inInfoVec, outInfoVec):
        from vtkmodules.vtkCommonDataModel import vtkPartitionedDataSet
        from vtkmodules.numpy_interface import dataset_adapter as dsa

        output = dsa.WrapDataObject(vtkPartitionedDataSet.GetData(outInfoVec, 0))
        if self._filename is None:
          raise RuntimeError("No filename specified")
            
        root = conduit.Node()
        conduit.relay.io.load(root, self._filename, "hdf5")
        if root.has_path("blueprint_index/mesh/state/number_of_domains"):
          number_of_domains = root["blueprint_index/mesh/state/number_of_domains"]
          topotype = root["blueprint_index/mesh/topologies"].child(0)["type"]
        else:
          number_of_domains = 1
          topotype = root["mesh/topologies/mesh/type"]
        #output.GetInformation().Set(output.DATA_TIME_STEP(), root["blueprint_index/mesh/state/time"])
        if topotype == "uniform":
          if number_of_domains == 1:
            grid = ConduitNode_to_UniformGrid(root)
            output.SetPartition(0, grid)
          else:
            for domain in range(number_of_domains):
              print("domain ", domain, " in ", basename + format(root["file_pattern"] % domain))
              grid = Make_uniform_grid(format(basename + root["file_pattern"] % domain))
              output.SetPartition(domain, grid)
        elif topotype == "rectilinear":
          if number_of_domains == 1:
            grid = ConduitNode_to_RectilinearGrid(root)
            output.SetPartition(0, grid)
          else:
            for domain in range(number_of_domains):
              print("domain ", domain, " in ", basename + format(root["file_pattern"] % domain))
              grid = Make_rectilinear_grid(format(basename + root["file_pattern"] % domain))
              output.SetPartition(domain, grid)
        elif topotype == "structured":
          if number_of_domains == 1:
            grid = ConduitNode_to_StructuredGrid(root)
            output.SetPartition(0, grid)
          else:
            for domain in range(number_of_domains):
              print("domain ", domain, " in ", basename + format(root["file_pattern"] % domain))
              grid = Make_structured_grid(format(basename + root["file_pattern"] % domain))
              output.SetPartition(domain, grid)
        elif topotype == "unstructured":
          if number_of_domains == 1:
            grid = ConduitNode_to_UnstructuredGrid(root)
            output.SetPartition(0, grid)
        elif topotype == "points":
          if number_of_domains == 1: 
            grid = ConduitNode_to_Points(root)
            output.SetPartition(0, grid)
          else:
            for d in range(number_of_domains):
              child = conduit.Node()
              file_pattern = root["blueprint_index/mesh/state/partition_pattern"]
              conduit.relay.io.load(child, (self._filename[:self._filename.rfind("/")+1]+file_pattern).format(domain=d)[:-2], "hdf5")
              grid = ConduitNode_to_Points(child)
              output.SetPartition(d, grid)
        else:
          print("Mesh type \"", topotype, "\" not implemented yet")

        return 1

