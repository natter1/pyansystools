# -*- coding: utf-8 -*-
"""
Provides classes to create and handle 2D geometry models in ANSYS via pyansys

Classes:

    Point
    Point2D
    Geometry2d
    Square
    Film_with_roi

@author: Nathanael Jöhrmann
"""

import copy
import math

class Point:
    """
    Standard 3D point
    """
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def shift_by(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z

    def get_list(self):
        return [self.x, self.y, self.z]

class Point2D(Point):
    """
    Class representing a 2D point.
    """
    def __init__(self, x=0, y=0):
        super().__init__(x, y, z=0)

    def shift_by(self, point):
        super().shift_by(Point(self.x, self.y, z=0))

    def get_list(self):
        return [self.x, self.y]

    def rotate_radians(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x = x
        self.y = y


class Geometry2d:
    """
    Geometry2d provides some basic functionality to handle 2D geometries
    using the module pyansys for ANSYS. This class is meant to be subclassed
    for each specific geometry (like Square).
    """

    def __init__(self, mapdl, rotation_angle=0, destination=Point2D(0, 0)):
        """
        Should be called inside subclasses __init__.

        Parameters
        ----------
        mapdl : Mapdl
            Pyansys Mapdl object to control ANSYS.
        rotation_angle : float (optional)
            Angle about which the geometry should be rotated inside ANSYS.
            Rotation is done with axis in z through Geometry._destination.
            Default value = 0
        destination : Point2D
            Position inside ANSYS, where geometry should be created.
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
        self._mapdl.asel("NONE")
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

    def _mesh(self):
        """
        Should be called inside subclasses->mesh(). Meshes all areas.
        """
        self.select_areas()
        # AMESH Generates nodes and area elements within areas
        self._mapdl.amesh("ALL")

    def select_lines(self):
        """
        Selects all lines belonging to the geometry.
        """
        self._mapdl.lsel("none")
        for line_number in self.lines:
            self._mapdl.lsel("A", "LINE", "", line_number)

    def select_areas(self):
        """
        Selects all areas belonging to the geometry.
        """
        self._mapdl.asel("none")
        for area_number in self.areas:
            self._mapdl.asel("A", "AREA", "", area_number)

    def _check_keypoint_is_at_point(self, keypoint_number, point, tol=1e-6):
        """
        Checks if keypoint is at the position point.

        Parameters
        ----------
        keypoint_number : int
            Ansys keypoint number of the keypoint to check.

        point : Point2D
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
        point : Point2D
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


class Polygon(Geometry2d):
    """
    A polygonal geometry constructed with a list of points.
    The points should be given in a clockwise manner starting
    at bottom left. Also, the first point should be at (0,0) if
    it shall be used as origin point (for rotation and destination).
    There can be exceptions to this, for example when creating a circle.
    """

    def __init__(self, mapdl, raw_points,
                 rotation_angle=0, destination=Point2D(0, 0)):
        super().__init__(mapdl, rotation_angle, destination)
        self._raw_points = raw_points
        # calc_raw_points not needed here. But in future maybe use it,
        # to check, if points result in valid geometry (e.g. one area ...)
        # self._calc_raw_points()
        super()._calc_points()

    def _create_lines(self):
        kp_count = len(self.keypoints)
        for i in range(0, kp_count):
            kp1 = self.keypoints[i]
            kp2 = self.keypoints[(i + 1) % kp_count]
            self.lines.append(self._mapdl.l(kp1, kp2))

    def _create_area(self):
        super().select_lines()
        self.areas.append(self._mapdl.al("ALL"))

    def create(self):
        self._mapdl.prep7()
        self._create_keypoints()
        self._create_lines()
        self._create_area()

    def mesh(self, nir):
        """
        Default meshing for polygons.
        The parameter nir sets number of divisions for each line.
        For more customized meshing, use mesh_custom in a subclass.
        """
        self._mapdl.prep7()
        super().select_lines()
        for line in self.lines:
            self._mapdl.lesize(line, "", "", nir)
            super()._mesh()

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
        self._create_area()


class Rectangle(Polygon):
    """
    A rectangle geometry with 4 keypoints, 4 lines and one area.
    """

    def __init__(self, mapdl, b, h, rotation_angle=0, destination=Point2D(0, 0)):
        # super().__init__(mapdl, rotation_angle,  destination)
        self._b = b
        self._h = h
        self._calc_raw_points()
        super().__init__(mapdl, self._raw_points, rotation_angle, destination)

    def _calc_raw_points(self):
        self._raw_points = []
        self._raw_points.append(Point2D(0, 0))
        self._raw_points.append(Point2D(0, self._h))
        self._raw_points.append(Point2D(self._b, self._h))
        self._raw_points.append(Point2D(self._b, 0))

    def mesh_custom(self, ndiv_width, ndiv_height, ratio_width=1, ratio_heigh=1):
        self._mapdl.prep7()
        super().select_lines()
        self._mapdl.lesize(self.lines[0], "", "", ndiv_height, ratio_heigh)
        self._mapdl.lesize(self.lines[2], "", "", ndiv_height, 1 / ratio_heigh)
        self._mapdl.lesize(self.lines[1], "", "", ndiv_width, ratio_width)
        self._mapdl.lesize(self.lines[3], "", "", ndiv_width, 1 / ratio_width)
        super()._mesh()


class Circle(Polygon):
    """
    A circle geometry approximation with parts lines.
    """

    # todo: better name for parts
    def __init__(self, mapdl, radius, parts,
                 rotation_angle=0, destination=Point2D(0, 0)):
        self._r = radius
        self._parts = parts
        self._calc_raw_points()
        super().__init__(mapdl, self._raw_points, rotation_angle, destination)

    def _calc_raw_points(self):
        self._raw_points = []
        # x = -self._r
        # y = 0
        for i in range(self._parts):
            # start left -> x = -r*cos(a)
            x = -self._r * math.cos(i * (2 * math.pi / self._parts))
            y = self._r * math.sin(i * (2 * math.pi / self._parts))
            self._raw_points.append(Point2D(x, y))


class FilmWithROI(Geometry2d):
    def __init__(self, mapdl, radius, height, roi_width, roi_height,
                 rotation_angle=0, destination=Point2D(0, 0)):
        super().__init__(mapdl, rotation_angle, destination)
        self._r = radius
        self._h = height
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
        self._raw_points.append(Point2D(0, 0))

        #  for line between film and roi:
        self._raw_points.append(Point2D(0, self._h - self._roi_height))
        support_point = Point2D()  # used to create spline
        support_point.x = 2 / 3 * self._roi_width
        support_point.y = self._h - 5 / 6 * self._roi_height
        self._raw_points.append(support_point)
        self._raw_points.append(Point2D(self._roi_width, self._h))
        #  ------------------------------

        self._raw_points.append(Point2D(self._r, self._h))
        self._raw_points.append(Point2D(self._r, 0))

        #  for missing keypoint of roi:
        self._raw_points.append(Point2D(0, self._h))

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
        self.areas.append(self.film_area)
        self.areas.append(self.roi_area)

    # todo: use parameter!
    def mesh(self, nir):
        self._mapdl.prep7()
        super().select_lines()
        # ROI - indent region
        self._mapdl.lesize(self.roi_lines[0], "", "", 2 * nir, 0, "", "", "", 1)
        self._mapdl.lesize(self.roi_lines[1], "", "", 6 * nir, -0.25, "", "", "", 1)
        self._mapdl.lesize(self.roi_lines[2], "", "", 2 * nir, -5, "", "", "", 1)

        # outer region
        self._mapdl.lesize(self.film_lines[0], "", "", 5 * 2 + 4, 0.1, "", "", "", 1)
        self._mapdl.lesize(self.film_lines[2], "", "", 15 + 4, 25, "", "", "", 1)
        self._mapdl.lesize(self.film_lines[3], "", "", 3, "", "", "", "", 1)
        self._mapdl.lesize(self.film_lines[4], "", "", 16 + 4, 10, "", "", "", 1)
        super()._mesh()


class Tip(Geometry2d):
    """
    Half of a sharp tip as used for nanoindentation (axisymmetric model).
    The shape is defined via coeff. of an area-function (polynom-fit).
    """

    def __init__(self, mapdl, shape_coefficients,
                 rotation_angle=0, destination=Point2D(0, 0)):
        """
        Initilize Tip-Instance and calculate points.
            Parameters
            ----------
            mapdl : Mapdl
                Pyansys Mapdl object to control ANSYS.
            shape_coefficients : list of floats
                Contains the polynom coefficients, that describe the tip shape
                via an area function (common in nanoindentation)
            rotation_angle : float (optional)
                Angle about which the geometry should be rotated inside ANSYS.
                Rotation is done with axis in z through Geometry._destination.
                Default value = 0
            destination : Point2D
                Position inside ANSYS, where geometry should be created.
        """
        super().__init__(mapdl, rotation_angle, destination)
        # todo: add parameter for area fit function
        self._shape_coefficients = shape_coefficients
        self._n_splines = 20
        # make sure, _n_splines is of form 5*n+1 !
        self._n_splines = (self._n_splines // 5) * 5 + 1
        self._calc_raw_points()
        super()._calc_points()

    def _calc_raw_points(self):
        self._raw_points.clear()

        self._raw_points.append(Point2D(0, 0))
        self._raw_points.append(Point2D(0, 1500))
        self._raw_points.append(Point2D(self._calc_tip_radius(1000), 1500))

        for i in reversed(range(1, self._n_splines + 1)):
            y = 1000 * pow(i / self._n_splines, 2)
            self._raw_points.append(Point2D(self._calc_tip_radius(y), y))

    def _create_lines(self):
        k = self.keypoints
        self.lines.append(self._mapdl.l(k[0], k[1]))
        self.lines.append(self._mapdl.l(k[1], k[2]))
        self.lines.append(self._mapdl.l(k[2], k[3]))

        for i in range(3, len(k) - 1, 5):
            keypoints = [k[i], k[i + 1], k[i + 2], k[i + 3], k[i + 4], k[i + 5]]
            self.lines.append(self._mapdl.bsplin(*keypoints))
        keypoints = [k[i + 5], k[0], "", "", "", ""]
        self.lines.append(self._mapdl.bsplin(*keypoints, "", "", "", -1))

    def select_spline_lines(self):
        """
        Selects all lines belonging to the spline shape.
        """
        self._mapdl.lsel("none")
        for line_number in self.lines[3:len(self.lines)]:
            self._mapdl.lsel("A", "LINE", "", line_number)

    # =============================================================================
    #         self._mapdl.lsel("S", "LINE", "", self.lines[3],
    #                  self.lines[len(self.lines)-1])
    # =============================================================================

    def create(self):
        self._mapdl.prep7()
        super()._create_keypoints()
        self._create_lines()
        self.select_lines()
        self.areas.append(self._mapdl.al("ALL"))

        self.select_spline_lines()

        # concatenate splines in preparation for mapped meshing
        # (needed to be done after creating area ?)
        self._mapdl.lccat("ALL")

    def mesh(self):
        self._mapdl.prep7()
        super().select_lines()
        self._mapdl.lesize(self.lines[0], "", "", 7, 4)  # , 11 ,7
        self._mapdl.lesize(self.lines[1], "", "", 25, "")  # 85 (,)
        self._mapdl.lesize(self.lines[2], "", "", 3)
        super()._mesh()

    # todo: better function name!
    def _calc_tip_radius(self, i):
        """
        calc radius of tip-area for a given indentation depth
        (using area function from experiment
        and y=mx**0.5 fit for very small indents)
        parameter:
            i: indentation depth
        """

        def use_area_function(i):
            ac = self._shape_coefficients
            return ((ac[0] * i ** 2 + ac[1] * i + ac[2] * i ** 0.5 + ac[3] * i ** 0.25
                     + ac[4] * i ** 0.125 + ac[5] * i ** 0.0625) / math.pi) ** 0.5

        assert i >= 0, "Indentation depth must be >=0 for calc_tip_radius"

        # todo: min_r should become more visible -> variable of myansys?
        # Part of input file? Calc useful value somehow?
        # 31 ... from exp. calibration
        # -> smallest indentation depth where areafunction is valid
        min_fitted_i = 31

        if i >= min_fitted_i:  # use experimental area fit function
            return use_area_function(i)
        # use simple fit with y=mx**2
        m = use_area_function(min_fitted_i) / (min_fitted_i ** 0.5)  # m = y/x**0.5
        return m * i ** 0.5
