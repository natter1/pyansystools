# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 15:03:12 2019

@author: Nathanael Jöhrmann
"""
import pytest
import geo2d


flag_create_plots = True

rotation_angle = 0.20
subs_width = 4
subs_height = 5
film_width = subs_width
film_height = 5
roi_width = 2
roi_height = 1


@pytest.fixture(scope='class')
def do_plot(setup_ansys):
    yield
    if flag_create_plots:
        plot(setup_ansys)


@pytest.fixture(scope='class')
def circle(setup_ansys, do_plot):
    circle = geo2d.Circle(setup_ansys, 1, 80)
    circle.create()
    yield circle


@pytest.fixture(scope='class')
def film_with_roi(setup_ansys, do_plot):
    film_with_roi = geo2d.FilmWithROI(setup_ansys, film_width, film_height,
                                      roi_width, roi_height, rotation_angle)
    film_with_roi.create()
    yield film_with_roi


def plot(ansys):
    ansys.allsel()
    ansys.pnum("KP", 1)
    ansys.pnum("LINE", 1)
    ansys.pnum("AREA", 1)
    ansys.gplot()


class TestCircle():
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


class TestFilmWithRoi():
    def test_lines(self, mapdl, film_with_roi):
        assert len(film_with_roi.lines) == 7
    def test_lines_ansys(self, mapdl):
        assert mapdl.get_float("LINE", 0, "COUNT") == 7
    def test_areas(self, mapdl, film_with_roi):
        assert len(film_with_roi.areas) == 2
    def test_areas_ansys(self, mapdl):
        assert mapdl.get_float("AREA", 0, "COUNT") == 2
    def test_mesh(self, mapdl, film_with_roi):
        pass


def test_film_with_roi_merged_to_rectangle(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height)
    subs.set_rotation(rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.FilmWithROI(mapdl, film_width, film_height,
                             roi_width, roi_height, rotation_angle, point)
    film.create_merged_to(subs)
    assert True


def test_rectangle_merged_with_rectangle(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create_merged_to(subs)
    assert True


def test_rectangle_on_rectangle_without_merge(mapdl):
    subs = geo2d.Rectangle(mapdl, subs_width, subs_height, rotation_angle)
    subs.create()

    point = geo2d.Point(subs.points[1].x, subs.points[1].y)
    film = geo2d.Rectangle(mapdl, subs_width, subs_height,
                           rotation_angle, point)
    film.create()
    assert True


def test_tip(mapdl):
    area_coefficients = [24.5, 0, 0, 0, 0, 0]
    tip = geo2d.Tip(mapdl, area_coefficients)
    tip.create()
    assert True
