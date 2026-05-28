
export PYTHONPATH=/local/apps/Ascent/install/conduit-v0.9.6/python-modules:/local/apps/Ascent/install/ascent-checkout/python-modules
export LD_LIBRARY_PATH=/local/apps/Ascent/install/ascent-checkout/lib:/local/apps/Ascent/install/viskores-1.1.1/lib
spack load py-matplotlib py-numpy

rm *png
python3 double_gyre_ascent.py

