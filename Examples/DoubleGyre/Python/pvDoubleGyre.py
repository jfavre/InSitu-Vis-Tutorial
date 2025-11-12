# ParaView script to run the DoubleGyre in-situ simulation example
# works for both C++ and Python examples.
#
# Written and tested by Jean M. Favre, CSCS
import paraview
paraview.compatibility.major = 6
paraview.compatibility.minor = 0

from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.AxesGrid.Visibility = 1
renderView1.Set(
  ViewSize = [1280, 768],
  InteractionMode = '2D',
  AxesGrid = 'GridAxes3DActor',
  CenterOfRotation = [1.0, 0.5, 0.0],
  CameraPosition = [1.0, 0.5, 6.7],
  CameraFocalPoint = [1.0, 0.5, 0.0],
  CameraFocalDisk = 1.0,
  CameraParallelScale = 0.8546757251683884,
  )

reader = TrivialProducer(registrationName='grid')
readerDisplay = Show(reader, renderView1, 'GeometryRepresentation')
readerDisplay.Representation = 'Outline'

glyph1 = Glyph(registrationName='Glyph1', Input=reader, GlyphType='Arrow')
glyph1.Set(
  OrientationArray = ['POINTS', 'Velocity'],
  ScaleArray = ['POINTS', 'Velocity'],
  ScaleFactor = 0.6,
  GlyphMode = 'Uniform Spatial Distribution (Surface Sampling)',
  MaximumNumberOfSamplePoints = 500,
  )

glyph1Display = Show(glyph1, renderView1, 'GeometryRepresentation')
glyph1Display.Representation = 'Surface'
ColorBy(glyph1Display, ['POINTS', 'Velocity'])

# create a new 'Annotate Time Filter'
annotateTimeFilter1 = AnnotateTimeFilter(registrationName='AnnotateTimeFilter1', Input=reader)

annotateTimeFilter1Display = Show(annotateTimeFilter1)
annotateTimeFilter1Display.Set(
  Bold = 1,
  FontSize = 24,
  )

# create Image extractor
pNG1 = CreateExtractor('PNG', renderView1, registrationName='PNG1')
pNG1.Trigger.Frequency = 5
pNG1.Writer.Set(
  FileName = 'RenderView1_{timestep:06d}{camera}.png',
  ImageResolution = [1280, 768],
  Format = 'PNG',
  )

# write the grid as a VTK Partitioned Dataset
vTR1 = CreateExtractor('VTPD', reader, registrationName='VTPD1')
vTR1.Trigger.Frequency = 10
vTR1.Writer.FileName = 'doublegyre_{timestep:06d}.vtpd'

# Catalyst options
from paraview import catalyst
options = catalyst.Options()
options.GlobalTrigger = 'TimeStep'
options.CatalystLiveTrigger = 'TimeStep'

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    from paraview.simple import SaveExtractsUsingCatalystOptions
    # Code for non in-situ environments; if executing in post-processing
    # i.e. non-Catalyst mode, let's generate extracts using Catalyst options
    SaveExtractsUsingCatalystOptions(options)
