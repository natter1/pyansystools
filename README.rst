pyansystools
============
.. image:: https://img.shields.io/pypi/v/pyansystools.svg
    :target: https://pypi.org/project/pyansystools/

.. image:: http://img.shields.io/:license-MIT-blue.svg?style=flat-square
    :target: http://badges.MIT-license.org

This module provides classes to simplify use of python module pyansys:

* Inline (easy python interface to use APDL inline functions)
* Geometry2d and its subclasses (create 2D geometries accesible as python objects)
* Macros (collection of common tasks available as methods)
* ...

Installation
------------
pip install pyansystools

Prerequisites
.............
* Python >= 3.6
* `pyansys <https://github.com/akaszynski/pyansys>`


Examples
-----------

Module geo2d
............

Class Geometry2d
,,,,,,,,,,,,,,,,
Geometry2d provides some basic functionality to handle 2D geometries. This class is meant to be subclassed for each specific geometry (like Rectangle).

.. code:: python

    import pyansys
    from pyansystools.geo2d import Geometry2d, Point2D, Rectangle
    geometry = Geometry2d()

    # following methods do not change already created data inside ANSYS
    geometry.set_rotation(radians=1.0)
    geometry.set_rotation_in_degree(degrees=20.0)
    geometry.set_destination(point=Point2D(2, -3))

    geometry.create()  # this creates the keypoints, lines and areas in ANSYS
    # Warning: Changes to geometry won't be transfered to ANSYS after this call.
    # If you call create() a second time, a new geometry is created!

    # Beware! Some APDL-functions change keypoint numbers.
    # In current version, Geometry2D is not updated automatically.
    geometry.keypoints  # list of ANSYS keypoint numbers
    geometry.lines  # lit of ANSYS line numbers
    geometry.areas  # list of ANSYS area numbers

    geometry.select_lines()  # Selects all lines belonging to the geometry (deselecting all other lines).
    geometry.select_areas()  # Selects all areas belonging to the geometry (deselecting all other areas).

    geometry.set_material_number(mat=3)

All subclasses have to implement at least:
    * __init__()
    * _calc_raw_points()
    * a method for meshing

Look at class Rectangle for an easy example how to subclass correctly.

Class Rectangle
,,,,,,,,,,,,,,,
.. code:: python

    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True)

    rectangle = Rectangle(mapdl, b=10, h=30)
    rectangle.set_rotation_in_degree(45)
    rectangle.create()  # create keypoints, lines and area in ANSYS

    rectangle.set_element_type(mapdl.et("", "PLANE183"))
    rectangle.mesh(10)
    # or: rectangle.mesh_custom(...)

    mapdl.pnum("KP", 1)
    mapdl.pnum("LINE", 1)
    mapdl.pnum("AREA", 1)
    mapdl.gplot()

    mapdl.exit()

.. figure:: https://github.com/natter1/pyansystools/raw/master/docs/images/example_geo2d_rectangle_01.png
    :width: 500pt

Module inline
.............

Class Inline
,,,,,,,,,,,,,,,

This class enables access to most of ANSYS APDL inline-functions.

.. code:: python

    import pyansys
    from inline import Inline


    mapdl = pyansys.Mapdl()  # see pyansys for arguments
    inline = Inline(Mapdl)
    # ...

It also provides some convienient functions not part of APDL:

.. code:: python

    inline.kxyz(k: int) -> Point
    inline.lxyz(l: int, lfrac: float) -> Point
    inline.uxyz(, n: int) -> Point


License and Acknowledgments
---------------------------
``pyansystools`` is licensed under the MIT license.

This module, ``pyansystools`` makes no commercial claim over ANSYS whatsoever.


API Documentation
=================
