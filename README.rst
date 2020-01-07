pyansystools
============
.. image:: http://img.shields.io/:license-mit-blue.svg?style=flat-square
    :target: http://badges.mit-license.org

This module provides classes to simplify the work python module pyansys:
* Inline (easy python interface to use APDL inline functions)
* Geometry2d and its subclasses (create 2D geometries accesible as python objects)
* Macros (collection of common tasks available as methods)
* ...

Installation
------------
...pip install pyansystools
Prerequisites
.............
* Python >= 3.6
* `pyansys <https://github.com/akaszynski/pyansys>`


Quick Guide
-----------

Class Inline
............
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
