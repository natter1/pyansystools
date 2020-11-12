# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:03:12 2019

@author: Nathanael Jöhrmann
"""
import pytest
import pyansystools.geo2d as geo2d


flag_create_plots = True

rotation_angle = 0.20
subs_width = 4
subs_height = 5
film_width = subs_width
film_height = 5
roi_width = 2
roi_height = 1


@pytest.fixture(scope='class')
def do_plot(ansys):
    yield
    if flag_create_plots:
        plot(ansys)


@pytest.fixture(scope='class')
def circle(ansys, do_plot):
    circle = geo2d.Isogon(ansys, 1, 80)
    circle.create()
    yield circle


@pytest.fixture(scope='class')
def film_with_roi(ansys, do_plot):
    film_with_roi = geo2d.FilmWithROI(ansys, film_width, film_height,
                                      roi_width, roi_height, rotation_angle)
    film_with_roi.create()
    #    film_with_roi.mesh(11)
    yield film_with_roi


@pytest.fixture(scope='class')
def tip(ansys, do_plot):
    area_coefficients = [24.5, 0, 0, 0, 0, 0]
    tip = geo2d.Tip(ansys, area_coefficients)
    tip.create()
    yield tip


def plot(ansys):
    ansys.allsel()
    ansys.pnum("KP", 1)
    ansys.pnum("LINE", 1)
    ansys.pnum("AREA", 1)
    ansys.gplot()


class TestPoint:
    def test_iterate(self):
        point = geo2d.Point(1, 2, 3)
        x, y, z = point
        assert (x, y, z) == (1, 2, 3)

    def test_equal(self):
        point = geo2d.Point(1, 2, 3)
        assert point == geo2d.Point(1, 2, 3)
        assert point != geo2d.Point(1, 2, 4)
        assert NotImplemented == point.__eq__((1, 2, 3))

    def test_shift_by(self):
        point = geo2d.Point(1, 2, 3)
        point.shift_by((-1, -2, -3))
        assert point == geo2d.Point(0, 0, 0)
        point.shift_by(geo2d.Point(0, 0, 1))
        assert point.z == 1

    def test_get_list(self):
        point = geo2d.Point(1, 2, 3)
        my_list = point.get_list()
        assert my_list == [1, 2, 3]


class TestGeometry2D:
    def test_abstract_class(self, mapdl):
        with pytest.raises(TypeError):  # abstract class
            geometry = geo2d.Geometry2d(mapdl)

    def test_set_element_type(self, mapdl):
        geometry = geo2d.Rectangle(mapdl, 2, 2)
        geometry.create()
        geometry.set_element_type(mapdl.et("", "PLANE183"))
        geometry.mesh_custom(2, 2, 2, 2)  # meshing causes exception, if no et set
        assert True


class TestRectangle:
    def test_mesh_custom(self, mapdl):
        rectangle = geo2d.Rectangle(mapdl, 2, 2)
        rectangle.create()
        mapdl.et("", "PLANE183")
        rectangle.mesh_custom(2,2,2,2)
        assert True


class TestCircle:
    def test_lines(self, mapdl, circle):
        assert len(circle.lines) == 80

    def test_lines_ansys(self, mapdl):
        assert mapdl.get_float("LINE", 0, "COUNT") == 80

    def test_areas(self, mapdl, circle):
        assert len(circle.areas) == 1

    def test_areas_ansys(self, mapdl):
        assert mapdl.get_float("AREA", 0, "COUNT") == 1

    def test_mesh(self, mapdl, circle):
        mapdl.et("", "PLANE183")
        mapdl.mshkey(2)
        circle.mesh(2)
        assert True


class TestFilmWithRoi:
    def test_lines(self, mapdl, film_with_roi):
        assert len(film_with_roi.lines) == 8

    def test_lines_ansys(self, mapdl):
        assert mapdl.get_float("LINE", 0, "COUNT") == 8

    def test_areas(self, mapdl, film_with_roi):
        assert len(film_with_roi.areas) == 2

    def test_areas_ansys(self, mapdl):
        assert mapdl.get_float("AREA", 0, "COUNT") == 2

    def test_mesh(self, mapdl, film_with_roi):
        mapdl.et("", "PLANE183")
        mapdl.mshkey(2)
        film_with_roi.mesh(22)
        assert True


class TestTip:
    def test_lines(self, mapdl, tip):
        assert len(tip.lines) == 8

    def test_lines_ansys(self, mapdl):
        assert mapdl.get_float("LINE", 0, "COUNT") == 6

    def test_areas(self, mapdl, tip):
        assert len(tip.areas) == 1

    def test_areas_ansys(self, mapdl):
        assert mapdl.get_float("AREA", 0, "COUNT") == 1

    def test_mesh(self, mapdl, tip):
        mapdl.et("", "PLANE183")
        mapdl.mshkey(2)
        tip.mesh()
        assert True


def test_film_with_roi_merged_to_rectangle(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height)
    subs.set_rotation(rotation_angle)
    subs.create()

    point = geo2d.Point2D(subs.points[1].x, subs.points[1].y)
    film = geo2d.FilmWithROI(mapdl, film_width, film_height,
                             roi_width, roi_height, rotation_angle, point)
    film.create_merged_to(subs)
    assert True


def test_rectangle_merged_with_rectangle(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point2D(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create_merged_to(subs)
    assert True


def test_rectangle_on_rectangle_without_merge(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point2D(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create()
    assert True
