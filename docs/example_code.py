import pyansys
from pyansystools.geo2d import Geometry2d, Point2D, Rectangle


# geometry2d is meant to be subclassed; it does not define any keypoints etc. to create
def example_geometry2d():
    geometry = Geometry2d()

    # following methods do not change already created data inside ANSYS
    geometry.set_rotation(radians=1.0)
    geometry.set_rotation_in_degree(degrees=20.0)
    geometry.set_destination(point=Point2D(2, -3))

    geometry.create()  # this this creates the keypoints, lines and areas in ANSYS
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


def main():
    example_geo2d_rectangle_01()


def example_geo2d_rectangle_01():
    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True,
                          jobname="example_geo2d_rectangle_01")

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

    # mapdl.show("PNG")
    mapdl.exit()


if __name__ == '__main__':
    main()