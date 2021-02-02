# -*- coding: utf-8 -*-
"""
Collection of Macro-like functions for APDL ANSYS via pyansys.

@author: Nathanael Jöhrmann
"""

import numbers
from typing import Union

# from pyansys import Mapdl
from ansys.mapdl.core import launch_mapdl


class RealConstants172:  # element 172
    def __init__(self):
        self.r1 = ""  # 1:target circle radius
        self.r2 = ""  # 2:superelement thickness
        self.fkn = ""  # 3: normal penalty stiffness factor
        self.ftoln = ""  # 4: penetration tolerance factor
        self.icont = ""  # 5:
        self.pinb = ""  # 6:
        self.pzer = ""  # 7:
        self.czer = ""  # 8:
        self.taumax = ""  # 9:
        self.cnof = ""  # 10:
        self.fkop = ""  # 11:
        self.fkt = ""  # 12:
        self.cohe = ""  # 13:
        self.tcc = ""  # 14:
        self.fhtg = ""  # 15:
        self.sbct = ""  # 15:
        self.rdvf = ""  # 17:
        self.fwgt = ""  # 18:
        # todo: add  mising real constants

    def call_r(self, mapdl, set):
        mapdl.r(set, self.r1, self.r2, self.fkn, self.ftoln, self.icont, self.pinb)
        mapdl.rmore(self.pzer, self.czer, self.taumax, self.cnof, self.fkop, self.fkt)
        mapdl.rmore(self.cohe, self.tcc, self.fhtg, self.sbct, self.rdvf, self.fwgt)

        # todo: self -> cls ?


class Macros:
    def __init__(self, mapdl):
        self._mapdl = mapdl

    def select_lines(self, lines: Union[int, list]):
        """
        Selects the given line numbers (lines) in ANSYS.

        Parameters
        ----------
        lines : list or numeric
            Number(s) of the line(s) to be selected.
        """
        if isinstance(lines, numbers.Number):
            lines = [lines]
        self._mapdl.lsel("none")
        for line_number in lines:
            self._mapdl.lsel("A", "LINE", "", line_number)

    def create_contact_pair_for_lines_asymmetric(self, target_lines: Union[int, list],
                                                 contact_lines: Union[int, list],
                                                 n_target169: int = None,
                                                 n_conta172: int = None,
                                                 constants172: RealConstants172 = None):
        """
        Create asymmetric contact pair between given line_numbers.
        Make sure to create nodes for those lines before calling this.
        """
        self._mapdl.prep7()
        if not n_target169:
            # TARGE169 is used to represent various 2-D 'target' surfaces
            # for the associated contact elements
            # (CONTA171, CONTA172, and CONTA175):
            n_target169 = self._mapdl.et("", 169)

        if not n_conta172:
            # CONTA172 is used to represent contact and sliding between
            # 2-D target surfaces (TARGE169) and a deformable surface,
            # defined by this element:
            n_conta172 = self._mapdl.et("", 172)
            # todo: test only
            # KEYOPT(2) ... Contact algorithm: 3 ... Lagrange multiplier on contact normal and penalty on tangent
            # self._mapdl.keyopt(n_conta172, 2, 3)
            # todo end
            # Close gap/reduce penetration with auto CNOF:
            self._mapdl.keyopt(n_conta172, 5, 3)
            # KEYOPT(9) ... Effect of initial penetration or gap;
            # value 0 ... Include both initial geometrical penetration
            # or gap and offset:
            self._mapdl.keyopt(n_conta172, 9, 0)
            # KEYOPT(10) ... Contact stiffness update;
            # value 2 ... Each iteration based on the current mean stress
            # of underlying elements. The actual elastic slip never exceeds
            # the maximum allowable limit (SLTO) during the entire solution:
            self._mapdl.keyopt(n_conta172, 10, 2)

        # Each contact pairs must be defined by a different real constant set
        next_real = self._mapdl.get_value("RCON", 0, "NUM", "MAX") + 1
        # Target and contact elements that make up a contact pair
        # are associated with each other via a shared real constant set
        self._mapdl.real(next_real)
        # todo: FKN; FTOLN
        # self._mapdl.r(next_real, "", "", 20.0)
        self._mapdl.r(next_real, "", "", "", -1)  # FTOLN = -1 (negative value sets it absolute)

        if constants172:  # overwrites previews values like ftoln
            constants172.call_r(self._mapdl, next_real)

        # Generate the target surface
        # Sets the element type attribute pointer:
        self._mapdl.type(n_target169)
        self.select_lines(target_lines)
        # Selects those nodes associated with the selected lines:
        self._mapdl.nsll("S", 1)
        # Selects those elements attached to the selected nodes:
        # (those elements must be selected for ESURF to work;
        # ESEL,ALL would also work)
        self._mapdl.esln("S", 0)
        # Generates elements overlaid on the free faces of selected nodes:
        # (underlaying elements must be selected!)
        self._mapdl.esurf()

        # Generate the contact surface
        self._mapdl.type(n_conta172)
        self.select_lines(contact_lines)
        self._mapdl.nsll("S", 1)
        self._mapdl.esln("S", 0)
        self._mapdl.esurf()

        return n_target169, n_conta172

    def create_contact_pair_for_lines_symmetric(self, lines_a: Union[int, list],
                                                lines_b: Union[int, list],
                                                n_target169: int = None,
                                                n_conta172: int = None,
                                                constants172: RealConstants172 = None):
        """
        Create symmetric contact pairs between given line_numbers.
        Make sure to create nodes for those lines before calling this.
        """
        # Create Contact Pair:
        n_target169, n_conta172 = self.create_contact_pair_for_lines_asymmetric(lines_a, lines_b, n_target169,
                                                                                n_conta172, constants172)
        # Create Companion Pair:
        self.create_contact_pair_for_lines_asymmetric(lines_b, lines_a, n_target169, n_conta172, constants172)
        # self.Edcontact(0.2)
        return n_target169, n_conta172

    # def create_slide_contact_pair_for_lines_symmetric(self, lines_a: Union[int, list],
    #                                                   lines_b: Union[int, list],
    #                                                   n_target169: int = None,
    #                                                   n_conta172: int = None
    #                                                   friction: float = 0):
    #     None