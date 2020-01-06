"""
Provides a class to directly use inline-functions in ANSYS via pyansys
Creates/overwrites ANSYS-Paramter `__inline__'!
@author: Nathanael Jöhrmann
"""

import re
from enum import IntEnum

import pyansys

from pyansystools.geo2d import Point as Point


class Status(IntEnum):
    """
    Enumeration for Status Information to use with Inline.
    """
    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1


class Inline:
    def __init__(self, mapdl: pyansys.Mapdl):
        assert isinstance(mapdl, pyansys.Mapdl)
        self._mapdl = mapdl

    def _read_inline(self, inline_function: str):
        """
        Use an Inline-Function and return its value.

        :param inline_function: String containing the complete inline-function
        :return: float
        """
        line = self._mapdl.run(f"__inline__={inline_function}")
        return float(re.search(r"(?<=__INLINE__ =).*", line).group(0))

    # ========================================================================
    # ============================ entity status =============================
    # ========================================================================
    def nsel(self, n: int) -> Status:
        """
        Status of node n (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param n: node number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"nsel({n})")
        return Status(result)

    def esel(self, e: int) -> Status:
        """
        Status of element e (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param e: element number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"esel({e})")
        return Status(result)

    def ksel(self, k: int) -> Status:
        """
        Status of keypoint k (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param k: keypoint number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"ksel({k})")
        return Status(result)

    def lsel(self, l: int) -> Status:
        """
        Status of line l (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param l: line number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"lsel({l})")
        return Status(result)

    def asel(self, a: int) -> Status:
        """
        Status of area a (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param a: area number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"asel({a})")
        return Status(result)

    def vsel(self, v: int) -> Status:
        """
        Status of volume v (UNSELECTED==-1, UNDEFINED==0, SELECTED==1)

        :param v: volume number in ANSYS
        :return: Status
        """
        result = self._read_inline(f"vsel({v})")
        return Status(result)

    # ========================================================================
    # ========================= next selected entity =========================
    # ========================================================================
    def ndnext(self, n: int) -> int:
        """
        Next selected node having a node number greater than n

        :param n: int
        :return: int
        """
        result = self._read_inline(f"ndnext({n})")
        return int(result)

    def elnext(self, e: int) -> int:
        """
        Next selected element having an element number greater than e.

        :param e: int
        :return: int
        """
        result = self._read_inline(f"elnext({e})")
        return int(result)

    def kpnext(self, k: int) -> int:
        """
        Next selected keypoint having a keypoint number greater than k.

        :param k: int
        :return: int
        """
        result = self._read_inline(f"kpnext({k})")
        return int(result)

    def lsnext(self, l: int) -> int:
        """
        Next selected line having a line number greater than l.

        :param l: int
        :return: int
        """
        result = self._read_inline(f"lsnext({l})")
        return int(result)

    def arnext(self, a: int) -> int:
        """
        Next selected area having an area number greater than a.

        :param a: int
        :return: int
        """
        result = self._read_inline(f"arnext({a})")
        return int(result)

    def vlnext(self, v: int) -> int:
        """
        Next selected volume having a volume number greater than v.

        :param v: int
        :return: int
        """
        result = self._read_inline(f"vlnext({v})")
        return int(result)

    # ========================================================================
    # ============================== locations ===============================
    # ========================================================================
    def centrx(self, e: int) -> float:
        """
        Centroid x-coordinate of element e in global Cartesian coordinate system.

        :param e: int
        :return: float
        """
        result = self._read_inline(f"centrx({e})")
        return result

    def centry(self, e: int) -> float:
        """
        Centroid y-coordinate of element e in global Cartesian coordinate system.

        :param e: int
        :return: float
        """
        result = self._read_inline(f"centry({e})")
        return result

    def centrz(self, e: int) -> float:
        """
        Centroid z-coordinate of element e in global Cartesian coordinate system.

        :param e: int
        :return: float
        """
        result = self._read_inline(f"centrz({e})")
        return result

    # ========================== not part of ANSYS! ==========================
    def centrxyz(self, e: int) -> Point:
        """
        Centroid coordinates of element e in global Cartesian coordinate system.

        :param e: int
        :return: Point
        """
        x = self._read_inline(f"centrx({e})")
        y = self._read_inline(f"centry({e})")
        z = self._read_inline(f"centrz({e})")
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    def nx(self, n: int) -> float:
        """
        X-coordinate of node n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"nx({n})")
        return result

    def ny(self, n: int) -> float:
        """
        Y-coordinate of node n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"ny({n})")
        return result

    def nz(self, n: int) -> float:
        """
        Z-coordinate of node n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"nz({n})")
        return result

    # ========================== not part of ANSYS! ==========================
    def nxyz(self, n: int) -> Point:
        """
        Coordinates of node n in the active coordinate system.

        :param n: int
        :return: Point
        """
        x = self._read_inline(f"nx({n})")
        y = self._read_inline(f"ny({n})")
        z = self._read_inline(f"nz({n})")
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    def kx(self, n: int) -> float:
        """
        X-coordinate of keypoint n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"kx({n})")
        return result

    def ky(self, n: int) -> float:
        """
        Y-coordinate of keypoint n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"ky({n})")
        return result

    def kz(self, n: int) -> float:
        """
        Z-coordinate of keypoint n in the active coordinate system.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"kz({n})")
        return result

    # ========================== not part of ANSYS! ==========================
    def kxyz(self, n: int) -> Point:
        """
        Coordinates of keypoint n in the active coordinate system.

        :param n: int
        :return: Point
        """
        x = self._read_inline(f"kx({n})")
        y = self._read_inline(f"ky({n})")
        z = self._read_inline(f"kz({n})")
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    @staticmethod
    def _check_lfrac(lfrac: float):
        """
        Raise exception, if lfrac not in (0, 1.0)

        :param lfrac: float
        :return: True
        """
        # todo: raise exception instead of assert
        assert 0.0 <= lfrac <= 1.0, "lfrac must be in the range of 0.0 ... 1.0"
        return True

    def _raise_if_not_line(self, l: float):
        """
        Should raise exception, if line not exists.

        :param l: int
        :return: None
        """
        # todo: check, if line exists -> if not, causes crash (raise exception before!)
        pass

    def lx(self, l: int, lfrac: float) -> float:
        """
        X-coordinate of line l at length fraction lfrac (0.0 to 1.0).

        :param l: int
        :param lfrac: float
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline(f"lx({l},{lfrac})")
        return result

    def ly(self, l: int, lfrac: float) -> float:
        """
        Y-coordinate of line l at length fraction lfrac (0.0 to 1.0).

        :param l: int
        :param lfrac: 0.0 <= lfrac <= 1.0
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline(f"ly({l},{lfrac})")
        return result

    def lz(self, l: int, lfrac: float) -> float:
        """
        Z-coordinate of line l at length fraction lfrac (0.0 to 1.0).

        :param l: int
        :param lfrac: 0.0 <= lfrac <= 1.0
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline(f"lz({l},{lfrac})")
        return result

    # ========================== not part of ANSYS! ==========================
    def lxyz(self, l: int, lfrac: float) -> Point:
        """
        Coordinates of line l at length fraction lfrac (0.0 to 1.0).

        :param l: int
        :param lfrac: float
        :return: Point
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        x = self._read_inline(f"lx({l},{lfrac})")
        y = self._read_inline(f"ly({l},{lfrac})")
        z = self._read_inline(f"lz({l},{lfrac})")
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    # ========================================================================
    # ========================= nearest to location ==========================
    # ========================================================================
    def node(self, x: float, y: float, z: float) -> int:
        """
        Number of the selected node nearest the x,y,z point
        (in the active coordinate system; lowest number for coincident nodes)

        :param x: float
        :param y: float
        :param z: float
        :return: int
        """
        result = self._read_inline(f"node({x},{y},{z})")
        # todo: raise exception, if result == 0 (no node found)
        return int(result)

    def kp(self, x: float, y: float, z: float) -> int:
        """
        Number of the selected keypoint nearest the X,Y,Z point
        (in the active coordinate system; lowest number for coincident keypoints)

        :param x: float
        :param y: float
        :param z: float
        :return: int
        """
        result = self._read_inline(f"kp({x},{y},{z})")
        # todo: raise exception, if result == 0 (no node found)
        return int(result)

    # ========================================================================
    # =============================== Distance ===============================
    # ========================================================================
    def distnd(self, n1: int, n2: int) -> float:
        """
        Distance between nodes n1 and n2.

        :param n1: int
        :param n2: int
        :return: float
        """
        result = self._read_inline(f"distnd({n1},{n2})")
        return result

    def distkp(self, k1: int, k2: int) -> float:
        """
        Distance between keypoints k1 and k2.

        :param k1: int
        :param k2: int
        :return: float
        """
        result = self._read_inline(f"distkp({k1},{k2})")
        return result

    def disten(self, e: int, n: int) -> float:
        """
        Distance between the centroid of element e and node n.
        Centroid is determined from the selected nodes on the element.

        :param e: int
        :param n: int
        :return: float
        """
        result = self._read_inline(f"disten({e},{n})")
        return result

    # ========================================================================
    # ================================ Angles ================================
    # ========================================================================
    def anglen(self, n1: int, n2: int , n3: int) -> float:
        """
        Subtended angle between two lines, defined by three nodes
        where n1 is the vertex node. Default is in radians.
        (see the *AFUN command to select degrees).

        :param n1: int
        :param n2: int
        :param n3: int
        :return: float
        """
        result = self._read_inline(f"anglen({n1},{n2},{n3})")
        return result

    def anglek(self, k1: int, k2: int, k3: int) -> float:
        """
        Subtended angle between two lines.
        (defined by three keypoints where k1 is the vertex keypoint)
        Default is in radians (see the *AFUN command to select degrees).

        :param k1: int
        :param k2: int
        :param k3: int
        :return: float
        """
        result = self._read_inline(f"anglek({k1},{k2},{k3})")
        return result

    # ========================================================================
    # ========================== nearest to entity ===========================
    # ========================================================================
    def nnear(self, n: int) -> int:
        """
        Selected node nearest node n.

        :param n: int
        :return: float
        """
        result = self._read_inline(f"nnear({n})")
        return int(result)

    def knear(self, k: int) -> int:
        """
        Selected keypoint nearest keypoint k.

        :param k: int
        :return: float
        """
        result = self._read_inline(f"knear({k})")
        return int(result)

    def enearn(self, n: int) -> int:
        """
        Selected element nearest node n.
        The element position is calculated from the selected nodes.

        :param n: int
        :return: int
        """
        result = self._read_inline(f"enearn({n})")
        return int(result)

    # ========================================================================
    # ================================ Areas =================================
    # ========================================================================
    # todo

    # ========================================================================
    # =============================== Normals ================================
    # ========================================================================
    # todo

    # ========================================================================
    # ============================ Connectivity ==============================
    # ========================================================================
    # todo

    # ========================================================================
    # ================================ Faces =================================
    # ========================================================================
    # todo

    # ========================================================================
    # ====================== Degree of freedom results =======================
    # ========================================================================
    def ux(self, n: int) -> float:
        """
        UX structural displacement at node N

        :param n: int
        :return: float
        """
        result = self._read_inline(f"ux({n})")
        return result

    def uy(self, n: int) -> float:
        """
        UY structural displacement at node N

        :param n: int
        :return: float
        """
        result = self._read_inline(f"uy({n})")
        return result

    def uz(self, n: int) -> float:
        """
        UZ structural displacement at node N

        :param n: int
        :return: float
        """
        result = self._read_inline(f"uz({n})")
        return result

    # ========================== not part of ANSYS! ==========================
    def uxyz(self, n: int) -> Point:
        """
        Structural displacement at node N as Point.

        :param n: int
        :return: Point
        """
        x = self._read_inline(f"ux({n})")
        y = self._read_inline(f"uy({n})")
        z = self._read_inline(f"uz({n})")
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    # todo
