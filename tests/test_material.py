"""
@author: Nathanael Jöhrmann
"""
import numpy as np
import pytest
from matplotlib import pyplot as plt

from pyansystools.material import Material


@pytest.fixture(scope='session')
def ramberg_osgood_material():
    m = Material()
    m.dens = 2.7E-9
    m.ex = 76220
    m.prxy = 0.32
    m.ro_n = 11.0
    m.ro_K = 1.79e25
    return m

@pytest.fixture(scope='function', params=["x"])
def bar(mapdl, request):
    """creates 3D beam including meshing and returns longest direction (x, y or z)"""
    pressure = 1e2
    aspect_ratio = 4  # higher aspect ratio gives smaller deviation between E_in and E_out, but longer solve-time

    mapdl.prep7()
    cube_dimensions = {"x": 1, "y": 1, "z": 1, request.param: aspect_ratio}

    mapdl.block(0, cube_dimensions["x"], 0, cube_dimensions["y"], 0, cube_dimensions["z"])
    mapdl.lesize("ALL", 0.25)
    mapdl.et(1,'SOLID186')
    mapdl.mshape(0, "3D")
    mapdl.mshkey(1)
    mapdl.vmesh('all')

    mapdl.nsel('s', 'loc', request.param, 0)
    mapdl.d('all', 'all', 0)
    mapdl.nsel('s', 'loc', request.param, aspect_ratio)
    mapdl.sf('all', 'pres', pressure)
    mapdl.allsel()
    return request.param, pressure, aspect_ratio


def strain_ramberg_osgood(stress, E, K, n):
    return stress/E + K * (stress/E)**n


def test_ramberg_osgood(mapdl, bar, ramberg_osgood_material):
    m = ramberg_osgood_material
    mat_id = 1
    m.set_ramberg_osgood(mapdl, mat_id, 0.1, 0.01)

    mapdl.tbplot("KINH", mat_id)

    # the returned array is 1D and has the stress-strain values at odd/even positions
    tb_kinh_data_raw = mapdl.get_array("KINH", mat_id, item1="TEMP", it1num=0, item2="CONST", it2num=0, kloop=6)

    # values from MAPDL
    strain = tb_kinh_data_raw[np.arange(0, len(tb_kinh_data_raw), 2)]
    stress = tb_kinh_data_raw[np.arange(1, len(tb_kinh_data_raw), 2)]
    strain = strain[strain != 0]
    stress = stress[stress != 0]
    plt.plot(strain, stress, '+')

    # values from theory (Ramberg Osgood)
    stress_ro = np.linspace(0, stress.max())
    plt.plot(strain_ramberg_osgood(stress_ro, m.ex, m.ro_K, m.ro_n), stress_ro)

    plt.show()






