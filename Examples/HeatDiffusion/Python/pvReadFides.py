# state file tested with paraview version 6.2
import paraview
import os

paraview.compatibility.major = 6
paraview.compatibility.minor = 2

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

from paraview import print_info

from paraview.catalyst import Options
options = Options()

# directory under which to save all extracts
options.ExtractsOutputDirectory = (os.getenv("SCRATCH") or "/dev/shm") +'/ADIOS2'
SaveExtractsUsingCatalystOptions(options)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
view = GetRenderView()
view.Set(
  ViewSize = [800, 800],
  InteractionMode = '2D',
  AxesGrid = 'GridAxes3DActor',
  CenterOfRotation = [0.5, 0.5, 0.0],
  CameraPosition = [0.5, 0.5, 3.35],
  CameraFocalPoint = [0.5, 0.5, 0.0],
  CameraFocalDisk = 1.0,
  CameraParallelScale = 0.707,
)

if __name__ == "__main__":
  producer = FidesReader(registrationName='diffusion.bp', FileName='diffusion.bp')
else:
  producer = TrivialProducer(registrationName='fides')

# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=producer)
contour1.Set(
  ContourBy = ['POINTS', 'temperature'],
  ComputeNormals = 0,
  Isosurfaces = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

producerDisplay = Show(producer)
producerDisplay.Representation = 'Surface'
ColorBy(producerDisplay, ('POINTS', 'temperature'))
# get color transfer function/color map for 'temperature'
temperatureLUT = GetColorTransferFunction('temperature')
temperatureLUT.RescaleTransferFunction(0.1, 0.9)

contour1Display = Show(contour1, view, 'GeometryRepresentation')
ColorBy(contour1Display, ('POINTS', 'temperature'))
contour1Display.LineWidth = 2.0

temperatureLUTColorBar = GetScalarBar(temperatureLUT, view)
temperatureLUTColorBar.Title = 'temperature'
temperatureLUTColorBar.ComponentTitle = ''

# set color bar visibility
temperatureLUTColorBar.Visibility = 1

contour1Display.SetScalarBarVisibility(view, True)

SetActiveSource(contour1)

# the extractor will save the view on each time step
extractor = CreateExtractor('PNG', view, registrationName='PNG1')
extractor.Writer.FileName = 'diffusion-{timestep:03d}.png'
extractor.Writer.ImageResolution = [800, 800]

if __name__ == "__main__":
  GetAnimationScene().UpdateAnimationUsingDataTimeSteps()

def catalyst_execute(info):
    global producer
    producer.UpdatePipeline()
