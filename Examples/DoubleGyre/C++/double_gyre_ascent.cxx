#include <math.h>
#include <vector>
#include <algorithm>
#include <cassert>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>

#include "double_gyre_ascent.h"

#include "double_gyre.h"

#include <ascent/ascent.hpp>
#include "conduit_blueprint.hpp"

namespace AscentAdaptor
{
  ascent::Ascent ascent;
  conduit::Node mesh;
  conduit::Node actions; // default actions can also be overidden by file ascent_actions.yaml

  using double_gyre::simulation;
  
void Ascent_Initialize(int frequency)
{
  std::string output_path = "datasets";
  if(!conduit::utils::is_directory(output_path))
  {
    ASCENT_INFO("Creating output folder: " + output_path);
    conduit::utils::create_directory(output_path);
  }
  conduit::Node ascent_options;
  ascent_options["default_dir"] = output_path;
  ascent_options["ascent_info"] = "verbose";
  ascent_options["exceptions"] = "forward";
  ascent.open(ascent_options);
  mesh["coordsets/coords/type"] = "uniform";
  mesh["coordsets/coords/dims/i"] = simulation.xres;
  mesh["coordsets/coords/dims/j"] = simulation.yres;

  mesh["topologies/mesh/type"] = "uniform";
  mesh["topologies/mesh/coordset"] = "coords";

  mesh["coordsets/coords/origin/x"] = simulation.grid_bounds[0];
  mesh["coordsets/coords/origin/y"] = simulation.grid_bounds[2];
  mesh["coordsets/coords/spacing/dx"] = simulation.grid_bounds[1] / (simulation.xres - 1.0);
  mesh["coordsets/coords/spacing/dy"] = simulation.grid_bounds[3] / (simulation.yres - 1.0);

  mesh["fields/vx/association"] = "vertex";
  mesh["fields/vx/topology"] = "mesh";
  mesh["fields/vx/values"].set_external(simulation.vel_x);

  mesh["fields/vy/association"] = "vertex";
  mesh["fields/vy/topology"] = "mesh";
  mesh["fields/vy/values"].set_external(simulation.vel_y);
  
  mesh["fields/vz/association"] = "vertex";
  mesh["fields/vz/topology"] = "mesh";
  mesh["fields/vz/values"].set_external(simulation.vel_z);

  mesh["fields/Velocity/association"] = "vertex";
  mesh["fields/Velocity/topology"] = "mesh";
  mesh["fields/Velocity/values/u"].set_external(simulation.vel_x);
  mesh["fields/Velocity/values/v"].set_external(simulation.vel_y);
  mesh["fields/Velocity/values/w"].set_external(simulation.vel_z);

// verify the mesh we created conforms to the blueprint
  conduit::Node verify_info;
  if(!conduit::blueprint::mesh::verify(mesh, verify_info))
    std::cerr << "\nDoubleGyre Mesh Verify failed!" << std::endl;
  else{
    std::cerr << "\nDoubleGyre Mesh verify success!" << std::endl;
   //print(self.mesh.to_yaml())
  }

  conduit::Node &add_triggers = actions.append();
  add_triggers["action"] = "add_triggers";
  conduit::Node &triggers = add_triggers["triggers"];

  // add a simple trigger (t1_ that fires at the given frequency
  triggers["t1/params/condition"] = "cycle() % " + std::to_string(frequency) + " == 0";
  triggers["t1/params/actions_file"] = "save_images_actions.yaml";

  std::cout << actions.to_yaml() << std::endl;
};

void Ascent_Execute()
{
  mesh["state/cycle"] = simulation.iteration;
  ascent.publish(mesh);
  ascent.execute(actions);
};

void Ascent_Finalize()
{
  ascent.close();
};

};
