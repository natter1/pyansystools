import pytest
import pyansys


@pytest.fixture(scope='session')
def ansys(tmp_path_factory):
    path = tmp_path_factory.getbasetemp()
    ansys = pyansys.Mapdl(override=True, interactive_plotting=True,
                          run_location=path, loglevel='ERROR')
    yield ansys
    # ansys.open_gui()
    ansys.exit()


@pytest.fixture(scope='class')
def mapdl(ansys):
    yield ansys
    ansys.clear()