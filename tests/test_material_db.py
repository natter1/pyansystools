"""
@author: Nathanael Jöhrmann
"""
import math

import pytest

from pyansystools.material import Material
from pyansystools.material_db import _Al, Si

materials = [_Al(), Si()]


def anisotrop_materials():
    """Get a list of all anisotrop materials"""
    result = []
    for material in materials:
        if (material.ey is not None) or (material.ez is not None):
            result.append(material)
    return result


@pytest.fixture(scope='function', params=["x", "y", "z"])
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


@pytest.fixture(scope='function', params=materials, ids=type)
def material(request):
    return request.param


@pytest.fixture(scope='function', params=anisotrop_materials(), ids=type)
def orthotropic_material(request):
    return request.param


def test_E(mapdl, material, bar):
    """Test Young's modulus from material by comparing with results of simulated bar compression test for x, y and z"""
    direction, pressure, aspect_ratio = bar
    #material = materials[material_name]
    material.set_elastic(mapdl, 1)
    mapdl.slashsolu()
    mapdl.solve()
    mapdl.finish()

    E_in = material.ex
    # in case of anisotropic material:
    if direction == "y" and material.ey is not None:
        E_in = material.ey
    elif direction == "z" and material.ez is not None:
        E_in = material.ez

    disp = mapdl.post_processing.nodal_displacement(direction)
    E_out = abs(pressure / (disp.min() / aspect_ratio))  # 0  # E modulus in comp direction

    assert (math.isclose(E_in, E_out, rel_tol=1e-02))


def test_linear_elastic_isotropic(material):
    """Test if all basic attributs are set (not None)"""
    assert (material.ex is not None) and (material.prxy is not None)


def test_linear_elastic_orthotropic(orthotropic_material):
    """If a material is orthotropic (Ex, Ey and Ez set), make sure shear modulus is set too."""
    m: Material = orthotropic_material
    assert m.ex is not None
    assert m.ey is not None
    assert m.ez is not None
    assert m.gxy is not None
    assert m.gyz is not None
    assert m.gzx is not None

