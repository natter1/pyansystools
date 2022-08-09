"""
@author: Nathanael Jöhrmann
"""
from pyansystools.material import Material


class _Al(Material):
    """
    Warning: this is not a standard _Al, but results for a specific thin film. More details can be found in:
    10.1109/THERMINIC52472.2021.9626510
    This is only meant as an example for using a material with Ramberg Osgood.
    """
    def __init__(self):
        super().__init__()
        self.dens = 2.7E-9
        self.ex = 76220  # in MPa Elastic Isotropic Modulus
        self.prxy = 0.32  # major Poisson's Ratio
        self.ctex = 22.2e-6  # CTE (http://www.engineeringtoolbox.com/linear-expansion-coefficients-d_95.html)
                                # 23.2 .. 23.8 http://dx.doi.org/10.6028/jres.048.030
                                # 22.17 .. 24.6	http://dx.doi.org/10.6028/nbsscipaper.179
        # Ramberg Osgood (n-K formula)
        self.ro_n = 11.714
        self.ro_K = 4 / (261.15 / self.ex)**(self.ro_n-1)  # alpha = K ( sy / E)**(n-1); alpha = 4; sy = 261,15


class Si(Material):
    """
    M. A. Hopcroft, W. D. Nix, and T. W. Kenny, "What is the Young's Modulus of Silicon?",
    IEEE Journal of Microelectromechanical Systems, vol. 19, Issue 2, pp. 229-238, 2010
    (DOI: 10.1109/JMEMS.2009.2039697).
    """
    def __init__(self):
        super().__init__()
        self.dens = 2.336E-9  # Density in t/mm^3

        # Hopcroft et al. - 2010 - What is the Young's Modulus of Silicon
        self.ex = 169000  # in MPa [110]
        self.ey = 169000  # in MPa [110]
        self.ez = 130000  # in MPa [100]


        # self.prxy = 0.2
        self.prxy = 0.064
        self.pryz = 0.36
        self.przx = 0.28

        self.gxy = 50900  # shear module [MPa]
        self.gyz = 79600  # shear module [MPa]
        self.gzx = 79600  # shear module [MPa]

        self.ctex = 3.0e-6  # CTE


# class Si111(Material):
#     """todo: class is incomplete (don't use)"""
#     def __init__(self):
#         super().__init__()
#         self.dens = 2.336E-9  # Density in t/mm^3
#         # todo:
#         # self.ex = 169000  # in MPa [110]
#         # self.ey = 169000  # in MPa [110]
#         # self.ez = 130000  # in MPa [100]
#         self.prxy = 0.2
#         self.ctex = 3.0e-6  # CTE
#
#         # Hopcroft std. Werte
