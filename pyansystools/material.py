"""
unit system:
mm, t, MPa
"""
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


class Material:
    def __init__(self):
        self.dens = None  # Density in t/mm^3
        self.ex = None  # in MPa
        self.ey = None  # in MPa
        self.ez = None  # in MPa
        self.prxy = None  # major Poisson's Ratio
        self.pryz = None
        self.przx = None
        self.gxy = None  # shear module [MPa]
        self.gyz = None  # shear module [MPa]
        self.gzx = None  # shear module [MPa]

        self.ctex = None  # CTE

        # Ramberg Osgood
        self.ro_n = None
        self.ro_K = None

    def set_elastic(self, mapdl: MapdlGrpc, mat_id: int):
        mapdl.run("/PREP7")
        mapdl.mptemp("", "", "", "", "", "", "")
        mapdl.mptemp(1, "T")
        # E-Modulus:
        mapdl.mpdata("EX", mat_id, "", self.ex)
        if self.ey is not None:
            mapdl.mpdata("EY", mat_id, "", self.ey)
        if self.ez is not None:
            mapdl.mpdata("EZ", mat_id, "", self.ez)

        # shear modulus
        if self.gxy is not None:
            mapdl.mpdata("GXY", mat_id, "", self.gxy)
        if self.gyz is not None:
            mapdl.mpdata("GYZ", mat_id, "", self.gyz)
        if self.gzx is not None:
            mapdl.mpdata("GXZ", mat_id, "", self.gzx)

        # Poisson Ratio:
        mapdl.mpdata("PRXY", mat_id, "", self.prxy)
        if self.pryz is not None:
            mapdl.mpdata("PRYZ", mat_id, "", self.pryz)
        if self.przx is not None:
            mapdl.mpdata("PRXZ", mat_id, "", self.przx)

    def set_ramberg_osgood(self, mapdl: MapdlGrpc, mat_id: int, strain_max: float, eps_tol: float = 0.01)\
            -> tuple[list, list]:
        """
        Define stress-strain-curve with 20 data points in mkin-table by using Ramberg-Osgood-Law
        calculate and define stress-strain-curve (total)
        (mkin max 40 temperatures & 20 pairs per temp)
        :param mapdl: MapdlGrpc object
        :param mat_id: Material reference identification number
        :param strain_max: largest strain value in the mkin-table
        :param eps_tol: tolerance for the actual max. strain value compared to eps_max
        :return: tuple (list of stresses, list of strains)
        """
        assert self.ro_n != None, "Can't set RO material data, if Ramberg-Osgood n not set."
        assert self.ro_K != None, "Can't set RO material data, if Ramberg-Osgood k not set."

        stress_max = 100  # only a start value - will be changed later to match strain_max

        mapdl.run("/PREP7")
        mapdl.mptemp("", "", "", "", "", "", "")
        mapdl.mptemp(1, "T")

        steps = 20
        mapdl.tb("KINH", mat_id, 1, steps)  # Activate a data table
        mapdl.tbtemp(0)  # Temperature

        # * Algorithm to find the maximum Strain for given strain_max *
        # *************************************************************
        abort_flag = False
        while not abort_flag:
            eps = stress_max / self.ex + self.ro_K * (
                    stress_max / self.ex) ** self.ro_n
            if (eps >= strain_max - eps_tol) and (
                    eps <= strain_max + eps_tol):
                abort_flag = True
            elif eps > strain_max:
                stress_max /= 1.5
            else:
                stress_max *= 2.0

        stress_list = [0]
        strain_list = [0]

        for i in range(1, steps+1):
            stress = i * stress_max / steps
            strain = (stress / self.ex) + self.ro_K * (stress / self.ex) ** (self.ro_n)
            mapdl.tbpt("", strain, stress)
            stress_list.append(stress)
            strain_list.append(strain)

        return stress_list, strain_list


