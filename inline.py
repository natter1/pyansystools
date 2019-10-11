"""
Provides a class to directly use inline-functions in ANSYS via pyansys
Creates/overwrites ANSYS-Paramter `__inline__'!
@author: Nathanael Jöhrmann
"""

from enum import IntEnum
import re
import pyansys
from geo2d import Point as Point


class Status(IntEnum):
    """
    Enumeration for Status Informations to use with Inline.
    """
    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1


class Inline:
    def __init__(self, ansys):
        assert isinstance(ansys, pyansys.Mapdl)
        self._ansys = ansys

    def _read_inline(self, str_inline):
        """
        Use an Inline-Function and return its value.
        :param str_inline: str
            String containing the complete inline-function
        :return: float
        """
        line = self._ansys.run("__inline__={}".format(str_inline))
        return float(re.search(r"(?<==).*", line).group(0))

    # ========================================================================
    # ============================ entity status =============================
    # ========================================================================
    def nsel(self, n):
        """
        Status of node n (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param n: int
            node number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("nsel({})".format(n))
        return Status(result)

    def esel(self, e):
        """
        Status of element e (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param e: int
            element number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("esel({})".format(e))
        return Status(result)

    def ksel(self, k):
        """
        Status of keypoint e (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param k: int
            keypoint number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("ksel({})".format(k))
        return Status(result)

    def lsel(self, l):
        """
        Status of keypoint e (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param l: int
            keypoint number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("lsel({})".format(l))
        return Status(result)

    def asel(self, a):
        """
        Status of area a (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param a: int
            keypoint number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("asel({})".format(a))
        return Status(result)

    def vsel(self, v):
        """
        Status of volume v (-1=UNSELECTED, 0=UNDEFINED, 1=SELECTED)
        :param v: int
            volume number in ANSYS
        :return: Status(IntEnum)
            (Status.UNSELECTED=-1, Status.UNDEFINED=0, Status.SELECTED=1)
        """
        result = self._read_inline("vsel({})".format(v))
        return Status(result)

    # ========================================================================
    # ========================= next selected entity =========================
    # ========================================================================
    def ndnext(self, n):
        """
        Next selected node having a node number greater than b
        :param n: int
        :return: int
        """
        result = self._read_inline("ndnext({})".format(n))
        return int(result)

    def elnext(self, e):
        """
        Next selected element having an element number greater than e.
        :param e: int
        :return: int
        """
        result = self._read_inline("elnext({})".format(e))
        return int(result)

    def kpnext(self, k):
        """
        Next selected keypoint having a keypoint number greater than k.
        :param k: int
        :return: int
        """
        result = self._read_inline("kpnext({})".format(k))
        return int(result)

    def lsnext(self, l):
        """
        Next selected line having a line number greater than l.
        :param l: int
        :return: int
        """
        result = self._read_inline("lsnext({})".format(l))
        return int(result)

    def arnext(self, a):
        """
        Next selected area having an area number greater than a.
        :param a: int
        :return: int
        """
        result = self._read_inline("arnext({})".format(a))
        return int(result)

    def vlnext(self, v):
        """
        Next selected volume having a volume number greater than v.
        :param v: int
        :return: int
        """
        result = self._read_inline("vlnext({})".format(v))
        return int(result)

    # ========================================================================
    # ============================== locations ===============================
    # ========================================================================
    def centrx(self, e):
        """
        Centroid x-coordinate of element e in global Cartesian coordinate system.
        :param e: int
        :return: float
        """
        result = self._read_inline("centrx({})".format(e))
        return result

    def centry(self, e):
        """
        Centroid y-coordinate of element e in global Cartesian coordinate system.
        :param e: int
        :return: float
        """
        result = self._read_inline("centry({})".format(e))
        return result

    def centrz(self, e):
        """
        Centroid z-coordinate of element e in global Cartesian coordinate system.
        :param e: int
        :return: float
        """
        result = self._read_inline("centrz({})".format(e))
        return result

    # ========================== not part of ANSYS! ==========================
    def centrxyz(self, e):
        """
        Centroid coordinates of element e in global Cartesian coordinate system.
        :param e: int
        :return: Point
        """
        x = self._read_inline("centrx({})".format(e))
        y = self._read_inline("centry({})".format(e))
        z = self._read_inline("centrz({})".format(e))
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    def nx(self, n):
        """
        X-coordinate of node n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("nx({})".format(n))
        return result

    def ny(self, n):
        """
        Y-coordinate of node n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("ny({})".format(n))
        return result

    def nz(self, n):
        """
        Z-coordinate of node n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("nz({})".format(n))
        return result

    # ========================== not part of ANSYS! ==========================
    def nxyz(self, n):
        """
        Coordinates of node n in the active coordinate system.
        :param n: int
        :return: Point
        """
        x = self._read_inline("nx({})".format(n))
        y = self._read_inline("ny({})".format(n))
        z = self._read_inline("nz({})".format(n))
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    def kx(self, n):
        """
        X-coordinate of keypoint n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("kx({})".format(n))
        return result

    def ky(self, n):
        """
        Y-coordinate of keypoint n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("ky({})".format(n))
        return result

    def kz(self, n):
        """
        Z-coordinate of keypoint n in the active coordinate system.
        :param n: int
        :return: float
        """
        result = self._read_inline("kz({})".format(n))
        return result

    # ========================== not part of ANSYS! ==========================
    def kxyz(self, n):
        """
        Coordinates of keypoint n in the active coordinate system.
        :param n: int
        :return: Point
        """
        x = self._read_inline("kx({})".format(n))
        y = self._read_inline("ky({})".format(n))
        z = self._read_inline("kz({})".format(n))
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    @staticmethod
    def _check_lfrac(lfrac):
        """
        Raise exception, if lfrac not in (0, 1.0)
        :param lfrac: float
        :return: True
        """
        # todo: raise exception instead of assert
        assert 0.0 <= lfrac <= 1.0, "lfrac must be in the range of 0.0 ... 1.0"
        return True

    def _raise_if_not_line(self, l):
        """
        Should raise exception, if line not exists.
        :param l: int
        :return: None
        """
        # todo: check, if line exists -> if not, causes crash (raise exception before!)
        pass

    def lx(self, l, lfrac):
        """
        X-coordinate of line l at length fraction lfrac (0.0 to 1.0).
        :param l: int
        :param lfrac: float
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline("lx({},{})".format(l, lfrac))
        return result

    def ly(self, l, lfrac):
        """
        Y-coordinate of line l at length fraction lfrac (0.0 to 1.0).
        :param l: int
        :param lfrac: float
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline("ly({},{})".format(l, lfrac))
        return result

    def lz(self, l, lfrac):
        """
        Z-coordinate of line l at length fraction lfrac (0.0 to 1.0).
        :param l: int
        :param lfrac: float
        :return: float
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        result = self._read_inline("lz({},{})".format(l, lfrac))
        return result

    # ========================== not part of ANSYS! ==========================
    def lxyz(self, l, lfrac):
        """
        Coordinates of line l at length fraction lfrac (0.0 to 1.0).
        :param l: int
        :param lfrac: float
        :return: Point
        """
        self._check_lfrac(lfrac)
        self._raise_if_not_line(l)
        x = self._read_inline("lx({},{})".format(l, lfrac))
        y = self._read_inline("ly({},{})".format(l, lfrac))
        z = self._read_inline("lz({},{})".format(l, lfrac))
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    # ========================================================================
    # ========================= nearest to location ==========================
    # ========================================================================
    def node(self, x, y, z):
        """
        Number of the selected node nearest the x,y,z point
        (in the active coordinate system; lowest number for coincident nodes)
        :param x: float
        :param y: float
        :param z: float
        :return: int
        """
        result = self._read_inline("node({},{},{})".format(x, y, z))
        # todo: raise exception, if result == 0 (no node found)
        return int(result)

    def kp(self, x, y, z):
        """
        Number of the selected keypoint nearest the X,Y,Z point
        (in the active coordinate system; lowest number for coincident keypoints)
        :param x: float
        :param y: float
        :param z: float
        :return: int
        """
        result = self._read_inline("kp({},{},{})".format(x, y, z))
        # todo: raise exception, if result == 0 (no node found)
        return int(result)

    # ========================================================================
    # =============================== Distance ===============================
    # ========================================================================
    def distnd(self, n1, n2):
        """
        Distance between nodes n1 and n2.
        :param n1: int
        :param n2: int
        :return: float
        """
        result = self._read_inline("distnd({},{})".format(n1, n2))
        return result

    def distkp(self, k1, k2):
        """
        Distance between keypoints k1 and k2.
        :param n1: int
        :param n2: int
        :return: float
        """
        result = self._read_inline("distkp({},{})".format(k1, k2))
        return result

    def disten(self, e, n):
        """
        Distance between the centroid of element e and node n.
        Centroid is determined from the selected nodes on the element.
        :param e: int
        :param n: int
        :return: float
        """
        result = self._read_inline("disten({},{})".format(e, n))
        return result

    # ========================================================================
    # ================================ Angles ================================
    # ========================================================================
    def anglen(self, n1, n2, n3):
        """
        Subtended angle between two lines.
        (defined by three nodes where n1 is the vertex node)
        Default is in radians (see the *AFUN command to select degrees).
        :param n1: int
        :param n2: int
        :param n3: int
        :return: float
        """
        result = self._read_inline("anglen({},{},{})".format(n1, n2, n3))
        return result

    def anglek(self, k1, k2, k3):
        """
        Subtended angle between two lines.
        (defined by three keypoints where k1 is the vertex keypoint)
        Default is in radians (see the *AFUN command to select degrees).
        :param n1: int
        :param n2: int
        :param n3: int
        :return: float
        """
        result = self._read_inline("anglek({},{},{})".format(k1, k2, k3))
        return result

    # ========================================================================
    # ========================== nearest to entity ===========================
    # ========================================================================
    def nnear(self, n):
        """
        Selected node nearest node n.
        :param n: int
        :return: float
        """
        result = self._read_inline("nnear({})".format(n))
        return int(result)

    def knear(self, k):
        """
        Selected keypoint nearest keypoint k.
        :param k: int
        :return: float
        """
        result = self._read_inline("nnear({})".format(n))
        return int(result)

    def enearn(self, n):
        """
        Selected element nearest node n.
        The element position is calculated from the selected nodes.
        :param n: int
        :return: int
        """
        result = self._read_inline("enearn({})".format(n))
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
    def ux(self, n):
        """
        UX structural displacement at node N
        :param n: int
        :return: float
        """
        result = self._read_inline("ux({})".format(n))
        return result

    def uy(self, n):
        """
        UX structural displacement at node N
        :param n: int
        :return: float
        """
        result = self._read_inline("uy({})".format(n))
        return result

    def uz(self, n):
        """
        UX structural displacement at node N
        :param n: int
        :return: float
        """
        result = self._read_inline("uz({})".format(n))
        return result

    # ========================== not part of ANSYS! ==========================
    def uxyz(self, n):
        """
        Structural displacement at node N as Point.
        :param n: int
        :return: Point
        """
        x = self._read_inline("ux({})".format(n))
        y = self._read_inline("uy({})".format(n))
        z = self._read_inline("uz({})".format(n))
        return Point(x, y, z)
    # ========================= not part of ANSYS! END ========================

    # todo