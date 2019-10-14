import pytest
import math

from inline import Inline
from inline import Status
from testcases import Data, TestCase
from geo2d import Point


# [test case, expected result]
select_params = [[TestCase.ZERO, Status.UNDEFINED],
                 [TestCase.TOOLARGE, Status.UNDEFINED],
                 [TestCase.UNSELECTED, Status.UNSELECTED],
                 [TestCase.SELECTED, Status.SELECTED]]

select_ids = ['ZERO',
              'TOOLARGE',
              'UNSELECTED',
              'SELECTED']

next_params = [[TestCase.ZERO, 1],
               [TestCase.MIN, 2],
               [TestCase.MAX, 0],
               [TestCase.TOOLARGE, 0]]

next_ids = ['ZERO',
            'MIN',
            'MAX',
            'TOOLARGE']


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
    e = Data()
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
    n.append(ansys.n("", 0, 1, -1))

    ansys.et("", 183)
    e.append(ansys.e(1, 2, 3, 4))
    e.append(ansys.e(1, 2, 3, 5))

    l.append(ansys.get_float('LINE', 0, 'NUM', 'MAXD'))
    a.append(ansys.get_float('AREA', 0, 'NUM', 'MAXD'))
    yield {'k': k, 'l': l, 'a': a, 'v': v, 'n': n, 'e': e}
    ansys.clear()


@pytest.fixture(scope='function')
def select_one(ansys, setup_data):
    """
    Select one entry (the one specified for this TestCase inside class Data)
    for each type (line, area) and makes all other entries unselected.
    """
    ansys.ksel("S", "KP", "", setup_data['k'].selected)
    ansys.lsel("S", "LINE", "", setup_data['l'].selected)
    ansys.asel("S", "AREA", "", setup_data['a'].selected)
    ansys.vsel("S", "VOLU", "", setup_data['v'].selected)
    ansys.nsel("S", "NODE", "", 1)
    ansys.esel("S", "ELEM", "", 1)


@pytest.fixture(scope='function')
def select_all(ansys):
    ansys.allsel()


@pytest.fixture(scope='function', params=select_params, ids=select_ids)
def select_task(select_one, request):
    return request.param

@pytest.fixture(scope='function', params=next_params, ids=next_ids)
def next_task(select_all, request):
    return request.param

