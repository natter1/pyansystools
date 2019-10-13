import pytest
from enum import Enum, auto
from inline import Inline
from inline import Status


class TestCase(Enum):
    """
    Enumeration for selection test cases.
    """
    ZERO = auto()
    TOOLARGE = auto()
    UNSELECTED = auto()
    SELECTED =auto()

# [test case, expected result]
select_params = [[TestCase.ZERO, Status.UNDEFINED],
                 [TestCase.TOOLARGE, Status.UNDEFINED],
                 [TestCase.UNSELECTED, Status.UNSELECTED],
                 [TestCase.SELECTED, Status.SELECTED]]

select_ids = ['ZERO',
              'TOOLARGE',
              'UNSELECTED',
              'SELECTED']

class Data(list):
    @property
    def selected(self):
        return min(self)

    @property
    def unselected(self):
        return max(self)

    @property
    def too_large(self):
        return 10^6  # max(self)+1

    def get_case_data(self, case):
        if case == TestCase.ZERO:
            return 0
        elif case == TestCase.TOOLARGE:
            return self.too_large
        elif case == TestCase.UNSELECTED:
            return self.unselected
        elif case == TestCase.SELECTED:
            return self.selected
        raise  # todo: specific exception

    def get_select_test_data(self):
        return [0, self.selected, self.unselected, self.invalid]

    def get_expected_select_results(self):
        return [Status.UNDEFINED,
                Status.SELECTED,
                Status.UNSELECTED,
                Status.UNDEFINED]


@pytest.fixture(scope='session')
def inline(ansys):
    yield Inline(ansys)


@pytest.fixture(scope='class')
def setup_data(ansys):
    ansys.prep7()
    k = Data()
    l = Data()
    a = Data()
    v = Data()
    n = Data()
    k.append(ansys.k("", 0, 0, 0))
    k.append(ansys.k("", 1, 0, 0))
    k.append(ansys.k("", 0, 1, 0))
    k.append(ansys.k("", 1, 1, 1))
    k.append(ansys.k("", -1, -1, -1))
    l.append(ansys.l(*k[0:2]))
    l.append(ansys.l(*k[1:3]))
    a.append(ansys.a(*k[0:3]))
    a.append(ansys.a(*k[1:4]))
    # todo: add returnvalue to mapdl.v()
    v.append(ansys.v(*k[0:4]))
    v.append(ansys.v(*k[0:3], k[4]))
    # todo: add returnvalue to mapdl.n()
    n.append(ansys.n("", 0, 0, 0))
    n.append(ansys.n("", 1, 0, 0))
    n.append(ansys.n("", 1, 1, 0))
    n.append(ansys.n("", 0, 1, 1))

    ansys.et("", 183)
    e1 = ansys.e(1, 2, 3, 4)
    yield [k, l, a, v, n]
    ansys.clear()


@pytest.fixture(scope='function')
def select_one(ansys):
    ansys.ksel("S", "KP", "", 1)
    ansys.lsel("S", "LINE", "", 1)
    ansys.asel("S", "AREA", "", 1)
    ansys.vsel("S", "VOLU", "", 1)
    ansys.nsel("S", "NODE", "", 1)
    ansys.esel("S", "ELEM", "", 1)


@pytest.fixture(scope='function')
def select_all(ansys):
    ansys.allsel()


@pytest.fixture(scope='function', params=select_params, ids=select_ids)
def select_task(select_one, request):
    return request.param


class TestInline:
    def test__read_inline(self, inline, select_one):
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

    def test_ksel(self, inline, setup_data, select_task):
        k = setup_data[0].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.ksel(k) == expected

    def test_lsel(self, inline, setup_data, select_task):
        l = setup_data[1].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.lsel(l) == expected

    def test_asel(self, inline, setup_data, select_task):
        a = setup_data[2].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.asel(a) == expected

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
