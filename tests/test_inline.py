import pytest

from inline import Inline as Inline
from inline import Status as Status

@pytest.fixture(scope='session')
def inline(setup_ansys):
    yield Inline(setup_ansys)

@pytest.fixture(scope='class')
def setup_data(setup_ansys):
    setup_ansys.prep7()
    # todo: change to dictionary
    k1 = setup_ansys.k("", 0, 0, 0)
    k2 = setup_ansys.k("", 1, 0, 0)
    k3 = setup_ansys.k("", 0, 1, 0)
    k4 = setup_ansys.k("", 1, 1, 1)
    k5 = setup_ansys.k("", -1, -1, -1)
    l1 = setup_ansys.l(k1, k2)
    l2 = setup_ansys.l(k2, k3)
    a1 = setup_ansys.a(k1, k2, k3)
    a2 = setup_ansys.a(k2, k3, k4)
    # todo: add returnvalue to mapdl.v()
    v1 = setup_ansys.v(k1, k2, k3, k4)
    v2 = setup_ansys.v(k1, k2, k3, k5)
    # todo: add returnvalue to mapdl.n()
    n1 = setup_ansys.n("", 0, 0, 0)
    n2 = setup_ansys.n("", 1, 0, 0)
    n3 = setup_ansys.n("", 1, 1, 0)
    n4 = setup_ansys.n("", 0, 1, 1)

    setup_ansys.et("", 183)
    e1 = setup_ansys.e(1, 2,3, 4)
    yield
    setup_ansys.clear()


@pytest.fixture(scope='function')
def select_one(setup_ansys):
    setup_ansys.nsel("S", "NODE", "", 1)
    setup_ansys.ksel("S", "KP", "", 1)
    setup_ansys.lsel("S", "LINE", "", 1)
    setup_ansys.asel("S", "AREA", "", 1)
    setup_ansys.vsel("S", "VOLU", "", 1)
    setup_ansys.esel("S", "ELEM", "", 1)


@pytest.fixture(scope='function')
def select_all(setup_ansys):
    setup_ansys.allsel()


class TestInline:
    def test__read_inline(self, inline, setup_data, select_one):
        result = inline._read_inline("3")
        assert result == 3
    # todo: parametrize
    def test_nsel(self, inline, setup_data, select_one):
        assert inline.nsel(0) == Status.UNDEFINED
        assert inline.nsel(1) == Status.SELECTED
        assert inline.nsel(2) == Status.UNSELECTED

    def test_esel(self, inline, setup_data, select_one):
        assert inline.esel(0) == Status.UNDEFINED
        assert inline.esel(1) == Status.SELECTED
        # assert inline.esel(2) == Status.UNSELECTED

    def test_ksel(self, inline, setup_data, select_one):
        assert inline.ksel(0) == Status.UNDEFINED
        assert inline.ksel(1) == Status.SELECTED
        assert inline.ksel(2) == Status.UNSELECTED

    def test_lsel(self, inline, setup_data, select_one):
        assert inline.lsel(0) == Status.UNDEFINED
        assert inline.lsel(1) == Status.SELECTED
        assert inline.lsel(2) == Status.UNSELECTED

    def test_asel(self, inline, setup_data, select_one):
        assert inline.asel(0) == Status.UNDEFINED
        assert inline.asel(1) == Status.SELECTED
        assert inline.asel(2) == Status.UNSELECTED

    def test_vsel(self, inline, setup_data, select_one):
        assert inline.vsel(0) == Status.UNDEFINED
        assert inline.vsel(1) == Status.SELECTED
        assert inline.vsel(2) == Status.UNSELECTED

    def test_ndnext(self, inline, setup_data, select_all):
        assert inline.ndnext(0) == 1
        assert inline.ndnext(3) == 4
        assert inline.ndnext(4) == 0
        assert inline.ndnext(40) == 0

    def test_elnext(self, inline, setup_data, select_all):
        assert False

    def test_kpnext(self, inline, setup_data, select_all):
        assert False

    def test_lsnext(self, inline, setup_data, select_all):
        assert False

    def test_arnext(self, inline, setup_data, select_all):
        assert False

    def test_vlnext(self, inline, setup_data, select_all):
        assert False

    def test_centrx(self, inline, setup_data):
        assert False

    def test_centry(self, inline, setup_data):
        assert False

    def test_centrz(self, inline, setup_data):
        assert False

    def test_centrxyz(self, inline, setup_data):
        assert False

    def test_nx(self, inline, setup_data):
        assert False

    def test_ny(self, inline, setup_data):
        assert False

    def test_nz(self, inline, setup_data):
        assert False

    def test_nxyz(self, inline, setup_data):
        assert False

    def test_kx(self, inline, setup_data):
        assert False

    def test_ky(self, inline, setup_data):
        assert False

    def test_kz(self, inline, setup_data):
        assert False

    def test_kxyz(self, inline, setup_data):
        assert False

    def test__check_lfrac(self, inline, setup_data):
        assert False

    def test__raise_if_not_line(self, inline, setup_data):
        assert False

    def test_lx(self, inline, setup_data):
        assert False

    def test_ly(self, inline, setup_data):
        assert False

    def test_lz(self, inline, setup_data):
        assert False

    def test_lxyz(self, inline, setup_data):
        assert False

    def test_node(self, inline, setup_data):
        assert False

    def test_kp(self, inline, setup_data):
        assert False

    def test_distnd(self, inline, setup_data):
        assert False

    def test_distkp(self, inline, setup_data):
        assert False

    def test_disten(self, inline, setup_data):
        assert False

    def test_anglen(self, inline, setup_data):
        assert False

    def test_anglek(self, inline, setup_data):
        assert False

    def test_nnear(self, inline, setup_data):
        assert False

    def test_knear(self, inline, setup_data):
        assert False

    def test_enearn(self, inline, setup_data):
        assert False

    def test_ux(self, inline, setup_data):
        assert False

    def test_uy(self, inline, setup_data):
        assert False

    def test_uz(self, inline, setup_data):
        assert False

    def test_uxyz(self, inline, setup_data):
        assert False
