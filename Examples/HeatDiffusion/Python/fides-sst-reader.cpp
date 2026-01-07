#include <mpi.h>
#include <adios2.h>
#include <thread>
#include <vector>
#include <format>
#include <fides/DataSetReader.h>

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
#include <viskores/rendering/View3D.h>
#include <viskores/filter/contour/Contour.h>
#include <viskores/filter/field_transform/PointTransform.h>
#include <viskores/cont/ColorTable.h>
#include <viskores/io/VTKDataSetWriter.h>


using FieldInfoType = fides::metadata::Vector<fides::metadata::FieldInformation>;

int main(int argc, char** argv)
{
  MPI_Init(&argc, &argv);
  viskores::cont::Initialize(argc, argv, viskores::cont::InitializeOptions::AddHelp);
  adios2::ADIOS adios(MPI_COMM_WORLD);
  const std::string source_name = "source";

  fides::io::DataSetReader fides_reader("diffusion-catalyst-fides.json");
  std::unordered_map<std::string, std::string> paths;
  paths[source_name] = std::string("diffusion.bp");
  fides::DataSourceParams params;
  params["engine_type"] = "SST";
  fides_reader.SetDataSourceParameters(source_name, std::move(params));

  size_t step = 0;
  while(true) {
    auto status = fides_reader.PrepareNextStep(paths);
    fides::metadata::MetaData metaData = fides_reader.ReadMetaData(paths);
    if (status == fides::StepStatus::EndOfStream)
      {
      break;
      }

    // Create a mapper, canvas and view that will be used to render the scene
    viskores::rendering::Scene scene;
    viskores::rendering::MapperWireframer mapperWireframe;
    viskores::rendering::CanvasRayTracer canvas(768,768);
    viskores::cont::ColorTable colorTable("viridis");
    colorTable.RescaleToRange({0.0, 1.0});
    
    fides::metadata::MetaData selections;
    fides::metadata::Vector<size_t> blockSelection;
    blockSelection.Data.push_back(0);

    FieldInfoType fieldSelection;
    fieldSelection.Data.push_back(fides::metadata::FieldInformation("temperature",
                                  viskores::cont::Field::Association::Points));
    selections.Set(fides::keys::FIELDS(), fieldSelection);

    viskores::cont::PartitionedDataSet output = fides_reader.ReadDataSet(paths, selections);
    auto nbOfProducers = output.GetNumberOfPartitions();
    std::vector<viskores::rendering::Actor> mesh_actors;
    for(auto i=0; i < nbOfProducers; i++)
      {
      auto inputData = output.GetPartition(i);
      /*
      const auto& scalarField = inputData.GetField("temperature");
      const auto& scalarHandle = scalarField.GetData().AsArrayHandle<viskores::cont::ArrayHandle<double>>();
      auto drange = viskores::cont::ArrayRangeCompute(scalarHandle);
      auto range = drange.ReadPortal().Get(0);
      std::cout << i << " :range(temperature) = " << range << std::endl;

      viskores::cont::ArrayHandle<viskores::Range> drange;

      if (!inputData.HasField("temperature", viskores::cont::Field::Association::Points))
        {
        std::cerr << "Error: expected a temperature array. Did not get it." << std::endl;
        }
      else
        {
        if (range.Min != 0)
          std::cerr << "Unexpected temperature min. Got " << range.Min << std::endl;
        if (range.Max > 1.0)
          std::cerr << "Unexpected temperature max range. Got " << range.Max << std::endl;
      //std::cout << "range(temperature) = " << range << std::endl;
        }
*/
      viskores::rendering::Actor a = viskores::rendering::Actor(inputData, "temperature", colorTable);
      a.SetScalarRange({0.0, 1.0});
      mesh_actors.push_back(a);
/*
    viskores::filter::contour::Contour contour;
    contour.SetGenerateNormals(false);
    contour.SetMergeDuplicatePoints(true);
    contour.SetIsoValues({0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9});
    contour.SetActiveField("temperature");
    contour.SetFieldsToPass(viskores::filter::FieldSelection::Mode::All);
    viskores::cont::DataSet isolines = contour.Execute(inputData);

    viskores::filter::field_transform::PointTransform xform;
    xform.SetTranslation(viskores::Vec3f(0.0f, 0.0f, 0.00f));

    viskores::cont::DataSet isolines2 = xform.Execute(isolines);

    viskores::rendering::Actor b = viskores::rendering::Actor(isolines, "temperature",
                               viskores::rendering::Color(1.0f, 1.0f, 1.0f, 1.0f));
    mesh_actors.push_back(b);
*/
    //viskores::Bounds coordsBounds = inputData.GetCoordinateSystem().GetBounds();

    scene.AddActor(a);
    //scene.AddActor(b);
    }
    viskores::rendering::View3D view(scene, mapperWireframe, canvas);
    auto camera = view.GetCamera();

    camera.SetLookAt(viskores::Vec3f(0.5, 0.5, 0.0));
    camera.SetPosition(viskores::Vec3f(0.5, 0.5, 100.0));
    camera.SetViewUp(viskores::Vec3f(0.0, 1.0, 0.0));

    view.SetBackgroundColor(viskores::rendering::Color(0.0f, 0.0f, 0.0f));
    view.SetForegroundColor(viskores::rendering::Color(1.0f, 1.0f, 1.0f));

    view.Paint();
    view.RenderScreenAnnotations();
    std::string filename = "diffusion_step_" + std::format("{:03}", step++) + ".png";
    view.SaveAs(filename);
    //std::cout << __FILE__ << ":" << __LINE__ << ": File " << filename << " written, going to next iteration of infinite loop." << std::endl;
  }

  MPI_Finalize();
}