class TestInline:
    def test__read_inline(self, inline, select_one):
        result = inline._read_inline("3")
        assert result == 3

    # todo: parametrize
    def test_nsel(self, inline, setup_data, select_task):
        n = setup_data['n'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.nsel(n) == expected

    def test_esel(self, inline, setup_data, select_task):
        e = setup_data['e'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.esel(e) == expected
        # assert inline.esel(0) == Status.UNDEFINED
        # assert inline.esel(1) == Status.SELECTED
        # assert inline.esel(2) == Status.UNSELECTED

    def test_ksel(self, inline, setup_data, select_task):
        k = setup_data['k'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.ksel(k) == expected

    def test_lsel(self, inline, setup_data, select_task):
        l = setup_data['l'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.lsel(l) == expected

    def test_asel(self, inline, setup_data, select_task):
        a = setup_data['a'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.asel(a) == expected

    def test_vsel(self, inline, setup_data, select_task):
        v = setup_data['v'].get_case_data(select_task[0])
        expected = select_task[1]
        assert inline.vsel(v) == expected

    def test_ndnext(self, inline, setup_data, next_task):
        n = setup_data['n'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.ndnext(n) == expected

    def test_elnext(self, inline, setup_data, next_task):
        e = setup_data['e'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.elnext(e) == expected

    def test_kpnext(self, inline, setup_data, next_task):
        k = setup_data['k'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.kpnext(k) == expected

    def test_lsnext(self, inline, setup_data, next_task):
        l = setup_data['l'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.lsnext(l) == expected

    def test_arnext(self, inline, setup_data, next_task):
        a = setup_data['a'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.arnext(a) == expected

    def test_vlnext(self, inline, setup_data, next_task):
        v = setup_data['v'].get_case_data(next_task[0])
        expected = next_task[1]
        assert inline.vlnext(v) == expected

    def test_centrx(self, inline, setup_data):
        assert inline.centrx(setup_data['e'].min) == 0.5

    def test_centry(self, inline, setup_data):
        assert inline.centry(setup_data['e'].min) == 0.5

    def test_centrz(self, inline, setup_data):
        assert inline.centrz(setup_data['e'].min) == 0.25

    def test_centrxyz(self, inline, setup_data):
        dummy = inline.centrxyz(setup_data['e'].min)
        assert inline.centrxyz(setup_data['e'].min) == Point(0.5, 0.5, 0.25)

    def test_nx(self, inline, setup_data):
        assert inline.nx(setup_data['n'].max) == 0

    def test_ny(self, inline, setup_data):
        assert inline.ny(setup_data['n'].max) == 1

    def test_nz(self, inline, setup_data):
        assert inline.nz(setup_data['n'].max) == -1

    def test_nxyz(self, inline, setup_data):
        assert inline.nxyz(setup_data['n'].max) == Point(0, 1, -1)

    def test_kx(self, inline, setup_data):
        assert inline.kx(setup_data['k'].max) == -1

    def test_ky(self, inline, setup_data):
        assert inline.ky(setup_data['k'].min) == 0

    def test_kz(self, inline, setup_data):
        assert inline.kz(setup_data['k'].max) == -1

    def test_kxyz(self, inline, setup_data):
        assert inline.kxyz(setup_data['k'].max) == Point(-1, -1, -1)

    def test__check_lfrac(self, inline, setup_data):
        assert inline._check_lfrac(0.9)
        # todo: check exception, if not in range (0, 1)

    def test__raise_if_not_line(self, inline, setup_data):
        # todo: function not implemented yet
        assert inline._raise_if_not_line(setup_data['l'].max) == None

    def test_lx(self, inline, setup_data):
        assert inline.lx(setup_data['l'].min, 0.5) == 0.5

    def test_ly(self, inline, setup_data):
        assert inline.ly(setup_data['l'].min, 0.5) == 0

    def test_lz(self, inline, setup_data):
        assert inline.lz(setup_data['l'].max, 0.5) == -0.5

    def test_lxyz(self, inline, setup_data):
        assert inline.lxyz(setup_data['l'].max, 0.5) == Point(-0.5, 0.0, -0.5)

    def test_node(self, inline, setup_data):
        assert inline.node(1, 0, 0) == 2

    def test_kp(self, inline, setup_data):
        assert inline.kp(-1, -1, -1) == 5

    def test_distnd(self, inline, setup_data):
        assert inline.distnd(1, 2) == 1

    def test_distkp(self, inline, setup_data):
        assert inline.distkp(1, 2) == 1

    def test_disten(self, inline, setup_data, select_all):
        assert inline.disten(1, 1) == 0.75

    def test_anglen(self, inline, setup_data):
        assert math.isclose(inline.anglen(1, 2, 3), math.pi/4)

    def test_anglek(self, inline, setup_data):
        assert math.isclose(inline.anglek(1, 2, 3), math.pi/2)

    def test_nnear(self, inline, setup_data, select_one):
        assert inline.nnear(3) == 1  # would be 2 if all nodes selected

    def test_knear(self, inline, setup_data, select_one):
        assert inline.knear(3) == 1

    def test_enearn(self, inline, setup_data):
        assert inline.enearn(5) == 1

    def test_ux(self, inline, setup_data):
        assert inline.ux(1) == 0  # todo: no solution was done jet

    def test_uy(self, inline, setup_data):
        assert inline.uy(1) == 0  # todo: no solution was done jet

    def test_uz(self, inline, setup_data):
        inline._ansys.set_log_level('ERROR')
        assert inline.uz(1) == 0  # todo: no solution was done jet
        inline._ansys.set_log_level('WARN')

    def test_uxyz(self, inline, setup_data):
        assert inline.uxyz(1) == Point(0, 0, 0)
