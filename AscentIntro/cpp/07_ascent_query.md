# Ascent query Example

- https://ascent.readthedocs.io/en/latest/Tutorial_Intro_Queries.html
    - [C++ example](###ascent_query_example1.cpp)
    - [Yaml actions](###ascent_actions.yaml)
    - [Outputs](####Outputs)
    - [Alps](###Build-and-run-on-Alps)

## Asking and answering questions with Queries

Queries are a way to ask summarization questions about meshes. Queries results
can be used with Triggers to adapt analysis and visualization actions. This
section shows how to execute queries with Ascent and access query results.

### ascent_query_example1.cpp

The [ascent_query_example1.cpp][cpp1] example code is a minimal example of
extracting mesh cycle and entropy of a time varying [mesh].

[cpp1]: https://github.com/Alpine-DAV/ascent/blob/develop/src/examples/tutorial/ascent_intro/cpp/ascent_query_example1.cpp
[mesh]: https://github.com/Alpine-DAV/ascent/blob/develop/src/examples/tutorial/ascent_intro/cpp/ascent_tutorial_cpp_utils.hpp#L84

```cpp
    Ascent a; // create an Ascent instance
    a.open(); // open ascent

    Node actions; // create a Conduit node of actions
    Node &add_act = actions.append();
    add_act["action"] = "add_queries";

    // add a simple query expression (q1)
    queries["q1/params/expression"] = "cycle()";;
    queries["q1/params/name"] = "cycle";

    // add a more complex query expression (q2)
    queries["q2/params/expression"] = "entropy(histogram(field('gyre'), num_bins=128))";
    queries["q2/params/name"] = "entropy_of_gyre";

    // declare a scene to render the dataset
    Node &add_scenes = actions.append();
    add_scenes["action"] = "add_scenes";
    Node &scenes = add_scenes["scenes"];
    scenes["s1/plots/p1/type"] = "pseudocolor";
    scenes["s1/plots/p1/field"] = "gyre";   // <---
    scenes["s1/image_name"] = "out_gyre";   // output file name (ascent will add ".png")
    // [...]
    for( int step =0; step < nsteps; step++) {
        tutorial_gyre_example(time_value, mesh); // generate a gyre mesh varying with time
        mesh["state/cycle"] = 100 + step * 100;
        mesh["state/cycle"] = cycle;
        std::cout << "time: " << time_value << " cycle: " << cycle << std::endl; 
        a.publish(mesh); // publish mesh to ascent
        scenes["s1/image_name"] = [...] ; // update image name
        a.execute(actions);
        Node ts_info; a.info(ts_info); // query the results
        info["expressions"].update(ts_info["expressions"]); // <---
        time_value = time_value + delta_time; // update time
    }
    a.execute(actions); // execute the actions
    a.close(); // close ascent
    // view the results of the cycle query
    std::cout << info["expressions/cycle"].to_yaml() << std::endl;
```

#### ascent_actions.yaml

```yaml
-
  action: "add_queries"
  queries:
    q1:
      params:
        expression: "cycle()"
        name: "cycle"
    q2:
      params:
        expression: "entropy(histogram(field('gyre'), num_bins=128))"
        name: "entropy_of_gyre"
-
  action: "add_scenes"
  scenes:
    s1:
      plots:
        p1:
          type: "pseudocolor"
          field: "gyre"
      image_name: "out_gyre"
```

#### Outputs

- ascent_query_example1.cpp -> .png + query results

![ex1](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMG9zZjE5OHVtbTN3b2FxMXQxMXNzZmE4ejRmenU2NWQwNmpkYmlodiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/f2k3UwqMXjKCZy3IJk/giphy.gif)

```
[...]
time: 4.5 cycle: 1000

type: "histogram"
attrs:
  value:
    value: [2.0, 2.0, 0.0, ..., 32.0, 32.0]
    type: "array"
  min_val:
    value: 0.0
    type: "double"
  max_val:
    value: 0.314159265359
    type: "double"
  num_bins:
    value: 128
    type: "int"
  clamp:
    value: 1
    type: "bool"
[...]
```

and

```
├── out_gyre_0000.png
├── out_gyre_0001.png
├── out_gyre_0002.png
├── out_gyre_0003.png
├── out_gyre_0004.png
├── out_gyre_0005.png
├── out_gyre_0006.png
├── out_gyre_0007.png
├── out_gyre_0008.png
└── out_gyre_0009.png
```

### Build and run on Alps

```sh
uenv image pull build::insitu_ascent/0.9.5:2109123735@daint
uenv start -v default insitu_ascent/0.9.5:2109123735

cp -a /user-tools/linux-neoverse_v2/ascent-0.9.5-*/examples/ascent/tutorial/ascent_intro/cpp .
cd cpp

make ASCENT_DIR=/user-tools/env/default/ ascent_query_example1

L1=/user-tools/linux-neoverse_v2/cray-gtl-8.1.32-25u7zwci35lms4zyrodhf24vlfken7xo/lib

LD_LIBRARY_PATH=$L1:$LD_LIBRARY_PATH ./ascent_query_example1
```

