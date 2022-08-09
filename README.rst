pyansystools
============
.. image:: https://img.shields.io/pypi/v/pyansystools.svg
    :target: https://pypi.org/project/pyansystools/

.. image:: http://img.shields.io/:license-MIT-blue.svg?style=flat-square
    :target: http://badges.MIT-license.org

This module provides classes to simplify use of python module pyansys:

* Inline (easy python interface to use APDL inline functions)
* Geometry2d and its subclasses (create 2D geometries accesible as python objects)
* Material
* Macros (collection of common tasks available as methods)
* ...

Installation
------------
Installation through pip::

    pip install pyansystools

Prerequisites
.............
* Python >= 3.6
* `pyansys <https://github.com/akaszynski/pyansys>`_


Quick Guide
-----------
At this point, pyansystools has three different modules:

inline.py
.........
This module implements the APDL inline functions as methods of class Inline.
As this functionality is now part of PyMAPDL, this module is deprecated.

.. code:: python

    import pyansys
    from inline import Inline


    mapdl = pyansys.Mapdl()  # see pyansys for arguments
    inline = Inline(Mapdl)
    # ...

In many cases those functions provide an alternative to the more complicated \*get function
for specific values. To get an overview of implemented inline functions (including a short description)
you could use the help function:

.. code:: python

    from pyansystools import inline
    help(inline.Inline)


For some inline functions that ask for x, y or z values Inline has aditional methods not part of APDL
to get all three values in one call:

.. code:: python

    inline.kxyz(k: int) -> Point  # for more information on Point see geo2d.py
    inline.lxyz(l: int, lfrac: float) -> Point
    inline.uxyz(, n: int) -> Point

Because inline functions can not run on its own in APDL, the Inline class needs to create (or overwrite) an APDL parameter '__INLINE__' to get the return values.


geo2d.py
........
The geo2d module provides classes to help create 2D geometries in a human readable way.

|

**class Point and class Point2D**

To work with coordinates, geo2d provides two classes - Point for 3D and Point2D for 2D. Both are iterable,
so you can do e.g.:

.. code:: python

    from pyansystools import inline

    x, y, z = inline.kxyz(5)  # kxyz() returns a Point-instance

|

**class Geometry2d**

Geometry2d provides some basic functionality to handle 2D geometries.
This class is meant to be subclassed for each specific geometry (like Rectangle).

.. code:: python

    mapdl = pyansys.Mapdl()
    geometry = Geometry2d(mapdl)
    # or with optional parameters:
    geometry = Geometry2d(mapdl, rotation_angle=0.5, destination=Point2D(0, 1))

    # following methods do not change already created data inside ANSYS
    geometry.set_rotation(radians=1.0)
    geometry.set_rotation_in_degree(degrees=20.0)
    geometry.set_destination(point=Point2D(2, -3))

    geometry.create()  # this creates the keypoints, lines and areas in ANSYS.
    # Note: Geometry2d does not implement create(), but enforces this method to all subclasses
    # Warning: Changes to geometry won't be transfered to ANSYS after this call.
    # If you call create() a second time, a new geometry or an error is created!

    # Beware! Some APDL functions change keypoint numbers.
    # In current version, Geometry2D is not updated automatically.
    # Make sure to use below methods/attributes before such changes.

    geometry.keypoints  # list of ANSYS keypoint numbers
    geometry.lines  # lit of ANSYS line numbers
    geometry.areas  # list of ANSYS area numbers

    geometry.select_lines()  # Selects all lines belonging to the geometry (deselecting all other lines).
    geometry.select_areas()  # Selects all areas belonging to the geometry (deselecting all other areas).

    geometry.set_material_number(mat=3)
    geometry.set_element_type(mapdl.et("", 183))

All subclasses have to implement at least:
    * __init__()
    * create()
    * _calc_raw_points()
    * a method for meshing

Geometry2D provides many more methods, that are meant to be called from inside a subclass.
Look at class Rectangle for an easy example how to subclass correctly.

|

**class Polygon**

A polygonal geometry constructed with a list of points. The points should be given in a clockwise manner starting
at bottom left.

.. code:: python

    import pyansys
    from pyansystools.geo2d import Rectangle

    mapdl = pyansys.Mapdl()
    # there are several ways to give the list of points.
    # It should work, as long as each point can be unpacked in 2 coordinates.
    points = [Point2D(0, 0), Point2D(0, 3), Point2D(2, 4), Point2D(2.5, 1)]
    points = [(0, 0), (0, 3), (2, 4), (2.5, 1)]
    points = [[0, 0], [0, 3], [2, 4], [2.5, 1]]

    polygon = Polygon(mapdl, points)
    # ...

|

**class Rectangle**

.. code:: python

    rectangle = Rectangle(mapdl, width=10, height=24.5)

|

**class Isogon**

Creates an Isogon (regular polygon) geometry.

.. code:: python

    pentagon = Isogon(mapdl, circumradius=10, edges=5)


macros.py
.........
Collection of macro-like functions for APDL ANSYS via pyansys.
Up till now, there are only macros to create contact pairs for lines (symmetric or asymmetric).
Suggestions for more macros are welcome.

Examples
--------
Created and mesh a rotated rectangle
....................................
.. code:: python

    import pyansys
    from pyansystools.geo2d import Rectangle

    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True)

    rectangle = Rectangle(mapdl, width=10, height=30)
    rectangle.set_rotation_in_degree(45)

    rectangle.create()  # create keypoints, lines and area in ANSYS

    rectangle.set_element_type(mapdl.et("", 183))
    rectangle.mesh(10)
    # or: rectangle.mesh_custom(...)

    mapdl.pnum("KP", 1)
    mapdl.pnum("LINE", 1)
    mapdl.pnum("AREA", 1)
    mapdl.gplot()

    mapdl.exit()

.. figure:: https://github.com/natter1/pyansystools/raw/master/docs/images/example_geo2d_rectangle_01.png
    :width: 500pt

Isogon with several rectangles (not merged)
...........................................
.. code:: python

    import pyansys
    from pyansystools.geo2d import Rectangle, Isogon

    radius = 40
    edges = 12
    isogon = Isogon(mapdl, radius, edges)
    isogon.create()
    rectangles = []

    for i, rotation in enumerate(range(0, 359, round(360/edges))):
        rectangle = Rectangle(mapdl, width=30, height=10)
        rectangles.append(rectangle)
        rectangle.set_destination(isogon.points[i])
        rectangle.set_rotation_in_degree(180-rotation+(180/edges))
        rectangle.create()  # create keypoints, lines and area in ANSYS

    mapdl.gplot()
    mapdl.exit()

.. figure:: https://github.com/natter1/pyansystools/raw/master/docs/images/example_geo2d_isogon_01.png
    :width: 500pt

Isogon with several rectangles (merged)
...........................................

...

Usage of Inline
...............

...

License and Acknowledgments
---------------------------
``pyansystools`` is licensed under the MIT license.

This module, ``pyansystools`` makes no commercial claim over ANSYS whatsoever.
