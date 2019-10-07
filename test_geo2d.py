# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:03:12 2019

@author: natj
"""
import re
import pyansys
import time
import os

import geo2d


rotation_angle = 0.20
subs_width = 4
subs_height = 5
film_width = subs_width
film_height = 5
roi_width = 2
roi_height = 1


def main():  # called at end of file if __name__ == "__main__"
    path = os.getcwd()
    mapdl = pyansys.Mapdl(override=True, interactive_plotting=True,
                          run_location=path)

    test_circle(mapdl)
    plot(mapdl)
# =============================================================================
#     test_film_with_roi(mapdl)
#     plot(mapdl)
#     test_film_with_roi_merged_to_rectangle(mapdl)
#     plot(mapdl)
#     test_rectangle_merged_with_rectangle(mapdl)
#     plot(mapdl)
#     test_rectangle_on_rectangle_without_merge(mapdl)
#     plot(mapdl)
#     test_tip(mapdl)
#     plot(mapdl)
# =============================================================================

    mapdl.open_gui()
    mapdl.exit()


def plot(mapdl):
    mapdl.allsel()
    mapdl.pnum("KP", 1)
    mapdl.pnum("LINE", 1)
    mapdl.pnum("AREA", 1)
    mapdl.gplot()


def test_circle(mapdl):
    mapdl.clear()
    circle = geo2d.Circle(mapdl, 1, 80)
    circle.create()
    mapdl.et("", "PLANE183")
    mapdl.mshkey(2)
    circle.mesh(2)


def test_film_with_roi(mapdl):
    mapdl.clear()
    film = geo2d.Film_with_roi(mapdl, film_width, film_height,
                               roi_width, roi_height, rotation_angle)
    film.create()


def test_film_with_roi_merged_to_rectangle(mapdl):
    mapdl.clear()
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height)
    subs.set_rotation(rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.Film_with_roi(mapdl, film_width, film_height,
                               roi_width, roi_height, rotation_angle, point)
    film.create_merged_to(subs)


def test_rectangle_merged_with_rectangle(mapdl):
    mapdl.clear()
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create_merged_to(subs)


def test_rectangle_on_rectangle_without_merge(mapdl):
    mapdl.clear()
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create()


def test_tip(mapdl):
    mapdl.clear()
    area_coefficients = [24.5, 0, 0, 0, 0, 0]
    tip = geo2d.Tip(mapdl, area_coefficients)
    tip.create()
# =============================================================================
# from pyansys import examples
# for i in range(1, int(10e5)):
#     examples.ansys_cylinder_demo(plot_vtk=False)
#     time.sleep(1)
#     print(i)
# =============================================================================


# =============================================================================
# from pyansys import examples
# examples.ansys_cylinder_demo()
# =============================================================================


if __name__ == "__main__":
    main()
