import pyansys
from pyansystools.geo2d import Rectangle


def main():
    example_geo2d_rectangle_01()

def example_geo2d_rectangle_01():
    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True,
                          jobname="example_geo2d_rectangle_01")

    rectangle = Rectangle(mapdl, b=10, h=30)
    rectangle.set_rotation_in_degree(45)
    rectangle.create()  # create keypoints, lines and area in ANSYS

    mapdl.pnum("KP", 1)
    mapdl.pnum("LINE", 1)
    mapdl.pnum("AREA", 1)
    mapdl.gplot()

    # mapdl.show("PNG")
    mapdl.exit()


if __name__ == '__main__':
    main()