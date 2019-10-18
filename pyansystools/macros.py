# -*- coding: utf-8 -*-
"""
Collection of Macro-like functions for APDL ANSYS via pyansys.

@author: Nathanael Jöhrmann
"""

import numbers


# todo: self -> cls ?
class Macros:
    def __init__(self, mapdl):
        self._mapdl = mapdl

    def select_lines(self, lines):
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

    def create_contact_pair_for_lines_asymmetric(self, target_lines,
                                                 contact_lines,
                                                 n_target169=None,
                                                 n_conta172=None):
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
        next_real = self._mapdl.get_float("RCON", 0, "NUM", "MAX") + 1
        # Target and contact elements that make up a contact pair
        # are associated with each other via a shared real constant set
        self._mapdl.real(next_real)
        # todo: FKN; FTOLN
        # self._mapdl.r(next_real, "", "", 20.0)
        self._mapdl.r(next_real, "", "", "", -1)
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

    def create_contact_pair_for_lines_symmetric(self, lines_a, lines_b,
                                                n_target169=None,
                                                n_conta172=None):
        """
        Create symmetric contact pairs between given line_numbers.
        Make sure to create nodes for those lines before calling this.
        """
        # Create Contact Pair:
        n_target169, n_conta172 = self.create_contact_pair_for_lines_asymmetric(lines_a, lines_b, n_target169, n_conta172)
        # Create Companion Pair:
        self.create_contact_pair_for_lines_asymmetric(lines_b, lines_a, n_target169, n_conta172)
        # self.Edcontact(0.2)
        return n_target169, n_conta172
