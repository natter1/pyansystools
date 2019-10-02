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

    def create_contact_pair_for_lines_symmetric(self, lines_a, lines_b, n_target169 = None, n_conta172 = None):
        """
        Create symmetric contact pairs between given line_numbers.
        Make sure to create nodes for those lines before calling this.
        """
        if not n_target169:
            self._mapdl.et("", 169)  #TARGE169 is used to represent various 2-D 'target' surfaces for the associated contact elements (CONTA171, CONTA172, and CONTA175).
            n_target169 = self.get_float("ETYP", 0, "NUM", "MAX")

        if not n_conta172:
            self._mapdl.et("", 172)  #CONTA172 is used to represent contact and sliding between 2-D target surfaces (TARGE169) and a deformable surface, defined by this element.
            n_conta172 = self.get_float("ETYP", 0, "NUM", "MAX")
            self._mapdl.keyopt(n_conta172, 5, 3)    # natj: (sometimes contact node below tip was not in contact at max load!) Close gap/reduce penetration with auto CNOF
            self._mapdl.keyopt(n_conta172, 9, 0)  #KEYOPT(9) ... Effect of initial penetration or gap; value 0 ... Include both initial geometrical penetration or gap and offset
            self._mapdl.keyopt(n_conta172, 10, 2)  #KEYOPT(10) ... Contact stiffness update; value 2 ... Each iteration based on the current mean stress of underlying elements. The actual elastic slip never exceeds the maximum allowable limit (SLTO) during the entire solution


        self._mapdl.prep7()
        # todo: how to replace fixed number here?
        self._mapdl.real(3)  # Sets the element real constant set attribute pointer. Target and contact elements that make up a contact pair are associated with each other via a shared real constant set

        # Generate the target surface
        self._mapdl.type(n_target169)  # Sets the element type attribute pointer.
        self.select_lines(lines_a)
#        self._mapdl.lsel("S", "", "", self.film.roi_lines[1])
        self._mapdl.nsll("S", 1)  # Selects those nodes associated with the selected lines.
        self._mapdl.esln("S", 0)  # Selects those elements attached to the selected nodes. (those elements must be selected for ESURF to work; ESEL,ALL would also work)
        self._mapdl.esurf()  # Generates elements overlaid on the free faces of selected nodes.; underlaying elements must be selected

        # Generate the contact surface
        self._mapdl.type(self.n_conta172)
        self._mapdl.tip.select_spline_lines()
#        self.lsel("S", "LINE", "", self.tip.lines[3], self.tip.lines[len(self.tip.lines)-1])  # select spline lines of tip
        self._mapdl.nsll("S", 1)
        self._mapdl.esln("S", 0)
        self._mapdl.esurf()

        # * Create Companion Pair - Start
        self._mapdl.real(4)  # Different contact pairs must be defined by a different real constant set, even if the element real constant values do not change.

        # Generate the target surface
        self._mapdl.type(self.n_target169)
        self._mapdl.esel("S", "TYPE", "", 3)
        self._mapdl.nsle("S")
        self._mapdl.esln("S", 0)
        self._mapdl.esurf()

        # Generate the contact surface
        self._mapdl.type(self.n_conta172)
        self._mapdl.esel("S", "TYPE", "", 2)
        self._mapdl.nsle("S")
        self._mapdl.esln("S", 0)
        self._mapdl.esurf()
        # self.Edcontact(0.2)
