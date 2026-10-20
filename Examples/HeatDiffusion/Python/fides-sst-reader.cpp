
#include <thread>
#include <vector>
#include <format>
#include <fides/DataSetReader.h>

#include <mpi.h>
#include <adios2.h>

#include <viskores/cont/ArrayRangeCompute.h>
#include <viskores/cont/Algorithm.h>
#include <viskores/cont/Initialize.h>
#include <viskores/worklet/DispatcherMapTopology.h>
#include <viskores/worklet/WorkletMapTopology.h>
#include <viskores/worklet/ScatterPermutation.h>
#include <viskores/rendering/Camera.h>
#include <viskores/rendering/Scene.h>
#include <viskores/rendering/MapperWireframer.h>
#include <viskores/rendering/CanvasRayTracer.h>
#include <viskores/rendering/ColorBarAnnotation.h>
#include <viskores/rendering/View3D.h>
#include <viskores/filter/contour/Contour.h>
#include <viskores/filter/field_transform/PointTransform.h>
#include <viskores/cont/ColorTable.h>
#include <viskores/cont/PartitionedDataSet.h>
#include <viskores/cont/MergePartitionedDataSet.h>
#include <viskores/io/VTKDataSetWriter.h>

using FieldInfoType = fides::metadata::Vector<fides::metadata::FieldInformation>;

int main(int argc, char** argv)
{
  MPI_Init(&argc, &argv);
  int rank, size;

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  viskores::cont::Initialize(argc, argv, viskores::cont::InitializeOptions::AddHelp);
  adios2::ADIOS adios(MPI_COMM_WORLD);
  const std::string source_name = "source";

  fides::io::DataSetReader fides_reader("diffusion-catalyst-fides.json");
  std::unordered_map<std::string, std::string> paths;
  paths[source_name] = std::string("diffusion.bp");
  fides::DataSourceParams sourceParams;
  sourceParams["engine_type"] = "SST";
  fides_reader.SetDataSourceParameters(source_name, std::move(sourceParams));

  // Create a mapper, canvas and view that will be used to render the scene

  viskores::rendering::MapperWireframer mapperWireframe;
  viskores::rendering::CanvasRayTracer canvas(768,768);
  viskores::cont::ColorTable colorTable("viridis");
  colorTable.RescaleToRange({0.0, 1.0});

  size_t step = 0;
  while(true) {
    auto status = fides_reader.PrepareNextStep(paths);
    if (status == fides::StepStatus::EndOfStream)
      {
      break;
      }      
    fides::metadata::MetaData metaData = fides_reader.ReadMetaData(paths);

    const auto& nBlocks = metaData.Get<fides::metadata::Size>(fides::keys::NUMBER_OF_BLOCKS());
    size_t N = nBlocks.NumberOfItems;
        
    std::cout << "Fides got " << N << " blocks" << std::endl;

    fides::metadata::MetaData selections;
    
    size_t begin = N * rank / size;
    size_t end   = N * (rank + 1) / size;

    fides::metadata::Vector<size_t> blockSelection;

    for (size_t i = begin; i < end; ++i)
      {
      blockSelection.Data.push_back(i);
      }
    selections.Set(fides::keys::BLOCK_SELECTION(), blockSelection);
    
    FieldInfoType fieldSelection;
    fieldSelection.Data.push_back(fides::metadata::FieldInformation("temperature",
                                  fides::FieldAssociation::Points));
    selections.Set(fides::keys::FIELDS(), fieldSelection);

    // Read only this rank's blocks
    auto container = fides_reader.ReadDataSet(paths, selections);

    viskores::cont::PartitionedDataSet output = fides::GetAsViskoresPDS(*container);

    std::cout
        << "Consumer rank " << rank
        << " read " << output.GetNumberOfPartitions()
        << " partitions at step " << step
        << std::endl;

    // Create a fresh scene for this timestep
    viskores::rendering::Scene scene;
    
    auto nbOfProducers = output.GetNumberOfPartitions();
    std::cout << "Fides got " << nbOfProducers << " Producers" << std::endl;

    viskores::rendering::Actor mesh_actor = viskores::rendering::Actor(output, "temperature", colorTable);
    mesh_actor.SetScalarRange({0.0, 1.0});
    scene.AddActor(mesh_actor);
    
    for(auto i=0; i < nbOfProducers; i++)
      {
      auto inputData = output.GetPartition(i);

      viskores::filter::contour::Contour contour;
      contour.SetActiveField("temperature");
      contour.SetGenerateNormals(false);
      contour.SetMergeDuplicatePoints(false);
      std::vector<viskores::Float64> isovalues = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9};
      contour.SetIsoValues(isovalues);
      contour.SetInputCellDimensionToPolygons();
      contour.SetFieldsToPass("temperature");
      viskores::cont::DataSet isolines = contour.Execute(inputData);
      //isolines.PrintSummary(std::cout);
    
// need to offset the isolines by a small amount in the direction of the eye-point
      viskores::filter::field_transform::PointTransform xform;
      xform.SetTranslation(viskores::Vec3f(0.0f, 0.0f, 0.001f));
 
      viskores::cont::DataSet isolines2 = xform.Execute(isolines);

      viskores::rendering::Actor isolines_actor(isolines2, "temperature",
                               viskores::rendering::Color(1.0f, 1.0f, 1.0f, 1.0f));

      scene.AddActor(isolines_actor);
      }
    
    canvas.Clear();
    viskores::rendering::View3D view(scene, mapperWireframe, canvas);
    auto camera = view.GetCamera();

    camera.SetLookAt(viskores::Vec3f(0.5, 0.5, 0.0));
    camera.SetPosition(viskores::Vec3f(0.5, 0.5, 100.0));
    camera.SetViewUp(viskores::Vec3f(0.0, 1.0, 0.0));

    view.SetBackgroundColor(viskores::rendering::Color(0.0f, 0.0f, 0.0f));
    view.SetForegroundColor(viskores::rendering::Color(1.0f, 1.0f, 1.0f));
    
    view.Paint();
    view.RenderScreenAnnotations();
    std::string filename = "diffusion_rank_" + std::format("{:03}", rank) + "_step_" + std::format("{:03}", step++) + ".png";
    view.SaveAs(filename);
  }
  fides_reader.Close();
  MPI_Finalize();

}
