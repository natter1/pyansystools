import time

import pyansys
from pyansystools.geo2d import Geometry2d, Point2D, Rectangle, Isogon


def main():
    example_geo2d_rectangle_01()
    time.sleep(1)  # short delay needed befor restart ANSYS
    example_geo2d_isogon_01()


# geometry2d is meant to be subclassed; it does not define any keypoints etc. to create
def example_geometry2d():
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
    geometry.set_element_type(183)


def example_geo2d_rectangle_01():
    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True,
                          jobname="example_geo2d_rectangle_01")

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


def example_geo2d_isogon_01():
    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True,
                          jobname="example_geo2d_isogon_01")

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


if __name__ == '__main__':
    main()
