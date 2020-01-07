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

Class Rectangle
,,,,,,,,,,,,,,,
Geometry2d provides some basic functionality to handle 2D geometries. This class is meant to be subclassed for each specific geometry (like Rectangle).

Class Rectangle
,,,,,,,,,,,,,,,
.. code:: python

    import pyansys
    from pyansystools.geo2d import Rectangle

    mapdl = pyansys.Mapdl()

    rectangle = Rectangle(mapdl, b=10, h=30)
    rectangle.set_rotation_in_degree(45)
    rectangle.create()  # create keypoints, lines and area in ANSYS
    ...


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
