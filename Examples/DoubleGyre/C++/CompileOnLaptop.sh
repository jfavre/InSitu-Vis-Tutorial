
cmake -B buildAscent -S . \
      -DINSITU=Ascent \
      -DAscent_DIR=/local/apps/Ascent/install/ascent-checkout/lib/cmake/ascent

cmake --build buildAscent

./buildAscent/bin/double_gyre_ascent 128 64 100 10

ll vort_mag.0* vel_mag.0*

=============================================================================
spack load libcatalyst
cmake -B buildCatalyst -S . \
      -DINSITU=Catalyst

cmake --build buildCatalyst

export CATALYST_IMPLEMENTATION_PATHS=/local/apps/ParaView/6.0/lib/catalyst

./buildCatalyst/bin/double_gyre_catalyst 128 64 10 ../Python/pvDoubleGyre.py

# check the contents of folder "datasets"
ll datasets
