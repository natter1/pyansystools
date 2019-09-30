# -*- coding: utf-8 -*-
"""
Provides classes to create and handle 2D geometry models in ANSYS via pyansys

Classes:

    Point
    Geometry2d
    Square
    Film_with_roi

@author: Nathanael Jöhrmann
"""

import math
import copy


class Point:
    """
    Class representing a 2D point.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def shift_by(self, point):
        self.x += point.x
        self.y += point.y

    def get_list(self):
        return [self.x, self.y]

    def rotate_radians(self, angle):
        x = self.x * math.cos(angle) - self.y*math.sin(angle)
        y = self.x * math.sin(angle) + self.y*math.cos(angle)
        self.x = x
        self.y = y


class Geometry2d:
    """
    Geometry2d provides some basic functionality to handle 2D geometries
    using the module pyansys for ANSYS. This class is meant to be subclassed
    for each specific geometry (like Square).
    """
    def __init__(self, mapdl, rotation_angle, destination=Point(0, 0)):
        """
        Should be called inside subclasses __init__.
        """
        self._mapdl = mapdl
        self._rotation_angle = rotation_angle
        self._destination = copy.deepcopy(destination)

        self._raw_points = []  # basic positions of geometry
        self.points = []  # actual positions including rotation and shift
        self.keypoints = []  # ansys keypoint numbers
        self.lines = []  # ansys line numbers clockwise starting on left side
        self.areas = []  # ansys area numbers
        self.component_name = ''

    def _create_keypoints(self):
        """
        Creates Keypoints for the geometry in ansys. The number and position
        of them is defined by a subclass of Geometry2d inside _calc_points().
        Make sure you are in PREP7 befor calling this function.

        Parameters
        ----------

        Returns
        -------
        None.
        """
        for point in self.points:
            self.keypoints.append(self._mapdl.k("", *point.get_list()))

    def _create_keypoints_merged(self, geometry2d):
        """
        Creates Keypoints for the geometry in ansys. The number and position
        of them is defined by a subclass of Geometry2d inside _calc_points().
        Only Keypoints at positions not part of the geometry2d parameter are
        created. In case a keypoint position already exists in geometry2d,
        that keypoint is used instead, thus merging both geometries.
        Make sure you are in PREP7 befor calling this function.

        Parameters
        ----------
        geometry2d : Geometry2d
            Geometry to which the new area should be glued (sharing KPs/Lines).

        Returns
        -------
        None.
        """
        for point in self.points:
            found_keypoint = False
            for keypoint_number in geometry2d.keypoints:
                if self._check_keypoint_is_at_point(keypoint_number, point):
                    self.keypoints.append(keypoint_number)
                    found_keypoint = True
            if not found_keypoint:
                self.keypoints.append(self._mapdl.k("", *point.get_list()))

    def set_element_type(self, et):
        pass

    def set_material_number(self, mat):
        assert self.areas is not [], "Can't set material number without area"
        self._mapdl.prep7()
        self.asel("NONE")
        for area in self.areas:
            self._mapdl.asel("A", "AREA", area)
        self._mapdl.aatt(mat)

    def _calc_points(self):
        self.points = copy.deepcopy(self._raw_points)
        self._rotate_and_shift_points()

    def _rotate_and_shift_points(self):
        """
        this function is supposed to be called from _calc_points().
        It rotates points by rotation_angle and shifts them to destination.
        """
        self._rotate_points_by_rotation_angle()
        self._shift_points_to_destination()

    def _rotate_points_by_rotation_angle(self):
        """
        Rotates geometry by _rotation_angle (in radians).
        """
        for point in self.points:
            point.rotate_radians(self._rotation_angle)

    def _shift_points_to_destination(self):
        """
        Moves the default positions to their destination via _destination.
        """
        for point in self.points:
            point.shift_by(self._destination)

    def select_lines(self):
        """
        Selects all lines belonging to the geometry.
        """
        self._mapdl.lsel("none")
        for line_number in self.lines:
            self._mapdl.lsel("A", "LINE", "", line_number)

    def _check_keypoint_is_at_point(self, keypoint_number, point, tol=1e-6):
        """
        Checks if keypoint is at the position point.

        Parameters
        ----------
        keypoint_number : int
            Ansys keypoint number of the keypoint to check.

        point : Point
            Position where keypoint is expected.

        tol : float (optional)
            Absolute tolerance when comparing float values for x and y.
            Defaults to 1e-6
        Returns
        -------
        Boolean.
        """
        x = self._mapdl.get_float("KP", keypoint_number, "LOC", "X")
        y = self._mapdl.get_float("KP", keypoint_number, "LOC", "Y")
        return (math.isclose(x, point.x, abs_tol=tol)
                and math.isclose(y, point.y, abs_tol=tol))

    def set_destination(self, point):
        """
        Sets destination of geometry and recalc points.
        Use before calling create() or create_merged_to().
        Does not change already created data inside ANSYS.

        Parameters
        ----------
        point : Point
            Destination coordinates for geometry.
        """
        self._destination.x = point.x
        self._destination.y = point.y
        self._calc_points()

    def set_rotation(self, radians):
        """
        Sets rotation_angle of geometry and recalc points.
        Use before calling create() or create_merged_to().
        Does not change already created data inside ANSYS.

        Parameters
        ----------
        radians : float
            Rotation of geometry in radians.
        """
        self._rotation_angle = radians
        self._calc_points()

    def set_rotation_in_degree(self, rotation):
        """
        Sets rotation_angle of geometry and recalc points.
        Use before calling create() or create_merged_to().
        Does not change already created data inside ANSYS.

        Parameters
        ----------
        rotation : float
            Rotation of geometry in degrees.
        """
        self.set_rotation(rotation / 180 * math.pi)


class Rectangle(Geometry2d):
    """
    A rectangle geometry with 4 keypoints, 4 lines and one area.
    """
    def __init__(self, mapdl, b, h, rotation_angle=0, destination=Point(0, 0)):
        super().__init__(mapdl, rotation_angle,  destination)
        self._b = b
        self._h = h
        self._calc_raw_points()
        super()._calc_points()

    def _calc_raw_points(self):
        self._raw_points.clear()
        self._raw_points.append(Point(0, 0))
        self._raw_points.append(Point(0, self._h))
        self._raw_points.append(Point(self._b, self._h))
        self._raw_points.append(Point(self._b, 0))

    def _create_lines(self):
        kp_count = len(self.keypoints)
        for i in range(0, kp_count):
            kp1 = self.keypoints[i]
            kp2 = self.keypoints[(i+1) % kp_count]
            self.lines.append(self._mapdl.l(kp1, kp2))

    def create(self):
        self._mapdl.prep7()
        super()._create_keypoints()
        self._create_lines()
        self.areas.append(self._mapdl.al(*self.lines))

    def create_merged_to(self, geometry2d):
        """
        Use this to glue new area to another. Don't use lglue/aglue!
        That would also change KP-numbers, line numbers and area numbers
        inside ANSYS.

        Parameters
        ----------
        geometry2d : Geometry2d
            Geometry to which the new area should be glued (sharing KPs/Lines).

        Returns
        -------
        None.

        """
        super()._create_keypoints_merged(geometry2d)

        self._create_lines()
        self.areas.append(self._mapdl.al(*self.lines))


class Film_with_roi(Geometry2d):
    def __init__(self, mapdl, r, h, roi_width, roi_height,
                 rotation_angle=0, destination=Point(0, 0)):
        super().__init__(mapdl, rotation_angle, destination)
        self._r = r
        self._h = h
        self._roi_width = roi_width
        self._roi_height = roi_height
        self._calc_raw_points()
        self.film_lines = []
        self.roi_lines = []
        self.film_area = None
        self.roi_area = None
        super()._calc_points()

    def _calc_raw_points(self):
        self._raw_points.clear()
        self._raw_points.append(Point(0, 0))

        #  for line between film and roi:
        self._raw_points.append(Point(0, self._h-self._roi_height))
        support_point = Point()  # used to create spline
        support_point.x = 2/3*self._roi_width
        support_point.y = self._h-5/6*self._roi_height
        self._raw_points.append(support_point)
        self._raw_points.append(Point(self._roi_width, self._h))
        #  ------------------------------

        self._raw_points.append(Point(self._r, self._h))
        self._raw_points.append(Point(self._r, 0))

        #  for missing keypoint of roi:
        self._raw_points.append(Point(0, self._h))

    def _create_lines(self):
        self._create_film_lines()
        self._create_roi_lines()
        self.lines.extend(self.film_lines)
        self.lines.extend(self.roi_lines[:2])

    def _create_film_lines(self):
        k = self.keypoints

        self.film_lines.append(self._mapdl.l(k[0], k[1]))

        spline_line = self._mapdl.bsplin(k[1], k[2], k[3], "", "", "",
                                         -1, 0, 0,
                                         0, 1, 0)
        self.film_lines.append(spline_line)

        self.film_lines.append(self._mapdl.l(k[3], k[4]))
        self.film_lines.append(self._mapdl.l(k[4], k[5]))
        self.film_lines.append(self._mapdl.l(k[5], k[0]))

    def _create_roi_lines(self):
        k = self.keypoints

        self.roi_lines.append(self._mapdl.l(k[1], k[6]))
        self.roi_lines.append(self._mapdl.l(k[6], k[3]))
        self.roi_lines.append(self.film_lines[1])

    def create(self):
        self._mapdl.prep7()
        self._create_keypoints()
        self._create_lines()
        self.film_area = self._mapdl.al(*self.film_lines)
        self.roi_area = self._mapdl.al(*self.roi_lines)
        self.areas.append(self.film_area)
        self.areas.append(self.roi_area)

    def create_merged_to(self, geometry2d):
        """
        Use this to merge this geometry to another. Don't use lglue/aglue!
        That would also change keypoint numbers, line numbers and area numbers
        inside ANSYS.

        Parameters
        ----------
        geometry2d : Geometry2d
            Geometry to which the new area will merge (sharing keypoints).

        Returns
        -------
        None.

        """
        self._mapdl.prep7()
        self._create_keypoints_merged(geometry2d)
        self._create_lines()
        self.film_area = self._mapdl.al(*self.film_lines)
        self.roi_area = self._mapdl.al(*self.roi_lines)
